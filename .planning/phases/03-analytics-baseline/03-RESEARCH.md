---
phase: 03-analytics-baseline
date: 2026-04-03
status: complete
requirements:
  - ANLT-01
---

# Phase 3 Research: Analytics Baseline

## Objective

Determine the safest static-site pattern for Google Analytics pageview baseline coverage across all public routes while preserving MVP constraints (no custom dashboard, no runtime backend).

## Inputs Reviewed

- `.planning/ROADMAP.md`
- `.planning/REQUIREMENTS.md`
- `.planning/phases/03-analytics-baseline/03-CONTEXT.md`
- `site/src/layouts/BaseLayout.astro`
- `site/scripts/verify-phase1.mjs`
- `site/scripts/verify-phase2.mjs`

## Findings

1. **Single integration point exists and is correct:** `site/src/layouts/BaseLayout.astro` wraps all public pages, so GA bootstrap belongs there (aligns with D-05).
2. **No dependency needed:** GA can be implemented with the standard `gtag.js` snippet directly in layout head; no npm package required for ANLT-01.
3. **Canonical path tracking should use pathname only:** `window.location.pathname` satisfies D-02 (no query/hash) and avoids report fragmentation.
4. **Page-load-only behavior is natural for current Astro setup:** no SPA transition handler needed for D-03.
5. **Build-artifact verification pattern is established:** Phase 1/2 scripts already verify generated HTML route coverage. Phase 3 should follow same pattern for telemetry snippet/config assertions.

## Recommended Implementation Pattern

### GA runtime wiring

- Source measurement ID from `import.meta.env.PUBLIC_GA_MEASUREMENT_ID` (D-09).
- Introduce environment gate `import.meta.env.PUBLIC_SITE_ENV` with `production` as the only value that enables telemetry (D-11).
- In `BaseLayout.astro` frontmatter, throw build error when `PUBLIC_SITE_ENV === 'production'` and measurement ID is empty (D-10).
- Render GA scripts only when telemetry is enabled:
  - Async loader: `https://www.googletagmanager.com/gtag/js?id=...` (D-06)
  - Bootstrap + config call:
    - `gtag('config', measurementId, { ... })` (D-07)
    - `anonymize_ip: true`
    - `allow_google_signals: false`
    - `allow_ad_personalization_signals: false` (D-08)
    - `page_path: window.location.pathname` (D-02)

### Automated verification

- Create `site/scripts/verify-phase3.mjs` to:
  - derive required routes (`/`, `/featured`, `/methodology`, approved `/syntheses/{slug}`) per D-01
  - assert each route artifact exists in `dist` (with base-prefix candidate lookup)
  - assert telemetry markers are present in each required HTML artifact:
    - `googletagmanager.com/gtag/js?id=`
    - `gtag('config'`
    - `anonymize_ip: true`
    - `allow_google_signals: false`
    - `allow_ad_personalization_signals: false`
    - `window.location.pathname`
- Wire as `npm --prefix site run verify:phase3` in `site/package.json`.

### Manual verification workflow

- Add a checklist artifact in phase folder for:
  - real-time GA confirmation after deploy with timestamp + route list evidence (D-15)
  - standard report confirmation within 24 hours (D-16)

## Risks and Mitigations

- **Risk:** Missing measurement ID in production silently ships without telemetry.
  - **Mitigation:** explicit build-time throw when `PUBLIC_SITE_ENV=production` and ID missing.
- **Risk:** Route coverage regresses as new syntheses are added.
  - **Mitigation:** verifier dynamically reads approved slugs from markdown source.
- **Risk:** Preview/local traffic pollutes reporting.
  - **Mitigation:** telemetry emission gated to `PUBLIC_SITE_ENV=production` only.

## Validation Architecture

### Fast feedback commands

- Quick: `npm --prefix site run build && npm --prefix site run verify:phase3`
- Full: `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2 && npm --prefix site run verify:phase3`

### Requirement-to-check mapping

- `ANLT-01` automated checks:
  - Route artifact coverage for all required public routes
  - GA bootstrap/config/privacy markers present in required built HTML artifacts
- `ANLT-01` manual checks:
  - GA Realtime view shows active visit events for tested routes
  - GA standard report confirms route visibility within 24h
