---
phase: 1
slug: core-publication-surface
status: partial
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-03
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | npm scripts (Astro build + route smoke checks) |
| **Config file** | `site/package.json` |
| **Quick run command** | `npm --prefix site run build` |
| **Full suite command** | `npm --prefix site run build && npm --prefix site run verify:phase1` |
| **Estimated runtime** | ~45 seconds |

---

## Sampling Rate

- **After every task commit:** Run `npm --prefix site run build`
- **After every plan wave:** Run `npm --prefix site run build && npm --prefix site run verify:phase1`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | PUBL-01,PUBL-02,PUBL-03,PUBL-04 | build | `npm --prefix site run build` | ✅ | ✅ green |
| 01-01-02 | 01 | 1 | PUBL-01,PUBL-02,PUBL-03,PUBL-04 | build | `npm --prefix site run build` | ✅ | ✅ green |
| 01-01-03 | 01 | 1 | PUBL-01,PUBL-02,PUBL-03,PUBL-04 | integration | `npm --prefix site run verify:phase1` | ✅ | ✅ green |
| 01-02-01 | 02 | 2 | PUBL-01 | integration | `npm --prefix site run verify:phase1 -- --route=/` | ✅ | ✅ green |
| 01-02-02 | 02 | 2 | PUBL-02 | integration | `npm --prefix site run verify:phase1 -- --route-prefix=/syntheses/` | ✅ | ✅ green |
| 01-03-01 | 03 | 2 | PUBL-03,PUBL-04 | integration | `npm --prefix site run verify:phase1 -- --route=/featured --route=/methodology` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure can validate this phase through build and route smoke checks; no dedicated test framework bootstrap required.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Homepage lists every approved synthesis and excludes drafts | PUBL-01 | Existing automation checks route existence only; user chose manual-only instead of generating behavior assertions | Run `npm --prefix site run build`; open `site/dist/scipop/index.html`; confirm one card/link per approved synthesis slug in `content/syntheses/*.md` and no draft entries are listed |
| Each approved synthesis detail page renders expected metadata and markdown content | PUBL-02 | Route smoke checks prove page presence but not page content fidelity; user chose manual-only | Build site, then inspect each `site/dist/scipop/syntheses/*/index.html`; verify title, cluster id, reviewed date, and representative body text from source markdown are present |
| Featured page content is rendered from featured markdown source | PUBL-03 | Automated check validates `/featured` route exists but not content correctness; user chose manual-only | Build site and inspect `site/dist/scipop/featured/index.html`; verify title, summary, reviewed date, and body content from `content/featured/research-group.md` |
| Methodology page content is rendered from methodology markdown source | PUBL-04 | Automated check validates `/methodology` route exists but not rendered copy; user chose manual-only | Build site and inspect `site/dist/scipop/methodology/index.html`; verify heading/body reflect `content/pages/methodology.md` |
| Public readability and link clarity across representative pages | PUBL-01,PUBL-02,PUBL-03,PUBL-04 | Visual quality and copy clarity require human judgment | Run local preview, open `/`, `/featured`, `/methodology`, and one `/syntheses/{slug}` page; confirm links and headings are understandable for general readers |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending

## Validation Audit 2026-04-03

| Metric | Count |
|--------|-------|
| Gaps found | 4 |
| Resolved | 0 |
| Escalated | 4 |

- Gap disposition: user selected "Skip - mark manual-only" during Nyquist audit.
