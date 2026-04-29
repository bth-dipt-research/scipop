# Requirements: Static scipop

**Defined:** 2026-04-03
**Core Value:** Anyone can reliably access and understand the approved research syntheses through a simple, shareable public website.

## v1 Requirements

Requirements for initial release. Each maps to exactly one roadmap phase.

### Publication

- [x] **PUBL-01**: User can browse a homepage listing all research area clusters
- [x] **PUBL-02**: User can open a dedicated detail page for each research area synthesis via stable URL
- [x] **PUBL-03**: User can open a top-level synthesis page representing the research group as a whole
- [x] **PUBL-04**: User can open a methodology page that explains how syntheses were created and expert-reviewed
- [x] **PUBL-05**: User can read a disclaimer section at the end of each synthesis page
- [x] **PUBL-06**: User can read and navigate all public pages on both desktop and mobile devices
- [x] **UIP-01**: User can read long-form content with polished typography and justified body copy while preserving readability/accessibility baselines
- [x] **UIP-02**: User can see a complete editor profile block (photo, name, email, contact sentence) near the top of each synthesis page
- [x] **UIP-03**: User can navigate with updated IA (`/overview` instead of `/featured`) and use desktop image-map plus mobile fallback homepage navigation

### Analytics

- [x] **ANLT-01**: User visits are tracked with basic Google Analytics pageview events across public pages

### Privacy

- [x] **PRIV-01**: User analytics tracking is gated by explicit consent (no tracking before consent)
- [x] **PRIV-02**: User can revisit and change privacy consent settings at any time
- [x] **PRIV-03**: User can read clear disclosure of what analytics data is tracked when consent is granted

## v2.0 Requirements

Requirements for v2.0 Interactive Topic Modeling milestone. Each maps to exactly one roadmap phase.

### Data Management

- [ ] **TM-01**: User can upload publication data (CSV/XLSX) and preview contents in UI
- [ ] **TM-02**: User can filter publications by type and select input columns for topic modeling

### Model Configuration

- [ ] **TM-03**: User can configure and run topic model with adjustable parameters (UMAP, HDBSCAN, vectorizer, embedding)

### Iterative Refinement

- [ ] **TM-04**: User can adjust UMAP/HDBSCAN parameters to minimize outliers, compare current results against any saved checkpoint, and navigate between workflow steps with automatic checkpoint creation
- [ ] **TM-05**: User can adjust topic labeling verbosity, compare current labels against any saved checkpoint, and navigate between workflow steps with automatic checkpoint creation
- [ ] **TM-06**: User can manually curate topics (merge/remove) with impact preview before applying changes

### Quality & Validation

- [ ] **TM-07**: User can see quality check showing papers with no remaining topics after curation
- [ ] **TM-08**: User can visualize hierarchical topic structure as interactive dendrogram

### Export

- [ ] **TM-09**: User can export topic model results (topic info, papers-with-topics, themed CSVs, trained model, visualization)

## v3+ Requirements

Deferred to future release. Tracked but not in current roadmap.

### Static Site Navigation

- **NAV-01**: User can navigate to related synthesis pages from each detail page

### Advanced Analytics

- **ANLT-02**: User outbound clicks to external references are tracked in Google Analytics

### Trust Signals

- **TRST-01**: User can view references or endnotes for each synthesis page
- **TRST-02**: User can view publish metadata on each synthesis page (author/reviewer and publish/update date)

## Out of Scope

Explicitly excluded for the current project scope.

| Feature | Reason |
|---------|--------|
| Automation pipeline for synthesis generation and publishing | Explicitly deferred until the manual publication MVP proves value |
| User accounts and authentication | Not needed for read-only public publication |
| On-site search and filtering for MVP | Deliberately excluded to keep release focused on publish-and-browse core |
| Custom analytics dashboards | Basic GA pageviews are sufficient for MVP validation |

## Traceability

Which phases cover which requirements. This section is refreshed during roadmap creation.

**v1.0 Requirements (Complete):**

| Requirement | Phase | Status |
|-------------|-------|--------|
| PUBL-01 | Phase 01 | Complete |
| PUBL-02 | Phase 01 | Complete |
| PUBL-03 | Phase 01 | Complete |
| PUBL-04 | Phase 01 | Complete |
| PUBL-05 | Phase 02 | Complete |
| PUBL-06 | Phase 02 | Complete |
| ANLT-01 | Phase 03 | Complete |
| PRIV-01 | Phase 04 | Complete |
| PRIV-02 | Phase 04 | Complete |
| PRIV-03 | Phase 04 | Complete |
| UIP-01 | Phase 05 | Complete |
| UIP-02 | Phase 05 | Complete |
| UIP-03 | Phase 05 | Complete |

**v2.0 Requirements (Pending):**

| Requirement | Phase | Status |
|-------------|-------|--------|
| TM-01 | Phase 06 | Pending |
| TM-02 | Phase 06 | Pending |
| TM-03 | Phase 07 | Pending |
| TM-08 | Phase 08 | Pending |
| TM-04 | Phase 09 | Pending |
| TM-05 | Phase 10 | Pending |
| TM-06 | Phase 11 | Pending |
| TM-07 | Phase 12 | Pending |
| TM-09 | Phase 13 | Pending |

**Coverage:**
- v1.0 requirements: 13 total → 13 mapped ✓
- v2.0 requirements: 9 total → 9 mapped ✓
- Unmapped: 0

---
*Requirements defined: 2026-04-03*
*Last updated: 2026-04-29 for v2.0 milestone roadmap*
