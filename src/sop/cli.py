import argparse
import sys
import os
import json
from .scanner import RepositoryScanner
from .engine import SOPDiffer, SOPPatcher

from .validator import SOPValidator

def main():
    parser = argparse.ArgumentParser(
        prog="sop",
        description="WellManifest SOP (Standard Operating Procedure) runtime and synchronizer"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # sop scan
    scan_p = subparsers.add_parser("scan", help="Skanuj repozytoria pod kÄ…tem zgodnoĹ›ci z SOP i WellManifest")
    scan_p.add_argument("--root", default=".", help="Katalog nadrzÄ™dny organizacji (domyĹ›lnie .)")
    scan_p.add_argument("--json", action="store_true", help="Format wyjĹ›ciowy JSON")

    # sop sync / apply
    apply_p = subparsers.add_parser("apply", help="Aplikuj poprawki standardĂłw do repozytoriĂłw")
    apply_p.add_argument("--root", default=".", help="Katalog nadrzÄ™dny")
    apply_p.add_argument("--dry-run", action="store_true", help="Tylko podglÄ…d bez wprowadzania zmian")

    # sop validate-spec
    val_p = subparsers.add_parser("validate-spec", help="Waliduj plik specyfikacji SOP")
    val_p.add_argument("file", help="ĹšcieĹĽka do pliku specyfikacji (YAML/JSON)")

    args = parser.parse_args()

    if args.command == "scan":
        scanner = RepositoryScanner(args.root)
        report = scanner.scan_all()
        summary = SOPDiffer.calculate_drift_summary(report.findings)
        if args.json:
            print(json.dumps({
                "timestamp": report.timestamp,
                "scanned_count": report.scanned_repos_count,
                "clean_count": report.clean_repos_count,
                "drifts_summary": summary,
                "findings": [{"repo": f.repo_name, "rule": f.rule_id, "severity": f.severity, "msg": f.message} for f in report.findings]
            }, indent=2, ensure_ascii=False))
        else:
            print(f"=== SOP Repository Scan Report ({report.timestamp}) ===")
            print(f"Przeskanowano repozytoriĂłw: {report.scanned_repos_count} (Czyste: {report.clean_repos_count})")
            print(f"Wykryto rozbieĹĽnoĹ›ci: {len(report.findings)}")
            for f in report.findings:
                print(f"  [{f.severity}] {f.repo_name}: {f.rule_id} - {f.message}")

    elif args.command == "apply":
        scanner = RepositoryScanner(args.root)
        report = scanner.scan_all()
        result = SOPPatcher.apply_all(report.findings, dry_run=args.dry_run)
        print(f"=== SOP Auto-Patcher ===")
        print(f"Zaaplikowano poprawek: {result['applied']}")
        print(f"PominiÄ™to (wymaga manualnej interwencji): {result['skipped']}")

    elif args.command == "validate-spec":
        if not os.path.isfile(args.file):
            print(f"BĹ‚Ä…d: Plik '{args.file}' nie istnieje.", file=sys.stderr)
            sys.exit(1)
        import yaml
        with open(args.file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        is_valid, errors = SOPValidator.validate_dict(data)
        if is_valid:
            print(f"SUKCES: Specyfikacja '{args.file}' jest w 100% poprawna.")
        else:
            print(f"BĹÄ„D walidacji specyfikacji '{args.file}':", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
