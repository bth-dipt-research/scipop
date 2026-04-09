# Roadmap: Static scipop

## Overview

This roadmap delivers the MVP as a public, static publication experience: first make the core synthesis information architecture usable, then harden reading quality across devices, then add lightweight usage measurement for iteration.

## Phases

**Phase Numbering:**
- Zero-padded integer phases (01, 02, 03): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

- [x] **Phase 01: Core Publication Surface** - Users can discover and open all core synthesis content destinations. (completed 2026-04-02)
- [x] **Phase 02: Readability & Accessibility Baseline** - Public content is readable and navigable on desktop and mobile. (completed 2026-04-03)
- [x] **Phase 03: Analytics Baseline** - Basic page-level usage is captured for MVP learning. (completed 2026-04-07)
- [x] **Phase 04: GDPR Compliance** - Public visitors can control analytics tracking consent and review what data is collected. (completed 2026-04-09)

## Phase Details

### Phase 01: Core Publication Surface
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

### Phase 02: Readability & Accessibility Baseline
**Goal**: Users can comfortably consume and navigate all published synthesis content across desktop and mobile contexts.
**Depends on**: Phase 01
**Requirements**: PUBL-05, PUBL-06
**Success Criteria** (what must be TRUE):
  1. User can find and read a disclaimer section at the end of every synthesis page.
  2. User can read content without layout breakage on both mobile and desktop viewports.
  3. User can navigate between public destinations on both device classes without interaction blockers.
**Plans**: 2 plans
Plans:
- [x] 02-01-PLAN.md — Add required synthesis disclaimers with build-time coverage checks
- [x] 02-02-PLAN.md — Implement responsive typography and accessible mobile/desktop navigation baseline
**UI hint**: yes

### Phase 03: Analytics Baseline
**Goal**: Project owner can verify that public usage is being measured with basic GA pageview telemetry.
**Depends on**: Phase 02
**Requirements**: ANLT-01
**Success Criteria** (what must be TRUE):
  1. When a visitor accesses any public route, a corresponding GA pageview event is recorded.
  2. Project owner can confirm real-time and standard-report visibility of visit data for the published routes.
**Plans**: 3 plans
Plans:
- [ ] 03-01-PLAN.md — Implement production-gated GA bootstrap and privacy-safe pageview config in shared layout
- [ ] 03-02-PLAN.md — Add Phase 3 analytics verification automation and manual GA evidence checklist
- [ ] 03-03-PLAN.md — Close UAT runtime GA request-visibility gap with smoke validation and checklist hardening

### Phase 04: GDPR Compliance
**Goal**: Respect user privacy by applying consent-based analytics behavior and transparent tracking disclosure.
**Depends on**: Phase 03
**Requirements**: PRIV-01, PRIV-02, PRIV-03
**Success Criteria** (what must be TRUE):
  1. Visitor privacy choice is respected before any analytics tracking runs.
  2. Visitor can change privacy settings after initial selection.
  3. Visitor can access clear information about what data is tracked when consent is granted.
**Plans**: 1 plan
Plans:
- [ ] 04-01-PLAN.md — Implement consent management with library integration and consent-aware analytics behavior
**UI hint**: yes

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 01. Core Publication Surface | 3/3 | Complete   | 2026-04-02 |
| 02. Readability & Accessibility Baseline | 2/2 | Complete | 2026-04-03 |
| 03. Analytics Baseline | 3/3 | Complete   | 2026-04-07 |
| 04. GDPR Compliance | 1/1 | Complete    | 2026-04-09 |
