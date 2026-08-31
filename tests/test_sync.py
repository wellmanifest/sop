import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from src.sop import __main__ as module_entry
from src.sop.cli import main
from src.sop.engine import SOPDiffer, SOPPatcher, UnsafePathError
from src.sop.models import PatchOperation
from src.sop.scanner import RepositoryScanner, sha256_file


class TestLocalSync(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.standard = self.root / "standard"
        self.target = self.root / "target"
        self.standard.mkdir()
        self.target.mkdir()
        (self.standard / ".git").mkdir()
        (self.target / ".git").write_text("gitdir: elsewhere", encoding="utf-8")
        (self.standard / "rules.txt").write_text("canonical\n", encoding="utf-8")

    def scanner(self):
        return RepositoryScanner(self.target, self.standard, ("rules.txt",))

    def symlink_or_skip(self, link: Path, target: Path):
        try:
            try:
                link.symlink_to(target)
            except OSError as exc:
                if getattr(exc, "winerror", None) == 1314:
                    raise PermissionError("Windows symlink privilege is unavailable") from exc
                raise
        except PermissionError as exc:
            self.skipTest(f"symlink creation is not permitted: {exc}")

    def test_linked_worktree_is_scanned_and_non_repositories_are_not_counted(self):
        report = self.scanner().scan_all()
        self.assertEqual(report.scanned_repos_count, 1)
        self.assertEqual(report.clean_repos_count, 0)
        self.assertEqual(report.findings[0].rule_id, "SOP-FILE-MISSING")

    def test_dry_run_default_does_not_write_then_explicit_write_verifies(self):
        operations = SOPDiffer.build_patch(self.scanner().scan_all().findings)
        self.assertEqual(SOPPatcher.apply_all(operations), {"planned": 1, "skipped": 0})
        self.assertFalse((self.target / "rules.txt").exists())
        self.assertEqual(SOPPatcher.apply_all(operations, write=True), {"applied": 1, "skipped": 0})
        self.assertEqual(SOPPatcher.verify(operations), [])
        self.assertEqual(
            sha256_file(self.target / "rules.txt"), sha256_file(self.standard / "rules.txt")
        )

    def test_changed_template_invalidates_reviewed_plan(self):
        operation = SOPDiffer.build_patch(self.scanner().scan_all().findings)[0]
        (self.standard / "rules.txt").write_text("changed\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "changed after patch planning"):
            SOPPatcher.apply_operation(operation, write=True)

    def test_batch_preflight_prevents_earlier_write_when_later_source_is_stale(self):
        second_source = self.standard / "second.txt"
        second_source.write_text("second\n", encoding="utf-8")
        scanner = RepositoryScanner(
            self.target, self.standard, ("rules.txt", "second.txt")
        )
        operations = SOPDiffer.build_patch(scanner.scan_all().findings)
        second_source.write_text("stale\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "changed after patch planning"):
            SOPPatcher.apply_all(operations, write=True)
        self.assertFalse((self.target / "rules.txt").exists())
        self.assertFalse((self.target / "second.txt").exists())

    def test_symlink_template_source_is_rejected(self):
        real_source = self.standard / "real.txt"
        link_source = self.standard / "linked.txt"
        real_source.write_text("linked content\n", encoding="utf-8")
        self.symlink_or_skip(link_source, real_source)
        finding = RepositoryScanner(
            self.target, self.standard, ("linked.txt",)
        ).scan_all().findings[0]
        self.assertFalse(finding.auto_fixable)
        self.assertIsNone(finding.source_path)
        operation = PatchOperation(
            str(self.target), "linked.txt", str(link_source), sha256_file(real_source)
        )
        with self.assertRaisesRegex(UnsafePathError, "symlink template source"):
            SOPPatcher.apply_operation(operation, write=True)
        self.assertFalse((self.target / "linked.txt").exists())

    def test_internal_symlink_target_is_rejected_by_apply_and_verify(self):
        real_target = self.target / "real-target.txt"
        link_target = self.target / "linked-target.txt"
        real_target.write_text("must remain unchanged\n", encoding="utf-8")
        self.symlink_or_skip(link_target, real_target)
        source = self.standard / "rules.txt"
        operation = PatchOperation(
            str(self.target), "linked-target.txt", str(source), sha256_file(source)
        )
        with self.assertRaisesRegex(UnsafePathError, "symlink target component"):
            SOPPatcher.apply_operation(operation, write=True)
        with self.assertRaisesRegex(UnsafePathError, "symlink target component"):
            SOPPatcher.verify([operation])
        self.assertEqual(real_target.read_text(encoding="utf-8"), "must remain unchanged\n")

    def test_scanner_rejects_unsafe_or_noncanonical_managed_paths(self):
        unsafe = (
            "../escape",
            ".git/config",
            "nested/.git/config",
            "/absolute",
            "./rules.txt",
            "nested//rules.txt",
            "nested\\rules.txt",
            "C:/outside.txt",
        )
        for relative in unsafe:
            with self.subTest(relative=relative), self.assertRaises(ValueError):
                RepositoryScanner(self.target, self.standard, (relative,))

    def test_path_traversal_and_git_metadata_are_rejected(self):
        source = self.standard / "rules.txt"
        for relative in ("../escape", ".git/config"):
            with self.subTest(relative=relative), self.assertRaises(UnsafePathError):
                SOPPatcher.apply_operation(
                    PatchOperation(str(self.target), relative, str(source), sha256_file(source)),
                    write=True,
                )

    def test_module_entry_delegates_to_cli(self):
        self.assertIs(module_entry.main, main)

    def test_cli_patch_preflights_without_writing(self):
        output = io.StringIO()
        args = [
            "patch",
            "--root",
            str(self.target),
            "--standard",
            str(self.standard),
            "--managed-path",
            "rules.txt",
        ]
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(args), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["preflight"], {"planned": 1, "skipped": 0})
        self.assertFalse((self.target / "rules.txt").exists())

    def test_cli_sync_is_dry_run_by_default_and_rejects_network(self):
        output = io.StringIO()
        args = [
            "sync",
            "--root",
            str(self.target),
            "--standard",
            str(self.standard),
            "--managed-path",
            "rules.txt",
        ]
        with contextlib.redirect_stdout(output):
            self.assertEqual(main(args), 0)
        self.assertEqual(json.loads(output.getvalue())["mode"], "dry-run")
        self.assertFalse((self.target / "rules.txt").exists())
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["scan", "--standard", "https://example.invalid"]), 2)

    def test_cli_verify_reports_drift_then_success(self):
        args = [
            "verify",
            "--root",
            str(self.target),
            "--standard",
            str(self.standard),
            "--managed-path",
            "rules.txt",
        ]
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(args), 1)
        SOPPatcher.apply_all(SOPDiffer.build_patch(self.scanner().scan_all().findings), write=True)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(args), 0)


if __name__ == "__main__":
    unittest.main()
