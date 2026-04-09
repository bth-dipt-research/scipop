# Static scipop

## What This Is

Static scipop is a public, static website that publishes expert-reviewed synthesis texts derived from clustered research areas. It is designed for a general audience to browse research area summaries without needing to run notebooks, scripts, or local tooling. The MVP focuses on clear publication and navigation of finalized synthesis content, not generation automation.

## Core Value

Anyone can reliably access and understand the approved research syntheses through a simple, shareable public website.

## Requirements

### Validated

- ✓ Topic-modeling and clustering workflows exist in the repository via experiments and scripts (`experiments/`, `src/DIPT research topics-hierarchical TM.py`) — existing
- ✓ Prompt-based synthesis assets exist and are already used in practice (`prompts/research-to-practice.txt`, `prompts/vision-builder.txt`) — existing
- ✓ Research text extraction and data-preparation pipelines exist for source material (`src/research_question_extractor.py`, `data/`) — existing
- ✓ Publish a static homepage that lists research area clusters and links to synthesis detail pages — Phase 1
- ✓ Publish one dedicated synthesis page per research area from finalized markdown sources — Phase 1
- ✓ Publish one featured top-level synthesis page representing the research group as a whole — Phase 1
- ✓ Publish a methodology page explaining how syntheses were created and expert-reviewed — Phase 1
- ✓ Include synthesis disclaimers and cross-device readability/navigation baseline — Phase 2
- ✓ Add basic Google Analytics tracking (page-level usage), without building a custom analytics UI — Validated in Phase 03: analytics-baseline
- ✓ Gate analytics behind explicit visitor consent with reopenable privacy controls and disclosure content — Validated in Phase 04: gdpr-compliance

### Active

- [ ] Deploy the site on GitHub Pages with a stable public URL for sharing

### Out of Scope

- Automation pipeline for synthesis generation and publishing — explicitly deferred until after MVP publication succeeds
- User accounts/authentication — not needed for public read-only synthesis delivery
- Search/filter features — deferred to keep first release focused on core publish-and-browse flow
- Custom analytics dashboards or interactive reporting tools — excluded from MVP; basic GA tracking only

## Context

This repository already contains exploratory topic-modeling work and synthesis-related prompt assets, but not a production publication surface for external readers. Current artifacts are primarily in local research workflows (`experiments/`, `src/`, `data/`, `prompts/`) and are not packaged as an audience-ready website. The user has validated synthesis quality through expert review and now wants to publish those approved syntheses first, then automate the pipeline in a later milestone.

Existing codebase map documents:
- `/.planning/codebase/STACK.md`
- `/.planning/codebase/ARCHITECTURE.md`
- `/.planning/codebase/STRUCTURE.md`

## Constraints

- **Hosting**: GitHub Pages — required for initial deployment target and sharing simplicity
- **Content Source**: Markdown-first — finalized syntheses are currently stored in markdown files
- **Scope**: MVP publication only — no planning/execution for end-to-end automation yet
- **Audience**: General public — content presentation should be readable beyond domain experts
- **Delivery Model**: Static site architecture — avoid backend/runtime complexity in v1

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Start with static publication before automation | Fastest path to visible value from already reviewed syntheses | Adopted in Phase 1 |
| Use index + detail information architecture | Matches browse-first discovery and supports multiple research areas cleanly | Implemented in Phase 1 |
| Include a featured top-level research-group synthesis page | User wants both area-level syntheses and a whole-group synthesis narrative | Implemented in Phase 1 |
| Host MVP on GitHub Pages | Low-friction static deployment and easy sharing | — Pending |
| Include basic Google Analytics only | Need lightweight usage visibility without building product analytics features | Implemented in Phase 3 |
| Gate analytics behind explicit consent with persistent settings access | Respect privacy requirements while keeping static-site delivery and simple UX | Implemented in Phase 4 |
| Standardize disclaimer heading/default copy with optional page override | Keep trust messaging consistent while allowing narrative-specific nuance | Implemented in Phase 2 |
| Enforce disclaimer coverage through build-artifact verification | Prevent accidental omission on required narrative routes | Implemented in Phase 2 |
| Set shared readability tokens with 70ch article measure and accessible mobile menu behavior | Ensure cross-device readability and navigation usability for public audience | Implemented in Phase 2 |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? -> Move to Out of Scope with reason
2. Requirements validated? -> Move to Validated with phase reference
3. New requirements emerged? -> Add to Active
4. Decisions to log? -> Add to Key Decisions
5. "What This Is" still accurate? -> Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check -> still the right priority?
3. Audit Out of Scope -> reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-09 after Phase 4*
