# Static scipop

## What This Is

Static scipop is a public, static website that publishes expert-reviewed synthesis texts derived from clustered research areas. It is designed for a general audience to browse research area summaries without needing to run notebooks, scripts, or local tooling. The MVP focuses on clear publication and navigation of finalized synthesis content, not generation automation.

## Core Value

Anyone can reliably access and understand the approved research syntheses through a simple, shareable public website.

## Current Milestone: v2.0 Interactive Topic Modeling

**Goal:** Build an interactive web UI that guides users through iterative topic model refinement with side-by-side parameter comparisons at key decision points.

**Target features:**
- Data upload and filtering (publications by type, select input columns)
- Configurable model generation (UMAP, HDBSCAN, vectorizer, embedding parameters)
- Iterative refinement with side-by-side comparisons at each step:
  - Outlier reduction strategy comparison (before/after preview)
  - Topic labeling configuration comparison (different nr_words settings)
  - Manual topic curation with impact preview (merge/remove topics)
  - Quality check showing papers with no remaining topics after removal
- Visualization and export (hierarchical topic trees, topic info tables, themed paper CSVs)

## Requirements

### Validated

- ✓ Topic-modeling and clustering workflows exist in the repository via experiments and scripts (`experiments/`, `src/DIPT research topics-hierarchical TM.py`) — existing
- ✓ Prompt-based synthesis assets exist and are already used in practice (`prompts/research-to-practice.txt`, `prompts/vision-builder.txt`) — existing
- ✓ Research text extraction and data-preparation pipelines exist for source material (`src/research_question_extractor.py`, `data/`) — existing
- ✓ Publish a static homepage that lists research area clusters and links to synthesis detail pages — Phase 1
- ✓ Publish one dedicated synthesis page per research area from finalized markdown sources — Phase 1
- ✓ Publish one top-level research-group synthesis page representing the group as a whole (`/featured` in Phase 1, migrated to `/overview` in Phase 5)
- ✓ Publish a methodology page explaining how syntheses were created and expert-reviewed — Phase 1
- ✓ Include synthesis disclaimers and cross-device readability/navigation baseline — Phase 2
- ✓ Add basic Google Analytics tracking (page-level usage), without building a custom analytics UI — Validated in Phase 03: analytics-baseline
- ✓ Gate analytics behind explicit visitor consent with reopenable privacy controls and disclosure content — Validated in Phase 04: gdpr-compliance
- ✓ Polish long-form presentation and site navigation IA while preserving accessibility/privacy/analytics behavior — Validated in Phase 05: ui-polish

### Active

- [ ] Upload publication data (CSV/XLSX) and preview in UI
- [ ] Filter publications by type and select input columns for topic modeling
- [ ] Configure and run topic model with adjustable parameters (UMAP, HDBSCAN, vectorizer, embedding)
- [ ] Compare outlier reduction strategies side-by-side and select preferred approach
- [ ] Compare topic labeling configurations and select preferred settings
- [ ] Manually curate topics (merge/remove) with impact preview
- [ ] Show quality check: papers with no remaining topics after curation
- [ ] Visualize hierarchical topic structure
- [ ] Export topic model results and themed paper CSVs
- [ ] Deploy the site on GitHub Pages with a stable public URL for sharing (from v1.0)

### Out of Scope

- Integration with v1.0 static site — v2.0 is a standalone tool, not part of the public website
- Automated synthesis generation from topic models — still deferred; v2.0 focuses on topic model UI only
- User accounts/authentication — not needed for local topic modeling tool
- Persistent storage of topic model sessions — user exports results, no session management
- Real-time collaboration — single-user tool for now

## Context

**v1.0 delivered:** A static publication website with homepage, synthesis pages, overview, methodology, readability/accessibility baseline, Google Analytics with GDPR consent, and UI polish.

**v2.0 focus:** Build an interactive UI for the topic modeling workflow that currently exists only in Jupyter notebooks (`experiments/BTH research topics.ipynb`) and partially in a Streamlit prototype (`src/DIPT research topics-hierarchical TM.py`). The notebook demonstrates an iterative refinement process where parameters are adjusted manually and outputs compared by eye. The new UI should formalize this workflow with side-by-side comparisons at key decision points.

**Existing topic modeling artifacts:**
- Notebook workflow: `experiments/BTH research topics.ipynb`
- Partial Streamlit prototype: `src/DIPT research topics-hierarchical TM.py` (upload + filtering only)
- BERTopic-based pipeline with UMAP, HDBSCAN, KeyBERT representation

Existing codebase map documents:
- `/.planning/codebase/STACK.md`
- `/.planning/codebase/ARCHITECTURE.md`
- `/.planning/codebase/STRUCTURE.md`

## Constraints

- **Tech Stack**: Python + Streamlit — topic modeling UI should extend existing Streamlit prototype
- **Workflow Fidelity**: Mirror notebook workflow — must replicate the iterative refinement process from `experiments/BTH research topics.ipynb`
- **ML Stack**: BERTopic + UMAP + HDBSCAN — keep existing topic modeling pipeline components
- **Comparison UI**: Side-by-side parameter variations — core convenience feature for decision points
- **Scope**: Topic modeling tool only — v2.0 does not integrate with static site publication from v1.0

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Start with static publication before automation | Fastest path to visible value from already reviewed syntheses | Adopted in Phase 1 |
| Use index + detail information architecture | Matches browse-first discovery and supports multiple research areas cleanly | Implemented in Phase 1 |
| Include a top-level research-group synthesis page | User wants both area-level syntheses and a whole-group synthesis narrative | Implemented in Phase 1, IA migrated to `/overview` in Phase 5 |
| Host MVP on GitHub Pages | Low-friction static deployment and easy sharing | — Pending |
| Include basic Google Analytics only | Need lightweight usage visibility without building product analytics features | Implemented in Phase 3 |
| Gate analytics behind explicit consent with persistent settings access | Respect privacy requirements while keeping static-site delivery and simple UX | Implemented in Phase 4 |
| Standardize disclaimer heading/default copy with optional page override | Keep trust messaging consistent while allowing narrative-specific nuance | Implemented in Phase 2 |
| Enforce disclaimer coverage through build-artifact verification | Prevent accidental omission on required narrative routes | Implemented in Phase 2 |
| Set shared readability tokens with 70ch article measure and accessible mobile menu behavior | Ensure cross-device readability and navigation usability for public audience | Implemented in Phase 2 |
| Replace `/featured` with `/overview` and update global navigation links | Keep research-group narrative destination while aligning polished IA | Implemented in Phase 5 |
| Require per-synthesis editor profile block (photo, name, email, contact sentence) | Improve trust and accountability on each approved synthesis article | Implemented in Phase 5 |
| Use desktop research-theme image map with explicit mobile fallback links | Deliver stronger homepage wayfinding without regressing accessibility | Implemented in Phase 5 |

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
*Last updated: 2026-04-29 after starting milestone v2.0*
