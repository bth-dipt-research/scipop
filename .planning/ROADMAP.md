# Roadmap: Static scipop

## Overview

This roadmap delivers the MVP as a public, static publication experience: first make the core synthesis information architecture usable, then harden reading quality across devices, then add lightweight usage measurement for iteration.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [ ] **Phase 1: Core Publication Surface** - Users can discover and open all core synthesis content destinations.
- [ ] **Phase 2: Readability & Accessibility Baseline** - Public content is readable and navigable on desktop and mobile.
- [ ] **Phase 3: Analytics Baseline** - Basic page-level usage is captured for MVP learning.

## Phase Details

### Phase 1: Core Publication Surface
**Goal**: Users can discover the research landscape and open each primary synthesis destination through stable public links.
**Depends on**: Nothing (first phase)
**Requirements**: PUBL-01, PUBL-02, PUBL-03, PUBL-04
**Success Criteria** (what must be TRUE):
  1. User can browse a homepage that lists all research area clusters.
  2. User can open each research area synthesis at a stable, shareable URL.
  3. User can open a featured top-level synthesis representing the whole research group.
  4. User can open a methodology page that explains synthesis creation and expert review.
**Plans**: 3 plans
Plans:
- [ ] 01-01-PLAN.md — Scaffold Astro publication app and content contracts with route smoke verification
- [ ] 01-02-PLAN.md — Implement homepage cluster listing and synthesis detail routes
- [ ] 01-03-PLAN.md — Implement featured and methodology routes with destination verification
**UI hint**: yes

### Phase 2: Readability & Accessibility Baseline
**Goal**: Users can comfortably consume and navigate all published synthesis content across desktop and mobile contexts.
**Depends on**: Phase 1
**Requirements**: PUBL-05, PUBL-06
**Success Criteria** (what must be TRUE):
  1. User can find and read a disclaimer section at the end of every synthesis page.
  2. User can read content without layout breakage on both mobile and desktop viewports.
  3. User can navigate between public destinations on both device classes without interaction blockers.
**Plans**: TBD
**UI hint**: yes

### Phase 3: Analytics Baseline
**Goal**: Project owner can verify that public usage is being measured with basic GA pageview telemetry.
**Depends on**: Phase 2
**Requirements**: ANLT-01
**Success Criteria** (what must be TRUE):
  1. When a visitor accesses any public route, a corresponding GA pageview event is recorded.
  2. Project owner can confirm real-time and standard-report visibility of visit data for the published routes.
**Plans**: TBD

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Publication Surface | 2/3 | In Progress|  |
| 2. Readability & Accessibility Baseline | 0/TBD | Not started | - |
| 3. Analytics Baseline | 0/TBD | Not started | - |
