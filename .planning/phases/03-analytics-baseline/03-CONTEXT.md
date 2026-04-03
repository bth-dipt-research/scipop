# Phase 3: Analytics Baseline - Context

**Gathered:** 2026-04-03
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement a basic Google Analytics baseline so public page visits are captured as pageview telemetry across all public routes, and the project owner can verify both real-time and standard-report visibility after deployment.

</domain>

<decisions>
## Implementation Decisions

### Tracking scope
- **D-01:** Required pageview coverage includes all public routes: `/`, `/featured`, `/methodology`, and approved `/syntheses/{slug}` pages.
- **D-02:** Track canonical route paths only; ignore query parameters and hash fragments for baseline reporting.
- **D-03:** Emit pageviews on full page loads only for this phase (no SPA/history-change tracking).
- **D-04:** Phase 3 telemetry scope is pageviews only; outbound click and interaction analytics stay deferred.

### Script loading behavior
- **D-05:** Integrate GA bootstrap globally in `site/src/layouts/BaseLayout.astro` so all public pages inherit tracking from one place.
- **D-06:** Load the GA library with the standard async head snippet.
- **D-07:** Use standard `gtag('config', MEASUREMENT_ID, ...)` initialization for initial pageview handling.
- **D-08:** Apply privacy-safe baseline config: enable IP anonymization and disable ad-personalization-oriented flags.

### Config and deployment
- **D-09:** Source measurement ID from a public build-time environment variable (e.g., `PUBLIC_GA_MEASUREMENT_ID`).
- **D-10:** If measurement ID is missing for a production build, fail the build (do not ship without required telemetry).
- **D-11:** Emit telemetry in production deployments only (not local dev/preview noise).
- **D-12:** Manage production measurement ID through GitHub repository deployment variables/secrets, not hardcoded source values.

### Verification workflow
- **D-13:** Verification must include both automated build-artifact checks and manual GA console validation.
- **D-14:** Automated phase verification checks that GA snippet/config appears on all required public route artifacts.
- **D-15:** Manual real-time verification uses a short checklist with timestamped evidence captured in phase verification notes.
- **D-16:** Standard GA report verification is required within 24 hours of deployment.

### the agent's Discretion
- Exact GA snippet implementation details and parameter ordering, as long as locked tracking/config/privacy decisions are preserved.
- Exact verification-note format for evidence capture, as long as route coverage and 24-hour standard-report confirmation are explicit.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase requirements and scope
- `.planning/ROADMAP.md` — Phase 3 goal and success criteria for baseline pageview telemetry and verification.
- `.planning/REQUIREMENTS.md` — `ANLT-01` requirement definition; `ANLT-02` explicitly deferred.
- `.planning/PROJECT.md` — MVP constraints: basic GA only, no custom analytics UI, GitHub Pages static delivery.

### Prior decision continuity
- `.planning/phases/02-readability-accessibility-baseline/02-CONTEXT.md` — Carry-forward publication route structure and verification style consistency from earlier phase work.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `site/src/layouts/BaseLayout.astro`: single shared wrapper for all public pages; ideal integration point for global analytics bootstrap.
- `site/src/lib/paths.ts`: existing base-path normalization helper useful when constructing canonical route paths under `/scipop`.
- `site/src/pages/syntheses/[slug].astro`: route-generation pattern for approved synthesis pages informs required route coverage expectations.

### Established Patterns
- `site/astro.config.mjs` defines static output and `/scipop` base path for GitHub Pages.
- `site/scripts/verify-phase1.mjs` and `site/scripts/verify-phase2.mjs` establish build-artifact verification pattern using `dist` HTML checks.
- `site/package.json` maintains per-phase verify scripts (`verify:phase1`, `verify:phase2`) as workflow conventions.

### Integration Points
- Add analytics bootstrap and environment gating in `site/src/layouts/BaseLayout.astro`.
- Add Phase 3 verification script in `site/scripts/` and wire it into `site/package.json` as `verify:phase3`.
- Reuse route-discovery approach from existing verify scripts to assert analytics snippet presence on required routes.

</code_context>

<specifics>
## Specific Ideas

- Keep analytics baseline strict and auditable: fail production builds if telemetry config is missing.
- Keep verification practical: combine automated route checks with manual GA evidence collection shortly after deployment.

</specifics>

<deferred>
## Deferred Ideas

- Outbound click analytics (`ANLT-02`) remains a later phase item, not part of Phase 3 baseline.
- Any custom analytics dashboard/reporting UI remains out of MVP scope.

</deferred>

---

*Phase: 03-analytics-baseline*
*Context gathered: 2026-04-03*
