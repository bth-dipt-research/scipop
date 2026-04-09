# Phase 4: GDPR Compliance - Context

**Gathered:** 2026-04-09
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement consent-based analytics behavior for the public site so tracking runs only when visitors opt in, visitors can change privacy settings later, and visitors can read clear tracking disclosure details.

</domain>

<decisions>
## Implementation Decisions

### Consent UX surface
- **D-01:** Use a bottom banner as the initial consent prompt.
- **D-02:** Do not load or run GA before explicit consent.
- **D-03:** Treat banner dismissal as reject by default.
- **D-04:** Persist consent in both cookie and localStorage.

### Consent choice model
- **D-05:** Initial choices are only `Accept all` and `Reject all`.
- **D-06:** Do not implement a `Customize` flow in Phase 04.
- **D-07:** If user switches from accept to reject later, apply immediately: stop GA behavior and clear consent-enabled state.
- **D-08:** Do not add consent-version re-prompt logic in Phase 04.

### Settings re-open path
- **D-09:** Add a footer link available on all pages for privacy settings.
- **D-10:** Re-open the same consent banner/panel from that link (no separate settings modal/page for controls).
- **D-11:** Apply settings changes immediately without requiring reload.
- **D-12:** Show an inline success confirmation after settings update.

### Tracking disclosure content
- **D-13:** Create a dedicated privacy page plus short summary copy in the banner.
- **D-14:** Disclosure must include provider, purpose, tracked data points/events, and how users can change consent.
- **D-15:** Use plain-language wording suitable for general public audience.
- **D-16:** Include contact details for privacy/technical questions.

### the agent's Discretion
- Exact library selection for consent management, provided it is established/maintained and integrates cleanly with Astro static output.
- Exact naming of storage keys/cookie key and the consent component internal state shape.
- Exact UI microcopy and visual styling details, as long as the locked behavior and disclosure requirements are preserved.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and requirement definitions
- `.planning/ROADMAP.md` — Phase 04 boundary, goal, and success criteria.
- `.planning/REQUIREMENTS.md` — `PRIV-01`, `PRIV-02`, `PRIV-03` definitions.
- `.planning/PROJECT.md` — audience and platform constraints (public readability, static delivery, GitHub Pages target).

### Prior decision continuity
- `.planning/phases/03-analytics-baseline/03-CONTEXT.md` — production telemetry gating and env-config decisions that consent logic must wrap.
- `.planning/phases/02-readability-accessibility-baseline/02-CONTEXT.md` — mobile/desktop navigation and accessibility baseline to preserve when adding settings entry points.

### Existing deployment/runtime context
- `.github/workflows/deploy-pages.yaml` — current production deploy environment behavior and public env variable wiring.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `site/src/layouts/BaseLayout.astro`: current global GA bootstrap location and shared header/nav shell; primary integration point for consent gate and settings entry wiring.
- `site/src/lib/analytics.ts`: existing production-env and measurement-id helpers to reuse for consent-aware telemetry enablement.
- `site/scripts/verify-phase3.mjs`: reusable build-artifact verification style for required-route checks.

### Established Patterns
- Global behavior is centralized in `BaseLayout.astro` for all public routes.
- Telemetry is currently production-gated and measurement-id validated before use.
- Per-phase verification scripts (`verify:phase*`) are the established quality gate pattern.

### Integration Points
- Wrap GA script/config emission in consent-aware logic within `site/src/layouts/BaseLayout.astro`.
- Add consent state read/write utilities (and library integration wrapper) under `site/src/lib/` and invoke from layout-level UI.
- Add privacy disclosure route under `site/src/pages/` and link from banner + footer.
- Add/update verifier script(s) in `site/scripts/` and `site/package.json` to enforce consent gating and disclosure route presence.

</code_context>

<specifics>
## Specific Ideas

- Use a standard library approach for consent management ("do not reinvent the wheel") rather than custom-from-scratch consent mechanics.
- Keep the user-facing privacy flow straightforward: binary consent choice now, revisit via persistent footer entry.

</specifics>

<deferred>
## Deferred Ideas

- Granular consent categories/customization flow beyond binary accept/reject.
- Consent versioning and forced re-prompt on policy updates.

</deferred>

---

*Phase: 04-gdpr-compliance*
*Context gathered: 2026-04-09*
