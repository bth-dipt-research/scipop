---
phase: 01-core-publication-surface
plan: 03
subsystem: ui
tags: [astro, markdown, verification]

# Dependency graph
requires:
  - phase: 01-01
    provides: featured/methodology markdown collections and route verifier script
provides:
  - Content-driven featured synthesis page at /featured
  - Content-driven methodology page at /methodology
  - Explicit core-route enforcement in phase route verifier
affects: [phase-2, phase-3]

# Tech tracking
tech-stack:
  added: []
  patterns: [single-entry collection rendering, explicit core-route verification]

key-files:
  created: []
  modified:
    - site/src/pages/featured/index.astro
    - site/src/pages/methodology.astro
    - site/scripts/verify-phase1.mjs

key-decisions:
  - "Render featured and methodology pages directly from markdown collection entries instead of hardcoded page copy."
  - "Treat /, /featured, and /methodology as explicit core routes in verification logic."

patterns-established:
  - "Throw explicit build-time errors when required single-entry content records are missing."
  - "Fail verification when filters produce an empty route set to avoid false-positive checks."

requirements-completed: [PUBL-03, PUBL-04]

# Metrics
duration: 3min
completed: 2026-04-02
---

# Phase 1 Plan 03: Core Publication Surface Summary

**Featured synthesis and methodology destinations now render from curated markdown content with stricter route-verification guarantees.**

## Performance

- **Duration:** 3 min
- **Started:** 2026-04-02T22:27:00Z
- **Completed:** 2026-04-02T22:29:06Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments
- Wired `/featured` to load and render the featured markdown entry, including title, summary, reviewed date, and body content.
- Wired `/methodology` to load and render methodology markdown content through the pages collection.
- Hardened route verifier defaults so core destination routes remain explicit and empty route selections fail fast.

## Task Commits

1. **Task 1: Implement featured and methodology static pages from markdown collections** - `eeeb37f` (feat)
2. **Task 2: Extend route smoke checker to enforce featured/methodology guarantees** - `3aae339` (fix)

## Files Created/Modified
- `site/src/pages/featured/index.astro` - featured collection rendering with metadata and markdown body.
- `site/src/pages/methodology.astro` - methodology page rendering from pages collection.
- `site/scripts/verify-phase1.mjs` - explicit core routes and empty-selection guard.

## Decisions Made
- Required content pages should be rendered from source markdown so editorial updates flow to public pages without template edits.
- Verification should guard against accidental no-op filtering to prevent false-positive test results.

## Deviations from Plan
None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 1 destination surface is fully content-driven and route-verified, ready for Phase 2 readability/accessibility work.

## Self-Check: PASSED
