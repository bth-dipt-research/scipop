# Phase 2 Research — Readability & Accessibility Baseline

**Phase:** 2  
**Date:** 2026-04-03  
**Requirements:** PUBL-05, PUBL-06

## Objective

Define a low-risk implementation plan that makes all public pages readable and navigable on desktop/mobile, while enforcing disclaimer coverage on required synthesis narrative pages.

## Recommended Technical Approach

1. Keep implementation in existing Astro surfaces only (`BaseLayout.astro`, synthesis/featured pages, content schema).
2. Add disclaimer fields to content schemas with:
   - shared default disclaimer copy support,
   - optional per-page disclaimer override,
   - explicit build-time failures when required disclaimer content is missing.
3. Render disclaimer as the final section of required narrative pages only:
   - `/syntheses/{slug}`
   - `/featured`
   - explicitly **exclude** `/methodology` per user decision.
4. Add global responsive typography + spacing styles in `BaseLayout.astro` so all public pages inherit readability baseline.
5. Replace static nav with responsive desktop+mobile pattern in `BaseLayout.astro` with keyboard support, visible focus states, and 44px touch targets.

## Locked Decision Implementation Notes

- Respect D-01..D-05 for disclaimer scope, placement, shared default copy, optional overrides, and build-fail behavior.
- Respect D-06..D-09 for disclaimer heading + tone + exact default copy.
- Respect D-10..D-13 for reading measure (`65-75ch`), body scale (`16px`→`18px`), line-height (`1.65` body), and spacing rhythm.
- Respect D-14..D-17 for mobile menu behavior, desktop nav visibility, keyboard/focus/touch accessibility baseline, and auto-close on selection.

## Risks and Mitigations

1. **Risk:** Missing disclaimer frontmatter on required pages creates silent content gaps.
   - **Mitigation:** hard throw in route pages when computed disclaimer text is empty.
2. **Risk:** Mobile nav can break keyboard/screen-reader behavior.
   - **Mitigation:** semantic button, `aria-expanded`, `aria-controls`, focus-visible styles, and no hidden-only links without toggle state sync.
3. **Risk:** Styling changes regress route rendering silently.
   - **Mitigation:** keep automated verify script for route existence + run Astro build as strict gate.

## Validation Architecture

Phase 2 validation should combine build integrity + deterministic route checks + static checks for new disclaimer wiring.

- **Primary signal:** `npm --prefix site run build` exits 0.
- **Secondary signal:** `npm --prefix site run verify:phase1` still passes (no route regressions).
- **Phase checks:** add `verify:phase2` script to assert required disclaimer content fields exist and required routes are present.

Recommended validation contract values:
- quick command: `npm --prefix site run build`
- full command: `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2`
- max feedback latency target: under 60 seconds local

## Planning Implications

- Use 2 sequential plans (shared `BaseLayout.astro` ownership).
- Keep each plan at 2 tasks for context quality.
- Ensure both requirement IDs appear in plan frontmatter coverage.
