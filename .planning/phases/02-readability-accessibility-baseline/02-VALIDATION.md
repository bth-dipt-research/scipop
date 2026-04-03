---
phase: 2
slug: readability-accessibility-baseline
status: draft
nyquist_compliant: false
wave_0_complete: true
created: 2026-04-03
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | other (Astro build + Node verification scripts) |
| **Config file** | `site/package.json` |
| **Quick run command** | `npm --prefix site run build` |
| **Full suite command** | `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2` |
| **Estimated runtime** | ~25 seconds |

---

## Sampling Rate

- **After every task commit:** Run `npm --prefix site run build`
- **After every plan wave:** Run `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | PUBL-05 | integration | `npm --prefix site run build && npm --prefix site run verify:phase2 -- --check=disclaimers` | ✅ | ⬜ pending |
| 02-01-02 | 01 | 1 | PUBL-05 | integration | `npm --prefix site run build && npm --prefix site run verify:phase2 -- --check=disclaimers` | ✅ | ⬜ pending |
| 02-02-01 | 02 | 2 | PUBL-06 | integration | `npm --prefix site run build` | ✅ | ⬜ pending |
| 02-02-02 | 02 | 2 | PUBL-06 | integration | `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Mobile menu opens/closes and remains keyboard-usable on a real viewport | PUBL-06 | Responsive interaction quality needs visual/interaction confirmation | `npm --prefix site run dev`, test at 390px width: open menu with button, Tab through links, activate link and confirm menu closes |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
