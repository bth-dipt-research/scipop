---
phase: 01-core-publication-surface
plan: 01
subsystem: ui
tags: [astro, markdown, github-pages, content-collections]

# Dependency graph
requires:
  - phase: none
    provides: first phase bootstrap
provides:
  - Astro static site scaffold in `site/`
  - Markdown content contracts for syntheses, featured, and methodology pages
  - Automated route smoke verification command for Phase 1 destinations
affects: [phase-1-plan-02, phase-1-plan-03, phase-2]

# Tech tracking
tech-stack:
  added: [astro]
  patterns: [contract-validated markdown collections, static route smoke verification]

key-files:
  created:
    - site/package.json
    - site/astro.config.mjs
    - site/src/content.config.ts
    - site/scripts/verify-phase1.mjs
    - content/syntheses/cluster-engineering-practices.md
    - content/syntheses/cluster-ai-and-software-engineering.md
    - content/featured/research-group.md
    - content/pages/methodology.md
  modified:
    - site/package.json

key-decisions:
  - "Use Astro static output with GitHub Pages base path `/scipop` in config."
  - "Verify required Phase 1 routes with a filesystem-based `verify:phase1` script after each build."

patterns-established:
  - "Content collection schemas enforce required metadata for publication entries."
  - "Phase-level verification checks generated route artifacts, not only build exit code."

requirements-completed: [PUBL-01, PUBL-02, PUBL-03, PUBL-04]

# Metrics
duration: 8min
completed: 2026-04-02
---

# Phase 1 Plan 01: Core Publication Surface Summary

**Astro static publication foundation with typed markdown collections and deterministic route smoke verification for all Phase 1 destinations.**

## Performance

- **Duration:** 8 min
- **Started:** 2026-04-02T22:14:00Z
- **Completed:** 2026-04-02T22:22:27Z
- **Tasks:** 3
- **Files modified:** 16

## Accomplishments
- Bootstrapped a Node 22-compatible Astro static project in `site/` with shared layout navigation for home, featured, and methodology destinations.
- Added markdown content contracts and seeded approved synthesis, featured, and methodology source files under top-level `content/`.
- Added `verify:phase1` route smoke checker that validates required destination pages in build output.

## Task Commits

1. **Task 1: Bootstrap Astro static publication app** - `fced4f5` (feat)
2. **Task 2: Define markdown contracts and seed publication content** - `95a1fa8` (feat)
3. **Task 3: Add automated route smoke verification for Phase 1 destinations** - `4790bc2` (feat)

## Files Created/Modified
- `site/package.json` - project scripts and `verify:phase1` command.
- `site/astro.config.mjs` - static output and GitHub Pages `site`/`base` configuration.
- `site/src/layouts/BaseLayout.astro` - shared layout and primary navigation.
- `site/src/content.config.ts` - Astro content collection contracts with required fields.
- `content/syntheses/*.md` - approved synthesis markdown sources with slugs and ordering.
- `content/featured/research-group.md` - featured synthesis markdown source.
- `content/pages/methodology.md` - methodology page markdown source.
- `site/scripts/verify-phase1.mjs` - route existence verification for required Phase 1 paths.

## Decisions Made
- Used content-schema validation as a hard gate for publication metadata consistency.
- Kept verification at build artifact level to provide quick feedback before deployment pipeline work.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Corrected content collection base paths**
- **Found during:** Task 2
- **Issue:** Initial collection loader paths resolved outside the repository content directory.
- **Fix:** Updated glob loader `base` paths in `site/src/content.config.ts` to `../content/*`.
- **Files modified:** `site/src/content.config.ts`
- **Verification:** `npm --prefix site run build` completed with synced collections.
- **Committed in:** `95a1fa8`

**2. [Rule 3 - Blocking] Added minimal static route files required by route verifier**
- **Found during:** Task 3
- **Issue:** Verifier contract required checking `/`, `/featured`, `/methodology`, and synthesis routes, but no pages existed yet.
- **Fix:** Added minimal route files in `site/src/pages/` so verification command could pass and enforce required paths.
- **Files modified:** `site/src/pages/index.astro`, `site/src/pages/featured/index.astro`, `site/src/pages/methodology.astro`, `site/src/pages/syntheses/[slug].astro`
- **Verification:** `npm --prefix site run build && npm --prefix site run verify:phase1` returned success.
- **Committed in:** `4790bc2`

---

**Total deviations:** 2 auto-fixed (1 bug, 1 blocking)
**Impact on plan:** Both fixes were required for correctness and executable verification; no architectural scope change.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Plan 02 can now replace minimal placeholder route implementations with content-driven homepage and synthesis detail rendering.
- Plan 03 can wire featured and methodology pages to markdown collection data.

## Self-Check: PASSED
