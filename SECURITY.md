# Security Policy

## Scope & Architecture

`Trader-Archives` is a public static archive hosted on GitHub Pages (`https://suoha888.github.io/Trader-Archives/`).
All KOL subsites are read-only static HTML/JSON/CSV archives; AI Q&A traffic is proxied through a dedicated Vercel Edge Function (`https://trader-archives-ai-gateway.vercel.app/api/chat`) so that zero upstream API keys are ever shipped to the browser.

## Reporting a Vulnerability

If you discover a security vulnerability, exposed secret, XSS vector, or abuse issue affecting `Trader-Archives` or its AI Mentor gateway:

1. **Do NOT open a public GitHub Issue** containing live credentials, exploit payloads, or sensitive details.
2. Report privately via GitHub Security Advisories (**Security → Advisories → Report a vulnerability**) on [`suoha888/Trader-Archives`](https://github.com/suoha888/Trader-Archives/security/advisories/new).
3. Include affected URL/file path, reproduction steps, and potential impact. We aim to acknowledge reports within 48 hours and ship remediations promptly.

## Security Controls Enforced in CI

Every pull request and push to `main` runs `.github/workflows/security-audit.yml` (`scripts/security_verify.py`), enforcing:

- Zero leaked secrets (`atr_*`, `sk-*`, `AIza*`, `ghp_`/`gho_`/`github_pat_`, JWT `eyJhbGci*`, PEM private keys) across all public HTML, JSON, CSV, and Markdown files;
- Strict `<meta http-equiv="Content-Security-Policy">` and `<meta name="referrer" content="strict-origin-when-cross-origin">` headers;
- DOM XSS defenses (`escHtml` single-quote escaping, `safeHttpUrl()` protocol allowlisting, `data-*` event delegation without inline `onclick` string interpolation, full `\u003c`/`\u003e`/`\u0026`/`\u2028`/`\u2029` inline JSON escaping, numeric coercion on `roleOrder` and `cached.ragCount`);
- Indirect RAG Prompt Injection isolation (`<untrusted_archive_excerpts>` delimiters + server-side prompt guard & SHA-256 prompt allowlist);
- CWE-1236 CSV spreadsheet formula neutralization across public CSV datasets;
- Repository security baseline files (`SECURITY.md`, `.gitleaks.toml`, `.github/CODEOWNERS`, BOM-free `.gitignore`);
- Full `rel="noopener noreferrer"` on external `target="_blank"` links and JavaScript `vm.Script` syntax verification.

## Historical Key Rotation & Git History Remediation Playbook

> [!IMPORTANT]
> If historical credentials are ever discovered in Git history (such as legacy client-side Atria `atr_*` or `api.b.ai` `sk-*` keys removed from `HEAD` prior to the Vercel Edge Gateway migration):
>
> 1. **Revoke** all exposed keys immediately in the upstream provider dashboard (do not rely on zero remaining balance).
> 2. **Rotate** active server-side credentials (`GEMINI_API_KEY`, `AI_GATEWAY_API_KEY`, `VERCEL_TOKEN`) using dedicated, project-scoped write-only secrets with hard spend caps.
> 3. **Scrub Git History** with `git filter-repo --replace-text` (or BFG Repo-Cleaner) and force-push cleaned refs after maintainer review, then request GitHub Support purge cached dangling commit objects.
> 4. **Enable Platform Defenses**: keep GitHub Secret Scanning and Push Protection enabled on the repository.
