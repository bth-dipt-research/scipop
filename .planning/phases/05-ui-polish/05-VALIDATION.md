---
phase: 05
slug: ui-polish
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-04-10
---

# Phase 05 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Astro build + node script verification |
| **Config file** | none - script-based checks in `site/scripts/*.mjs` |
| **Quick run command** | `npm --prefix site run build && npm --prefix site run verify:phase5` |
| **Full suite command** | `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2 && npm --prefix site run verify:phase3 && npm --prefix site run verify:phase4 && npm --prefix site run verify:phase5` |
| **Estimated runtime** | ~60 seconds |

---

## Sampling Rate

- **After every task commit:** Run `npm --prefix site run build && npm --prefix site run verify:phase5`
- **After every plan wave:** Run full suite (`verify:phase1` through `verify:phase5`)
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | UIP-01 | build/regression | `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase4` | ✅ | ⬜ pending |
| 05-01-02 | 01 | 1 | UIP-03 | route/IA | `npm --prefix site run build` | ✅ | ⬜ pending |
| 05-02-01 | 02 | 2 | UIP-03 | static/component | `npm --prefix site run build` | ✅ | ⬜ pending |
| 05-02-02 | 02 | 2 | UIP-03 | navigation/regression | `npm --prefix site run build && npm --prefix site run verify:phase1` | ✅ | ⬜ pending |
| 05-03-01 | 03 | 2 | UIP-02 | schema/content | `npm --prefix site run build` | ✅ | ⬜ pending |
| 05-03-02 | 03 | 2 | UIP-01, UIP-02, UIP-03 | phase verifier | `npm --prefix site run build && npm --prefix site run verify:phase5` | ✅ | ⬜ pending |

*Status: ⬜ pending - ✅ green - ❌ red - ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Desktop image-map hotspots are visually clear and usable | UIP-03 | Requires visual review of hit-area quality and readability at real breakpoints | Run `npm --prefix site run dev`, open homepage at desktop/tablet widths, tab through hotspot links and verify visible focus + clear labels |
| Mobile fallback list/cards are easy to use | UIP-03 | Runtime viewport behavior and touch ergonomics are hard to assert from static markers | Open homepage under 768px width, confirm map is replaced by fallback links/cards and all entries are reachable |
| Editor profile block wraps/stack behavior matches design intent | UIP-02 | Responsive layout quality is visual and cannot be fully grep-verified | Open a synthesis page on desktop and mobile widths; verify top-left wrap on desktop and stacked profile block on mobile |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 60s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
