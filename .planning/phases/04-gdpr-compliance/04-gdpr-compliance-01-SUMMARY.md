---
phase: 04-gdpr-compliance
plan: 01
subsystem: privacy
tags: [gdpr, consent, analytics, astro]
requires:
  - phase: 03-analytics-baseline
    provides: production-gated analytics bootstrap and phase verification scripts
provides:
  - Consent storage contract with shared cookie and localStorage state
  - Consent-aware analytics initialization and runtime opt-out handling
  - Dedicated privacy disclosure route and automated phase verifier
affects: [site layout runtime behavior, analytics verification workflow]
tech-stack:
  added:
    - vanilla-cookieconsent
  patterns:
    - Layout-level consent gating for static Astro routes
    - Phase verifier checks combining build artifact assertions and source guard checks
key-files:
  created:
    - site/src/lib/consent.ts
    - site/src/pages/privacy.astro
    - site/scripts/verify-phase4.mjs
  modified:
    - site/src/layouts/BaseLayout.astro
    - site/package.json
    - site/package-lock.json
    - site/scripts/verify-phase3.mjs
decisions:
  - Keep analytics bootstrap runtime-controlled behind explicit accepted consent and production mode checks.
  - Use a persistent footer privacy-settings entry that reopens the same bottom consent banner controls.
metrics:
  duration: 13m
  completed: 2026-04-09
---

# Phase 4 Plan 1: Implement consent management with library integration and consent-aware analytics behavior Summary

**Consent-gated analytics now runs only after explicit acceptance, with always-available privacy settings controls and a dedicated public disclosure page enforced by phase verification.**

## Accomplishments

- Added `site/src/lib/consent.ts` with explicit `accepted | rejected | unset` contract and mirrored cookie/localStorage persistence (`scipop_analytics_consent`).
- Updated `BaseLayout.astro` to add a bottom consent banner (Accept all / Reject all), footer privacy-settings reopen control, and inline update confirmation.
- Changed analytics bootstrap behavior so production mode still applies, but runtime initialization only occurs when consent is accepted.
- Added `/privacy` route with provider/purpose/tracked-data/change-consent/contact disclosure content.
- Added `site/scripts/verify-phase4.mjs` and `verify:phase4` script to enforce privacy route and consent marker coverage.

## Task Commits

1. `0dd9f3f` — **test(04-01): add failing test for consent storage contract**
2. `377023e` — **feat(04-01): implement consent persistence contract**
3. `78f455c` — **test(04-01): add failing tests for consent UI gating**
4. `b8af627` — **feat(04-01): implement consent banner and GA consent gate**
5. `534ed17` — **test(04-01): add failing tests for privacy route verification**
6. `1eacf8b` — **feat(04-01): add privacy disclosure route and phase verifier**

## Verification

- `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2 && npm --prefix site run verify:phase3 && npm --prefix site run verify:phase4` ✅

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Prevented false Phase 3 verification failures outside production**
- **Found during:** Final full-suite verification
- **Issue:** `verify:phase3` required GA markers in built HTML even when `PUBLIC_SITE_ENV` was not production, causing false failures after consent-based production-only gating.
- **Fix:** Updated `site/scripts/verify-phase3.mjs` to always verify route existence but enforce telemetry marker checks only when `PUBLIC_SITE_ENV=production`.
- **Files modified:** `site/scripts/verify-phase3.mjs`
- **Commit:** `1afdb57`

## Known Stubs

None.

## Self-Check: PASSED

- FOUND: `.planning/phases/04-gdpr-compliance/04-gdpr-compliance-01-SUMMARY.md`
- FOUND: `site/src/lib/consent.ts`
- FOUND: `site/src/layouts/BaseLayout.astro`
- FOUND: `site/src/pages/privacy.astro`
- FOUND: `site/scripts/verify-phase4.mjs`
- FOUND commit: `0dd9f3f`
- FOUND commit: `377023e`
- FOUND commit: `78f455c`
- FOUND commit: `b8af627`
- FOUND commit: `534ed17`
- FOUND commit: `1eacf8b`
- FOUND commit: `1afdb57`
