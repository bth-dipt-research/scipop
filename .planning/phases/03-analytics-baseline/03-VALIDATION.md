---
phase: 03
slug: analytics-baseline
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-04-03
---

# Phase 03 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Node script verification + Astro build checks |
| **Config file** | none — script-based verification in `site/scripts/*.mjs` |
| **Quick run command** | `npm --prefix site run build && npm --prefix site run verify:phase3` |
| **Full suite command** | `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2 && npm --prefix site run verify:phase3` |
| **Estimated runtime** | ~25 seconds |

---

## Sampling Rate

- **After every task commit:** Run `npm --prefix site run build && npm --prefix site run verify:phase3`
- **After every plan wave:** Run `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2 && npm --prefix site run verify:phase3`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | ANLT-01 | build/static | `npm --prefix site run build` | ✅ | ⬜ pending |
| 03-01-02 | 01 | 1 | ANLT-01 | integration/static | `npm --prefix site run build && npm --prefix site run verify:phase1` | ✅ | ⬜ pending |
| 03-02-01 | 02 | 2 | ANLT-01 | verification script | `npm --prefix site run build && npm --prefix site run verify:phase3` | ✅ | ⬜ pending |
| 03-02-02 | 02 | 2 | ANLT-01 | regression | `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2 && npm --prefix site run verify:phase3` | ✅ | ⬜ pending |
| 03-02-03 | 02 | 2 | ANLT-01 | docs consistency | `rg "Realtime verification checklist|24-hour standard report" .planning/phases/03-analytics-baseline/03-GA-VERIFICATION-CHECKLIST.md` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Realtime telemetry visibility in GA UI | ANLT-01 | Requires access to GA property dashboard and live traffic panel | Visit production routes, open GA Realtime view, record route path + timestamp evidence in checklist file. |
| Standard-report visibility within 24h | ANLT-01 | Requires delayed aggregation in GA standard reports | Return within 24h, verify tested routes appear in standard reports, capture screenshot/notes evidence in checklist file. |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 60s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
