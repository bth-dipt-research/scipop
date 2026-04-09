---
phase: 04-gdpr-compliance
date: 2026-04-09
status: complete
requirements:
  - PRIV-01
  - PRIV-02
  - PRIV-03
---

# Phase 4 Research: GDPR Compliance

## Objective

Identify a low-risk static-site implementation pattern for consent-gated GA tracking that preserves Phase 03 telemetry architecture while adding visitor consent control and clear disclosure.

## Inputs Reviewed

- `.planning/ROADMAP.md`
- `.planning/REQUIREMENTS.md`
- `.planning/phases/04-gdpr-compliance/04-CONTEXT.md`
- `.planning/phases/03-analytics-baseline/03-CONTEXT.md`
- `site/src/layouts/BaseLayout.astro`
- `site/src/lib/analytics.ts`
- `site/scripts/verify-phase3.mjs`

## Findings

1. **Current GA injection is centralized in `BaseLayout.astro`** so consent enforcement should also be centralized there to avoid route-level drift.
2. **Phase 03 already production-gates telemetry** via `isProductionTelemetryEnabled()`. Phase 04 must add consent gating on top of this (both conditions required).
3. **A dedicated consent library is appropriate** per context guidance (“do not reinvent”). For Astro/static output and plain-JS integration, `vanilla-cookieconsent` is a suitable fit.
4. **Binary accept/reject is a native fit** for Phase 04 because user decisions explicitly defer granular category customization.
5. **Existing verification pattern is artifact-first scripts** under `site/scripts/`; Phase 04 should add a dedicated verifier to assert consent UI/disclosure and no-unconditional GA markers.

## Recommended Implementation Pattern

### Consent library and storage contract

- Add dependency: `vanilla-cookieconsent`.
- Implement a consent helper module (e.g., `site/src/lib/consent.ts`) that:
  - Uses one stable key for consent state in both cookie and localStorage (D-04).
  - Exposes getter/setter helpers returning explicit states: `'accepted' | 'rejected' | 'unset'`.
  - Treats dismiss/close as reject (D-03).
  - Exposes an update event/hook that UI and analytics gate can react to immediately (D-11).

### Analytics gating behavior

- Keep Phase 03 production checks intact.
- Add consent check so GA script/config is emitted/executed only when:
  - `isProductionTelemetryEnabled() === true`, and
  - Consent state is accepted.
- On transition accepted -> rejected, clear consent-enabled state and prevent subsequent GA config/init execution in current and future loads (D-07).

### UX and disclosure

- Initial surface is a bottom banner (D-01) with only “Accept all” and “Reject all” actions (D-05, D-06).
- Add persistent footer privacy-settings link on all pages reopening the same banner/panel (D-09, D-10).
- Show inline success message after settings updates (D-12).
- Add dedicated privacy page (`/privacy`) and short banner summary copy (D-13), covering provider, purpose, tracked datapoints/events, consent-change instructions, and contact details in plain language (D-14, D-15, D-16).

### Verification approach

- Add `site/scripts/verify-phase4.mjs` to assert:
  - `/privacy` route artifact exists.
  - Required disclosure text markers exist in `/privacy` artifact.
  - Footer contains privacy-settings re-open affordance marker.
  - Base layout no longer unconditionally emits GA markers across routes (checks for consent-gated marker patterns).
- Wire `verify:phase4` in `site/package.json` and include it in full verification workflow with `build`.

## Risks and Mitigations

- **Risk:** Consent banner appears but GA still initializes due to unconditional legacy script path.
  - **Mitigation:** Move GA emission behind explicit consent + production guard in a single code path; verify with phase script.
- **Risk:** Dismiss behavior ambiguity causes accidental tracking.
  - **Mitigation:** Explicitly map dismiss/close event to reject state and persist immediately.
- **Risk:** Storage mismatch between cookie/localStorage causes inconsistent reopen behavior.
  - **Mitigation:** Use one shared state model with write-through to both stores and deterministic read precedence.

## Validation Architecture

### Fast feedback commands

- Quick: `npm --prefix site run build && node site/scripts/verify-phase4.mjs`
- Full: `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2 && npm --prefix site run verify:phase3 && npm --prefix site run verify:phase4`

### Requirement-to-check mapping

- `PRIV-01` automated checks:
  - Consent UI artifacts present and GA script path is consent-gated (not unconditional).
- `PRIV-02` automated checks:
  - Re-open control marker exists in global footer and consent update success marker exists.
- `PRIV-03` automated checks:
  - `/privacy` route contains required disclosure sections and contact details markers.
