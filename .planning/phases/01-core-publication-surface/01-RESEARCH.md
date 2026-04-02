# Phase 1 Research — Core Publication Surface

**Phase:** 1  
**Date:** 2026-04-03  
**Requirements:** PUBL-01, PUBL-02, PUBL-03, PUBL-04

## Objective

Identify the lowest-risk implementation approach for publishing a static MVP website where users can discover cluster syntheses and open each required destination via stable public URLs on GitHub Pages.

## Recommended Technical Approach

1. Use an isolated `site/` Astro project (static build only; no SSR) to avoid coupling with existing Python workflows.
2. Keep publication content in top-level `content/` so researchers can update markdown without modifying app internals.
3. Define strict content contracts in `site/src/content.config.ts` using Astro collections + Zod.
4. Generate pages from content:
   - homepage (`/`) from `syntheses` collection
   - synthesis detail (`/syntheses/[slug]`)
   - featured page (`/featured`)
   - methodology page (`/methodology`)
5. Configure Astro for GitHub Pages path safety (`site`, `base`) to preserve stable shareable URLs.

## Key Decisions for Planning

- **Use Astro content collections** (do not hand-roll markdown parsing) for build-time validation and predictable routing.
- **Use dynamic route generation for synthesis pages** (`getStaticPaths`) from approved entries only.
- **Keep this phase focused on publication surface only** (no search, no account/auth, no automation pipeline).
- **Defer GA instrumentation to Phase 3** to keep Phase 1 scope aligned with roadmap requirements.

## Risks and Mitigations

1. **Broken paths on GitHub Pages project URL**
   - Mitigation: set `site` + `base` in Astro config and verify generated route files after build.
2. **Inconsistent markdown metadata breaking pages**
   - Mitigation: required frontmatter schema in `content.config.ts`; build fails on missing fields.
3. **Over-expansion beyond publication MVP**
   - Mitigation: explicitly prohibit search/filter/automation in plan task actions.

## Validation Architecture

This phase can use build-artifact verification as Nyquist-fast feedback even before a full test framework is introduced.

- **Primary signal:** `npm --prefix site run build` exits 0
- **Secondary signal:** route smoke script confirms required output pages exist:
  - `/`
  - `/syntheses/{slug}` for each approved synthesis
  - `/featured`
  - `/methodology`

Validation strategy artifact should define:
- quick command: `npm --prefix site run build`
- full command: `npm --prefix site run build && npm --prefix site run verify:phase1`
- max feedback latency target: under 60 seconds on local runs

## Planning Implications

- Split into a contract-first foundation plan and route implementation plans.
- Keep plans at 2-3 tasks each to stay under context quality thresholds.
- Ensure every requirement ID appears in at least one plan frontmatter `requirements` field.
