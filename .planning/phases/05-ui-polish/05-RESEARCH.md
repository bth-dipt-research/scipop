---
phase: 05-ui-polish
date: 2026-04-10
status: complete
requirements:
  - UIP-01
  - UIP-02
  - UIP-03
---

# Phase 5 Research: UI Polish

## Objective

Identify a low-risk implementation approach for visual/IA polish in the Astro static site while preserving Phase 02 readability/accessibility and Phase 03-04 analytics/privacy behavior.

## Inputs Reviewed

- `.planning/ROADMAP.md`
- `.planning/phases/05-ui-polish/05-CONTEXT.md`
- `.planning/phases/02-readability-accessibility-baseline/02-CONTEXT.md`
- `.planning/phases/03-analytics-baseline/03-CONTEXT.md`
- `.planning/phases/04-gdpr-compliance/04-CONTEXT.md`
- `site/src/layouts/BaseLayout.astro`
- `site/src/pages/index.astro`
- `site/src/pages/syntheses/[slug].astro`
- `site/src/pages/featured/index.astro`
- `site/src/content.config.ts`
- `data/dev/Grafisk manual.pdf`
- `data/dev/SERLSweden_rectangular-black.svg`
- `data/dev/Research themes.drawio.svg`

## Findings

1. **`BaseLayout.astro` is the highest-leverage integration point** for typography tokens, header/nav IA, and preserving consent/analytics behavior; Phase 5 should keep these scripts intact and limit changes to visual/nav structure around them.
2. **Long-form readability constraints are already encoded** (`70ch`, responsive body size, focus states, touch target sizing). UI polish should tune visual language without weakening these defaults.
3. **Homepage currently renders only card listings**, so desktop image-map navigation is best introduced as a dedicated component with explicit fallback links for mobile.
4. **`/featured` currently carries the research-group long-form page**, so replacing IA with `/overview` requires both route migration and navigation updates to avoid broken links.
5. **Synthesis schema currently lacks editor metadata**, so per-entry editor profile blocks require schema additions plus frontmatter updates across all approved synthesis content files.
6. **Existing verification pattern is phase-specific static/build checks** (`site/scripts/verify-phase*.mjs` + `package.json` scripts), so Phase 5 should add `verify-phase5.mjs` covering IA/route/editor markers.

## Recommended Implementation Pattern

### Visual system and global layout polish

- Introduce explicit design tokens in `BaseLayout.astro` (color, typography, spacing, radius, shadow) aligned to the restrained academic direction.
- Apply serif body text for long-form content and sans-serif for navigation/UI labels.
- Add branded header with left-aligned logo asset and right-aligned nav links.
- Keep consent and analytics script blocks behaviorally unchanged; only move/retune surrounding markup/styles.

### Long-form presentation and IA migration

- Keep article max-width around 70ch and existing responsive sizing baseline.
- Apply justified paragraph text only to long-form article surfaces (`/syntheses/[slug]`, `/methodology`, `/privacy`, `/overview`), with ragged fallback for narrow screens when needed.
- Create `/overview` page by reusing/adapting current featured content.
- Remove `/featured` route and nav exposure; ensure homepage and header no longer reference it.

### Homepage image-map interaction model

- Implement a dedicated desktop/tablet map component (SVG hotspots or absolutely positioned links over SVG) sourced from `Research themes.drawio.svg`.
- Provide a mobile fallback list/card navigation that remains fully keyboard/screen-reader accessible.
- Keep existing synthesis cards as fallback/link targets rather than removing them entirely.

### Editor profile block model

- Extend `syntheses` collection schema with required editor fields:
  - `editor_name`
  - `editor_email`
  - `editor_photo`
  - `editor_contact_sentence`
- Enforce required-field presence at build time via schema validation.
- Render a top-of-article editor profile block in `/syntheses/[slug]` with desktop wrap behavior and mobile stacked behavior.

### Verification approach

- Add `site/scripts/verify-phase5.mjs` to assert:
  - `/overview` exists and `/featured` no longer builds.
  - Header/nav includes `/overview` and excludes `/featured`.
  - Homepage includes desktop map markers and mobile fallback markers.
  - Synthesis artifacts include editor profile markers and standard contact sentence.
  - Long-form pages include justified text marker/class hook.
- Add npm script `verify:phase5` in `site/package.json`.

## Risks and Mitigations

- **Risk:** Visual polish accidentally breaks consent banner or telemetry gating logic.
  - **Mitigation:** Avoid altering consent/analytics logic blocks; run phase1-4 verifiers alongside phase5 checks.
- **Risk:** Desktop image map reduces accessibility.
  - **Mitigation:** Keep semantic links for all targets; retain mobile fallback list; include keyboard focus styles and descriptive labels.
- **Risk:** Required editor metadata missing in one or more synthesis files.
  - **Mitigation:** Make fields required in schema and add verifier checks over generated synthesis routes.
- **Risk:** `/featured` removal breaks internal links/bookmarks.
  - **Mitigation:** Update all internal references during phase and verify route presence/absence explicitly in verifier.

## Validation Architecture

### Fast feedback commands

- Quick: `npm --prefix site run build && npm --prefix site run verify:phase5`
- Full: `npm --prefix site run build && npm --prefix site run verify:phase1 && npm --prefix site run verify:phase2 && npm --prefix site run verify:phase3 && npm --prefix site run verify:phase4 && npm --prefix site run verify:phase5`

### Requirement-to-check mapping

- `UIP-01` automated checks:
  - Long-form route artifacts include justified-text markers and preserve baseline article container constraints.
- `UIP-02` automated checks:
  - Synthesis route artifacts include editor profile fields and exact standard contact sentence structure.
- `UIP-03` automated checks:
  - `/overview` route exists, `/featured` route absent, nav markers updated, homepage map/fallback markers present.
