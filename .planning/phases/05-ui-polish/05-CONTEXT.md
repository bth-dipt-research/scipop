# Phase 5: ui-polish - Context

**Gathered:** 2026-04-09
**Status:** Ready for planning

<domain>
## Phase Boundary

Polish the public Astro site UI so the reading and navigation experience is more intentional and brand-aligned, while preserving existing accessibility/privacy/analytics behavior and keeping the site static.

</domain>

<decisions>
## Implementation Decisions

### Brand visual system and typography
- **D-01:** Adopt a subtle academic visual direction derived from the BTH graphic manual, not a high-saturation or decorative redesign.
- **D-02:** Use editorial long-form typography with serif body text and sans-serif UI headings/labels.
- **D-03:** Use the manual-defined palette as canonical; prioritize sea/dark neutral web-safe tones and use orange only as an accent.
- **D-04:** Place the research-group logo in the header with logo-left and primary navigation-right layout.

### Long-form article presentation
- **D-05:** Apply justified paragraph alignment across all long-form article pages (synthesis pages, methodology page, and privacy page).
- **D-06:** Keep previously locked readability baselines (70ch reading measure, responsive type sizing, keyboard/focus/touch accessibility) while applying the polish updates.

### Synthesis editor profile block
- **D-07:** Add a per-synthesis editor block near the top of each synthesis article.
- **D-08:** Required editor block fields are photo, name, and email.
- **D-09:** Include the standard contact sentence in every editor block: "Questions regarding the research presented on this page? Please contact [Title] [Firstname] [Lastname]. [email]"
- **D-10:** Place the editor block top-left with wrapped body text on desktop; stack above article content on mobile.

### Homepage and navigation structure
- **D-11:** Replace homepage card-first emphasis with a research-theme image-map centerpiece (hex/pentagram structure) for desktop/tablet navigation.
- **D-12:** Use accessible list/card link navigation on mobile instead of the image map.
- **D-13:** Remove the featured-synthesis IA concept: remove `/featured` route and remove the featured nav link.
- **D-14:** Add a dedicated long-form research-group overview page at `/overview`, linked from the header navigation.

### the agent's Discretion
- Exact CSS token values, spacing scale numbers, and animation timing that satisfy the locked visual direction.
- Exact technical implementation for the image map interaction model (SVG map hotspots vs transformed link regions), as long as desktop map and mobile fallback behavior are preserved.
- Exact schema field names for editor metadata in content entries, as long as required fields and standard contact text are represented.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Phase scope and continuity
- `.planning/PROJECT.md` - project constraints and audience expectations for static public publishing.
- `.planning/ROADMAP.md` - active roadmap anchor and milestone context.
- `.planning/phases/02-readability-accessibility-baseline/02-CONTEXT.md` - carry-forward readability/accessibility baselines to preserve.
- `.planning/phases/03-analytics-baseline/03-CONTEXT.md` - telemetry and verification constraints that UI polish must not break.
- `.planning/phases/04-gdpr-compliance/04-CONTEXT.md` - consent UX and privacy control requirements that UI polish must preserve.

### Visual identity and assets (user-provided)
- `data/dev/Grafisk manual.pdf` - canonical typography, color, and logo usage rules.
- `data/dev/SERLSweden_rectangular-black.svg` - canonical light-background logo asset.
- `data/dev/SERLSweden_rectangular-white.svg` - canonical dark-background logo asset.
- `data/dev/Research themes.drawio.svg` - canonical source for homepage research-theme image map structure.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `site/src/layouts/BaseLayout.astro`: single integration point for global typography, header/nav structure, footer links, consent banner, and shared styles.
- `site/src/components/ClusterCard.astro`: existing synthesis-link surface for mobile fallback list/cards.
- `site/src/pages/index.astro`: current homepage synthesis listing flow where image-map-first hierarchy will connect.
- `site/src/pages/syntheses/[slug].astro`: synthesis article template where editor profile block should be injected.
- `site/src/pages/featured/index.astro`: existing long-form structure that can inform `/overview` migration/replacement.

### Established Patterns
- Public pages consistently render through `BaseLayout.astro` with centralized global styling and interactions.
- Route generation for synthesis pages already uses content collections and `getStaticPaths`.
- Required content guards use build-time errors (throw on missing required content) rather than runtime fallback.
- Per-phase verification scripts in `site/scripts/verify-phase*.mjs` are the established quality gate pattern.

### Integration Points
- Update `site/src/layouts/BaseLayout.astro` for logo slot, revised nav links, and shared long-form typography polish.
- Update `site/src/pages/index.astro` to integrate the desktop image map and mobile fallback links.
- Extend content schema in `site/src/content.config.ts` and synthesis content entries for editor profile metadata.
- Inject editor profile rendering in `site/src/pages/syntheses/[slug].astro` near article start.
- Replace featured page usage by adding a new overview route/page and removing featured route/nav references.

</code_context>

<specifics>
## Specific Ideas

- Keep the voice and look "academic but modern": calm palette, trustworthy contrast, restrained accents.
- Preserve privacy/accessibility behavior from previous phases while polishing visuals.
- The research-group-wide synthesis remains a dedicated destination, but under `/overview` instead of `/featured`.

</specifics>

<deferred>
## Deferred Ideas

None - discussion stayed within phase scope.

</deferred>

---

*Phase: 05-ui-polish*
*Context gathered: 2026-04-09*
