import os
import re
import json
from typing import List, Dict, Any, Optional
from .models import DriftFinding, ScanReport

class RepositoryScanner:
    def __init__(self, root_dir: str):
        self.root_dir = os.path.abspath(root_dir)

    def scan_repository(self, repo_path: str) -> List[DriftFinding]:
        findings = []
        repo_name = os.path.basename(repo_path)

        if not os.path.isdir(os.path.join(repo_path, ".git")):
            return findings

        # Rule 1: Sprawdzenie obecności governance baseline
        gov_dir = os.path.join(repo_path, ".governance")
        if not os.path.isdir(gov_dir):
            findings.append(DriftFinding(
                repo_name=repo_name,
                rule_id="SOP-GOV-001",
                severity="ERROR",
                message=f"Brak katalogu .governance w repozytorium {repo_name}",
                remediation_action="Zainstaluj baseline wellmanifest/new-project za pomoca create_adoption_lock",
                target_path=gov_dir,
                auto_fixable=True
            ))

        # Rule 2: Sprawdzenie obecności .githooks/pre-commit
        pre_commit_hook = os.path.join(repo_path, ".githooks", "pre-commit")
        if not os.path.isfile(pre_commit_hook):
            findings.append(DriftFinding(
                repo_name=repo_name,
                rule_id="SOP-HOOK-001",
                severity="WARNING",
                message=f"Brak aktywnego githooka pre-commit w {repo_name}",
                remediation_action="Zainstaluj standardowy .githooks/pre-commit z wellmanifest/new-project",
                target_path=pre_commit_hook,
                auto_fixable=True
            ))

        # Rule 3: Sprawdzenie formatu ticketów pod kątem daty w nazwie lub nagłówku
        project_dir = os.path.join(repo_path, "project")
        if os.path.isdir(project_dir):
            for item in os.listdir(project_dir):
                ticket_path = os.path.join(project_dir, item)
                if os.path.isdir(ticket_path) and re.match(r"^ticket-[0-9]{3}$", item):
                    readme_file = os.path.join(ticket_path, "README.md")
                    if os.path.isfile(readme_file):
                        try:
                            with open(readme_file, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()
                            # Sprawdź czy ticket zawiera pole Created z datą YYYY-MM-DD
                            if not re.search(r"\*\*Created\*\*:\s*[0-9]{4}-[0-9]{2}-[0-9]{2}", content):
                                findings.append(DriftFinding(
                                    repo_name=repo_name,
                                    rule_id="SOP-TICKET-DATE-001",
                                    severity="WARNING",
                                    message=f"Ticket {item} w repozytorium {repo_name} nie zawiera wymaganej daty utworzenia (YYYY-MM-DD)",
                                    remediation_action="Dodaj pole Created: YYYY-MM-DD do README ticketu oraz zaktualizuj wpis w TICKETS.md",
                                    target_path=readme_file,
                                    auto_fixable=True
                                ))
                        except Exception:
                            pass

        # Rule 4: Sprawdzenie obecności plików agent hosts (AGENTS.md, CLAUDE.md, GEMINI.md)
        for host_file in ["AGENTS.md", "CLAUDE.md", "GEMINI.md"]:
            host_path = os.path.join(repo_path, host_file)
            if not os.path.isfile(host_path):
                findings.append(DriftFinding(
                    repo_name=repo_name,
                    rule_id="SOP-AGENT-HOST-001",
                    severity="WARNING",
                    message=f"Brak pliku instrukcji agenta {host_file} w {repo_name}",
                    remediation_action=f"Wygeneruj {host_file} z szablonu wellmanifest/new-project",
                    target_path=host_path,
                    auto_fixable=True
                ))

        return findings

    def scan_all(self, target_dirs: Optional[List[str]] = None) -> ScanReport:
        from datetime import datetime
        all_findings = []
        scanned_count = 0
        clean_count = 0

        paths_to_scan = target_dirs if target_dirs else [self.root_dir]
        for base in paths_to_scan:
            if not os.path.exists(base):
                continue
            for item in os.listdir(base):
                sub_path = os.path.join(base, item)
                if os.path.isdir(sub_path):
                    scanned_count += 1
                    findings = self.scan_repository(sub_path)
                    if findings:
                        all_findings.extend(findings)
                    else:
                        clean_count += 1

        return ScanReport(
            timestamp=datetime.now().isoformat(),
            scanned_repos_count=scanned_count,
            findings=all_findings,
            clean_repos_count=clean_count
        )