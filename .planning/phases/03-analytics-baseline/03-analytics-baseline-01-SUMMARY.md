---
phase: 03-analytics-baseline
plan: 01
subsystem: infra
tags: [analytics, ga4, astro, telemetry]
requires:
  - phase: 02-readability-accessibility-baseline
    provides: shared BaseLayout route wrapper and verification conventions
provides:
  - Production-gated GA environment contract for Astro runtime env variables
  - Global GA bootstrap/pageview config in BaseLayout for required public routes
affects: [analytics baseline verification, production deployment configuration]
tech-stack:
  added: []
  patterns:
    - Production-only telemetry gate via PUBLIC_SITE_ENV
    - Build-time configuration assertion for required measurement ID
key-files:
  created:
    - site/src/lib/analytics.ts
  modified:
    - site/src/layouts/BaseLayout.astro
key-decisions:
  - "Centralized telemetry env parsing and production guard logic in site/src/lib/analytics.ts for reuse and consistency."
  - "Injected GA loader/config only when PUBLIC_SITE_ENV resolves to production, with canonical pathname and privacy flags locked in BaseLayout."
patterns-established:
  - "Analytics env contract: expose getter + enablement + assert helpers to keep runtime checks deterministic."
  - "Global pageview wiring in shared layout instead of per-route script duplication."
requirements-completed: [ANLT-01]
duration: 1m 29s
completed: 2026-04-03
---

# Phase 3 Plan 1: Analytics Baseline Summary

**Production-only GA4 bootstrap now ships from BaseLayout with canonical pathname pageviews and enforced measurement-ID configuration in production builds.**

## Performance

- **Duration:** 1m 29s
- **Started:** 2026-04-03T18:44:09Z
- **Completed:** 2026-04-03T18:45:38Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Added a dedicated analytics env module with normalized env parsing and a hard production config assertion.
- Wired asynchronous GA loader + inline `gtag('config', ...)` pageview bootstrap into the shared layout.
- Locked privacy-safe telemetry defaults (`anonymize_ip`, disabled google/ad personalization signals) and canonical `window.location.pathname` page path.

## Task Commits

Each task was committed atomically:

1. **Task 1: Create analytics environment contract and production guard helpers** - `3d7bf82` (feat)
2. **Task 2: Wire GA async snippet and privacy-safe pageview config in BaseLayout** - `1bbf4cb` (feat)

**Plan metadata:** _pending final docs commit_

## Files Created/Modified
- `site/src/lib/analytics.ts` - Exposes production telemetry constants/helpers and throws on missing `PUBLIC_GA_MEASUREMENT_ID` in production.
- `site/src/layouts/BaseLayout.astro` - Adds production-gated GA loader/bootstrap with required privacy and canonical page-path config.

## Decisions Made
- Centralized all telemetry env contract behavior in a standalone helper module to avoid duplicating env parsing and production guard logic in layout code.
- Kept pageview emission strictly page-load only with no history/hash listeners to preserve Phase 3 scope and avoid SPA overreach.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

External services require manual configuration:
- Set `PUBLIC_GA_MEASUREMENT_ID` from GA4 Web stream settings.
- Set `PUBLIC_SITE_ENV=production` for production deployment variables.

## Next Phase Readiness

- Baseline GA wiring is in place and production-safe for all BaseLayout-backed public routes.
- Ready for Phase 3 follow-up validation work (artifact-level telemetry verifier + manual GA console checks).

## Self-Check

PASSED

- FOUND: `.planning/phases/03-analytics-baseline/03-analytics-baseline-01-SUMMARY.md`
- FOUND: `site/src/lib/analytics.ts`
- FOUND: `site/src/layouts/BaseLayout.astro`
- FOUND commit: `3d7bf82`
- FOUND commit: `1bbf4cb`

---
*Phase: 03-analytics-baseline*
*Completed: 2026-04-03*
