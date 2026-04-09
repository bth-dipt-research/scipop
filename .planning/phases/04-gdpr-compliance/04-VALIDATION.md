---
phase: 04
slug: gdpr-compliance
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-04-09
---

# Phase 04 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | node script checks + Astro build |
| **Config file** | none — existing phase verifier pattern |
| **Quick run command** | `npm --prefix site run build && node site/scripts/verify-phase4.mjs` |
| **Full suite command** | `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2 && npm --prefix site run verify:phase3 && npm --prefix site run verify:phase4` |
| **Estimated runtime** | ~45 seconds |

---

## Sampling Rate

- **After every task commit:** Run `npm --prefix site run build && node site/scripts/verify-phase4.mjs`
- **After every plan wave:** Run `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2 && npm --prefix site run verify:phase3 && npm --prefix site run verify:phase4`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | PRIV-01 | integration | `npm --prefix site run build && node site/scripts/verify-phase4.mjs` | ✅ | ⬜ pending |
| 04-01-02 | 01 | 1 | PRIV-02 | integration | `npm --prefix site run build && node site/scripts/verify-phase4.mjs` | ✅ | ⬜ pending |
| 04-01-03 | 01 | 1 | PRIV-03 | integration | `npm --prefix site run build && node site/scripts/verify-phase4.mjs` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Banner appears on first visit and user can interact with accept/reject controls | PRIV-01 | Visual and interaction flow cannot be fully asserted by static artifact grep alone | `npm --prefix site run dev`, open site in a private window, confirm bottom banner appears and actions are clickable |
| Footer privacy settings link re-opens consent controls and success message appears after change | PRIV-02 | Re-open and immediate feedback involve runtime interaction state | Open any route, click footer privacy link, change consent, verify inline success text renders without reload |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 60s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
