# Phase 5: ui-polish - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md - this log preserves alternatives considered.

**Date:** 2026-04-09
**Phase:** 05-ui-polish
**Areas discussed:** Visual language, Homepage hierarchy, Structure updates, Synthesis editor profile

---

## Visual language

| Option | Description | Selected |
|--------|-------------|----------|
| Editorial serif body | Serif body for long-form reading + sans UI labels | x |
| Modern sans everywhere | All text sans-serif with refined scale/spacing | |
| Minimal change | Keep current system stack and only tune spacing/colors | |

**User's choice:** Editorial serif body
**Notes:** User asked to anchor typography and palette to the university graphic manual.

| Option | Description | Selected |
|--------|-------------|----------|
| Logo left + nav right | Header brand-left, links-right | x |
| Logo above nav | Stacked brand and nav | |
| Logo only on home | Brand shown only on homepage | |

**User's choice:** Logo left + nav right
**Notes:** Explicitly requested adding research-group logo to header.

| Option | Description | Selected |
|--------|-------------|----------|
| All long-form articles | Justify synthesis + methodology + privacy article bodies | x |
| Synthesis pages only | Justify only synthesis narratives | |
| Every paragraph site-wide | Justify all paragraphs globally | |

**User's choice:** All long-form articles
**Notes:** User explicitly requested justified long-form text.

| Option | Description | Selected |
|--------|-------------|----------|
| Subtle academic polish | Neutral palette with restrained accents | x |
| Strong branded look | Heavier visual accents and motifs | |
| Monochrome minimal | Mostly black/white neutral scheme | |

**User's choice:** Subtle academic polish
**Notes:** Confirmed as the target visual intensity.

---

## Structure updates

| Option | Description | Selected |
|--------|-------------|----------|
| Remove route + nav link | Remove `/featured` and its nav exposure | x |
| Keep route, hide in nav | Keep `/featured` reachable by direct URL | |
| Redirect `/featured` to home | Keep route as redirect | |

**User's choice:** Remove route + nav link
**Notes:** User asked to remove featured synthesis concept from primary IA.

| Option | Description | Selected |
|--------|-------------|----------|
| New header link + dedicated page | Separate long-form research-group page | x |
| Methodology sub-section | Embed long narrative inside methodology | |
| Homepage section | Place long narrative directly on homepage | |

**User's choice:** New header link + dedicated page
**Notes:** User stated long overview text should not be on homepage.

| Option | Description | Selected |
|--------|-------------|----------|
| New route `/overview` | New URL and nav label for overview content | x |
| Reuse `/featured` route | Keep path, only change semantics | |
| New route `/research-group` | Alternative explicit route name | |

**User's choice:** New route `/overview`
**Notes:** Explicit route preference was provided.

---

## Synthesis editor profile

| Option | Description | Selected |
|--------|-------------|----------|
| Photo + name + email | Concise profile card fields | |
| Add title/role too | Add role/title to core fields | |
| Add short bio | Add 1-2 sentence biography | |
| Other (free-text) | User-specified field set and copy | x |

**User's choice:** Photo, name, email, and standard text: "Questions regarding the research presented on this page? Please contact [Title] [Firstname] [Lastname]. [email]"
**Notes:** This standardized sentence should appear on every synthesis editor block.

| Option | Description | Selected |
|--------|-------------|----------|
| Top-left with wrap | Near article start; wrap on desktop, stack on mobile | x |
| Top full-width | Full-width block above article body | |
| Right sidebar | Desktop sidebar variant | |

**User's choice:** Top-left with wrap
**Notes:** Placement should be near beginning of article.

---

## Homepage hierarchy

| Option | Description | Selected |
|--------|-------------|----------|
| Cards-first, short intro | Intro + prominent cluster cards | |
| Long intro, then cards | Narrative-first homepage | |
| Split layout with highlights | Highlights plus card section | |
| Other (free-text) | Image-map-centered homepage concept | x |

**User's choice:** Use research-theme image map (honeycomb/pentagram structure) as homepage centerpiece.
**Notes:** User referenced `data/dev/Research themes.drawio.svg` as source artifact.

| Option | Description | Selected |
|--------|-------------|----------|
| Desktop map + mobile list | Interactive map desktop/tablet, list/cards on mobile | x |
| Map on all screens | Use map interaction everywhere | |
| Map as decorative only | Keep links in list/cards only | |

**User's choice:** Desktop map + mobile list
**Notes:** Accessibility/reliability fallback on mobile is required.

---

## the agent's Discretion

- Exact token values and motion details within locked visual direction.
- Exact image-map technical strategy (SVG hotspots vs layered anchors).
- Exact schema field naming for editor metadata.

## Deferred Ideas

None.
