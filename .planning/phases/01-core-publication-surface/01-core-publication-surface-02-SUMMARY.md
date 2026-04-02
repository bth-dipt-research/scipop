---
phase: 01-core-publication-surface
plan: 02
subsystem: ui
tags: [astro, content-collections, static-routes]

# Dependency graph
requires:
  - phase: 01-01
    provides: content schemas and seeded synthesis markdown
provides:
  - Homepage cluster listing from approved synthesis collection entries
  - Dynamic synthesis detail route generation from frontmatter slugs
affects: [phase-1-plan-03, phase-2]

# Tech tracking
tech-stack:
  added: []
  patterns: [approved-content filtering, getStaticPaths from content collection]

key-files:
  created:
    - site/src/components/ClusterCard.astro
  modified:
    - site/src/pages/index.astro
    - site/src/pages/syntheses/[slug].astro
    - site/scripts/verify-phase1.mjs

key-decisions:
  - "Homepage card list is rendered only from syntheses with `status: approved`."
  - "Detail routes are generated from collection slugs via getStaticPaths instead of hardcoded paths."

patterns-established:
  - "Filter + sort collection entries before rendering homepage destination links."
  - "Scope verification commands with route and route-prefix CLI filters."

requirements-completed: [PUBL-01, PUBL-02]

# Metrics
duration: 3min
completed: 2026-04-02
---

# Phase 1 Plan 02: Core Publication Surface Summary

**Content-driven homepage and synthesis detail pages now publish stable destination URLs directly from approved markdown entries.**

## Performance

- **Duration:** 3 min
- **Started:** 2026-04-02T22:24:00Z
- **Completed:** 2026-04-02T22:26:38Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Implemented homepage listing that loads syntheses from content collections, filters to approved entries, sorts by order, and links each card to `/syntheses/{slug}`.
- Replaced hardcoded synthesis route generation with dynamic `getStaticPaths` from approved collection entries and rendered metadata + markdown content.
- Corrected route-verifier CLI parsing so `--route=` and `--route-prefix=` arguments work reliably for scoped verification.

## Task Commits

1. **Task 1: Build homepage cluster listing from approved syntheses** - `d67a225` (feat)
2. **Task 2: Generate stable detail routes for each approved synthesis** - `ebaecb1` (feat)

## Files Created/Modified
- `site/src/components/ClusterCard.astro` - reusable card component for homepage synthesis destinations.
- `site/src/pages/index.astro` - homepage collection query, approved filtering, ordering, and card rendering.
- `site/src/pages/syntheses/[slug].astro` - dynamic route generation and synthesis content rendering.
- `site/scripts/verify-phase1.mjs` - robust CLI flag parsing and route-prefix filtering behavior.

## Decisions Made
- Kept destination listing strictly tied to approved content status to avoid exposing draft entries.
- Used collection-driven route generation to preserve stable URL mapping from markdown slugs.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed verifier flag parsing for npm argument style**
- **Found during:** Task 2
- **Issue:** `verify:phase1` ignored `--route=` and `--route-prefix=` forms passed by npm, causing unscoped checks.
- **Fix:** Added support for both `--flag value` and `--flag=value` parsing and corrected prefix-only filtering logic.
- **Files modified:** `site/scripts/verify-phase1.mjs`
- **Verification:** `npm --prefix site run verify:phase1 -- --route-prefix=/syntheses/` reported `Verified 2 route(s).`
- **Committed in:** `ebaecb1`

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Improved correctness of verification scope without expanding plan scope.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Plan 03 can wire featured and methodology routes to content collections on the same rendering pattern.

## Self-Check: PASSED
