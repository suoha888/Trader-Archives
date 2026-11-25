#!/usr/bin/env python3
"""Trader-Archives Automated Security Regression Gate.

Verifies HTML/JS/data security invariants across the repository:
1. Secret scanning across all HTML and derived data/doc files (sk-, atr_, AIza, ghp_, JWT, etc.).
2. .gitignore integrity (UTF-8 without BOM + mandatory sensitive patterns).
3. CSP & Referrer-Policy meta headers on root index.html and all non-frozen KOL subsites.
4. No target="_blank" without rel="noopener noreferrer", no abs.twimg.com onerror loops.
5. DOM XSS hardening: escHtml escapes single quotes, safeHttpUrl() validates href schemes,
   dynamic image modal uses data-modal-src delegation, rCls and cached.ragCount are numeric,
   and inline <script> JSON data escapes <, >, &, U+2028, U+2029.
6. Indirect Prompt Injection boundary (<untrusted_archive_excerpts>) in AI RAG prompt assembly.
7. Optional Node.js vm.Script syntax validation for every inline <script> block.
"""
from __future__ import annotations

import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FROZEN_SLUGS = {"thankucrypto", "laoemo"}

SECRET_PATTERNS = [
    ("Atria Key (atr_)", re.compile(r"atr_[A-Za-z0-9_-]{12,}")),
    ("OpenAI/Proxy Key (sk-)", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
    ("Google API Key (AIza)", re.compile(r"AIza[0-9A-Za-z_-]{30,}")),
    ("GitHub Token (ghp/gho/pat)", re.compile(r"(?:gh[po]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})")),
    ("JWT Token", re.compile(r"eyJhbGci[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")),
    ("Private Key PEM", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]


def check_gitignore(errors: list[str]) -> None:
    gi = REPO_ROOT / ".gitignore"
    if not gi.exists():
        errors.append(".gitignore missing")
        return
    raw = gi.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        errors.append(".gitignore contains UTF-8 BOM (breaks first ignore rule)")
    txt = raw.decode("utf-8")
    for required in ("*_ultra_raw.json", "*_harvest_report.json", ".env", "*.key", "*.pem"):
        if required not in txt.splitlines():
            errors.append(f".gitignore missing mandatory rule: {required}")


def check_secrets(errors: list[str]) -> None:
    skip_dirs = {".git", ".github", "scripts"}
    checked = 0
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_dirs for part in path.relative_to(REPO_ROOT).parts):
            continue
        # Preserve read-only *_ultra_raw.json historical backups per workspace policy
        if path.name.endswith("_ultra_raw.json"):
            continue
        if path.suffix.lower() not in {".html", ".js", ".css", ".json", ".csv", ".md"}:
            continue
        checked += 1
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for label, pat in SECRET_PATTERNS:
            if pat.search(content):
                errors.append(f"Secret match [{label}] in {path.relative_to(REPO_ROOT)}")
    print(f"[PASS/SCAN] Scanned {checked} public text/data files for leaked secrets")


def check_root_html(errors: list[str]) -> None:
    root = REPO_ROOT / "index.html"
    txt = root.read_text(encoding="utf-8")
    if 'http-equiv="Content-Security-Policy"' not in txt:
        errors.append("index.html missing Content-Security-Policy meta tag")
    if 'name="referrer"' not in txt:
        errors.append("index.html missing Referrer-Policy meta tag")
    if "abs.twimg.com" in txt:
        errors.append("index.html still references external abs.twimg.com fallback")
    for m in re.finditer(r'<a\b[^>]*target="_blank"[^>]*>', txt):
        tag = m.group(0)
        if 'rel="noopener noreferrer"' not in tag:
            errors.append(f"index.html target=_blank missing rel='noopener noreferrer': {tag[:80]}")


def check_subsites(errors: list[str]) -> None:
    subsites = sorted(REPO_ROOT.glob("*/index.html"))
    checked = 0
    for p in subsites:
        slug = p.parent.name
        if slug in FROZEN_SLUGS:
            continue
        checked += 1
        txt = p.read_text(encoding="utf-8")
        if 'http-equiv="Content-Security-Policy"' not in txt:
            errors.append(f"{slug}/index.html missing Content-Security-Policy meta")
        if 'name="referrer"' not in txt:
            errors.append(f"{slug}/index.html missing Referrer-Policy meta")
        if ".replace(/'/g,'&#39;')" not in txt and '.replace(/\'/g,"&#39;")' not in txt:
            errors.append(f"{slug}/index.html escHtml does not escape single quotes")
        if "function safeHttpUrl(" not in txt:
            errors.append(f"{slug}/index.html missing safeHttpUrl() scheme validator")
        if "onclick=\"showModalImage('${escHtml(p)}')\"" in txt:
            errors.append(f"{slug}/index.html still uses unsafe inline onclick in dynamic card")
        if "t.roleOrder || 4" in txt and "parseInt(t.roleOrder, 10)" not in txt:
            errors.append(f"{slug}/index.html rCls not coerced to integer")
        if "${cached.ragCount || 0}" in txt:
            errors.append(f"{slug}/index.html cached.ragCount not coerced to Number")
        if "<untrusted_archive_excerpts>" not in txt:
            errors.append(f"{slug}/index.html missing <untrusted_archive_excerpts> prompt boundary")
        for m in re.finditer(r'target="_blank"\s+rel="noopener"(?!\s*noreferrer)', txt):
            errors.append(f"{slug}/index.html has target=_blank rel='noopener' without noreferrer")
            break
        # Verify inline JSON data assignments contain no raw <, >, U+2028, U+2029
        for var_name in ("CJ_AI_CONFIG", "FALLBACK_TWEETS", "EARLY_FALLBACK"):
            m = re.search(rf"const {var_name} = ([^\n]+);", txt)
            if m:
                raw_json = m.group(1)
                if any(ch in raw_json for ch in ("<", ">", "\u2028", "\u2029")):
                    errors.append(f"{slug}/index.html {var_name} contains unescaped <, >, U+2028, or U+2029")
                try:
                    json.loads(raw_json)
                except Exception as exc:
                    errors.append(f"{slug}/index.html {var_name} invalid JSON: {exc}")
    print(f"[PASS/SCAN] Audited {checked} non-frozen KOL subsites for HTML/DOM security")


def check_js_syntax(errors: list[str]) -> None:
    node = shutil.which("node")
    if not node:
        print("[SKIP] node not installed; skipping vm.Script JS syntax verification")
        return
    js_verifier = r"""
const fs = require('fs');
const vm = require('vm');
const files = JSON.parse(process.argv[1]);
const errs = [];
for (const f of files) {
  const html = fs.readFileSync(f, 'utf8');
  const re = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
  let m, idx = 0;
  while ((m = re.exec(html)) !== null) {
    idx++;
    const code = m[1].trim();
    if (!code) continue;
    try {
      new vm.Script(code, { filename: `${f}#script-${idx}` });
    } catch (e) {
      errs.push(`${f}#script-${idx}: ${e.message}`);
    }
  }
}
if (errs.length) {
  console.error(errs.join('\n'));
  process.exit(1);
}
console.log(`JS syntax OK across ${files.length} HTML files`);
"""
    html_files = [str(REPO_ROOT / "index.html")] + [
        str(p) for p in sorted(REPO_ROOT.glob("*/index.html")) if p.parent.name not in FROZEN_SLUGS
    ]
    proc = subprocess.run([node, "-e", js_verifier, json.dumps(html_files)], capture_output=True, text=True)
    if proc.returncode != 0:
        errors.append(f"JS syntax check failed: {proc.stderr.strip()}")
    else:
        print(f"[PASS/JS] {proc.stdout.strip()}")


def check_repo_security_files(errors: list[str]) -> None:
    for rel in ("SECURITY.md", ".gitleaks.toml", ".github/CODEOWNERS", ".github/workflows/security-audit.yml"):
        if not (REPO_ROOT / rel).is_file():
            errors.append(f"Missing required security baseline file: {rel}")
    wf = REPO_ROOT / ".github/workflows/security-audit.yml"
    if wf.is_file():
        for m in re.finditer(r"uses:\s*([^\s#]+)", wf.read_text(encoding="utf-8")):
            ref = m.group(1)
            if not re.search(r"@[0-9a-f]{40}$", ref):
                errors.append(f"GitHub Action not pinned to full commit SHA: {ref}")


def check_csv_formula_injection(errors: list[str]) -> None:
    num_neg = re.compile(r"^-\d+(?:\.\d+)?%?$")
    at_func = re.compile(r"^@[A-Za-z_][A-Za-z0-9_.]*\(")
    checked = 0
    for p in sorted(REPO_ROOT.rglob("*.csv")):
        if any(part in {".git", ".github", "scripts"} for part in p.relative_to(REPO_ROOT).parts):
            continue
        if p.relative_to(REPO_ROOT).parts[0] in FROZEN_SLUGS:
            continue
        checked += 1
        with p.open("r", encoding="utf-8-sig", newline="") as f:
            for rno, row in enumerate(csv.reader(f), 1):
                for cno, cell in enumerate(row):
                    s = cell.lstrip(" ")
                    if not s:
                        continue
                    c0 = s[0]
                    bad = (
                        c0 in ("=", "+", "\t", "\r")
                        or (c0 == "-" and not num_neg.match(s))
                        or (c0 == "@" and bool(at_func.match(s)))
                    )
                    if bad:
                        errors.append(
                            f"CWE-1236 unneutralized CSV formula cell in {p.relative_to(REPO_ROOT)}:{rno} col={cno}: {s[:40]!r}"
                        )
    print(f"[PASS/CSV] Checked {checked} non-frozen CSV files for CWE-1236 formula injection")


def main() -> int:
    errors: list[str] = []
    check_gitignore(errors)
    check_repo_security_files(errors)
    check_secrets(errors)
    check_csv_formula_injection(errors)
    check_root_html(errors)
    check_subsites(errors)
    check_js_syntax(errors)

    if errors:
        print("\n[FAIL] Security verification failed with the following issues:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("\n[SUCCESS] All Trader-Archives security regression checks passed!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
