# Feature Research

**Domain:** Public, static research-synthesis websites for general readers  
**Researched:** 2026-04-02  
**Confidence:** MEDIUM

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Topic index homepage (cluster cards + clear titles) | Public readers expect to browse by topic first, not by file name/path | LOW | Aligns directly with your active requirement for index + detail IA |
| One stable detail page per synthesis (clean URL/permalink) | Readers expect each synthesis to be linkable and shareable | LOW | Slug per research area; include canonical URL |
| Plain-language summary at top ("key takeaways") | Research-heavy pages need immediate comprehension for non-experts | LOW | 3–6 bullet takeaways before long-form content |
| Source transparency (references/endnotes + outbound links) | Trust in synthesis content depends on traceable evidence | MEDIUM | Minimum: numbered references section in each synthesis |
| Methodology page (how syntheses were created/reviewed) | Comparable sites expose method and quality controls | LOW | Central page linked globally; include review process and limitations |
| Publish metadata (author/reviewer, published date, last updated) | Users expect recency and accountability signals | LOW | Frontmatter-driven fields rendered on each detail page |
| Related-content navigation (next/related syntheses) | Readers expect cross-topic navigation, not dead-end pages | LOW | Use shared tags/cluster relationships for related links |
| Mobile-first readability + accessibility baseline | General public traffic is mobile-heavy; inaccessible pages reduce trust/reach | MEDIUM | Responsive layout, semantic headings, alt text, contrast, keyboard nav |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Layered reading modes ("2-min brief" + "full synthesis") | Serves skimmers and deep readers without duplicate pages | MEDIUM | Store one source markdown with collapsible/sectioned rendering |
| Evidence confidence panel per synthesis | Makes uncertainty explicit; builds credibility with non-experts | MEDIUM | Show evidence strength + caveats in a compact info box |
| "What changed" changelog per page | Signals editorial rigor and ongoing stewardship | LOW | Static markdown changelog block on each synthesis page |
| Download package per synthesis (Markdown/PDF/citation block) | Increases reuse by educators, journalists, policy readers | MEDIUM | Start with downloadable markdown + copyable citation |
| Reader pathways ("Start here" curated sequences) | Improves comprehension across multiple clusters | MEDIUM | Curated links from top-level synthesis to area syntheses |
| Multilingual summary snippets for top pages | Expands accessibility to broader public audiences | HIGH | Defer full translation; start with short translated abstracts |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Build-time/full-site search for MVP | Users often ask for search immediately | Adds indexing, UX tuning, and relevance work that dilutes publish-first milestone | Start with strong taxonomy + related links + featured pathways; add search in v1.x only if navigation data shows need |
| User accounts, comments, and community features | Seen as engagement boosters | Moderation/compliance burden; conflicts with read-only static publishing goal | Use lightweight feedback/contact link and analytics-informed iteration |
| Auto-regeneration pipeline from raw research | Feels like "complete automation" | Explicitly out of scope; introduces validation and QA risk before publication basics are stable | Keep manual curated publish workflow for MVP; automate post-validation |
| Custom analytics dashboards | Tempting for product insight | High implementation cost with low immediate reader value | Use Google Analytics event/page tracking only in MVP |
| Heavy interactive data explorer in v1 | Looks modern and impressive | Large complexity jump (data pipeline, performance, UX) for limited initial validation value | Embed a small number of static or lightweight interactive visuals only where essential |

## Feature Dependencies

```
[Markdown content model + frontmatter]
    └──requires──> [Detail synthesis pages]
                        └──requires──> [Topic index homepage]

[References/endnotes structure]
    └──requires──> [Methodology page]

[Topic taxonomy/tags]
    └──enhances──> [Related-content navigation]
    └──enhances──> [Reader pathways]

[Publish metadata (date/reviewer/version)]
    └──enhances──> [Evidence confidence panel]
    └──enhances──> [What changed changelog]

[Search MVP]
    └──conflicts──> [Publish-fast scope for this milestone]

[Automation pipeline MVP]
    └──conflicts──> [Manual expert-reviewed publishing milestone]
```

### Dependency Notes

- **Detail synthesis pages require a stable markdown/frontmatter schema:** without consistent fields (title, slug, summary, dates), index and metadata rendering become brittle.
- **Topic index depends on detail pages existing first:** index entries should be generated from valid, published synthesis pages.
- **Methodology and references are coupled:** credibility is stronger when per-page evidence links and site-level method narrative are both present.
- **Taxonomy enables both related links and pathways:** one tagging system supports two UX features, reducing implementation overhead.
- **Search conflicts with publish-first MVP:** relevance tuning and indexing can consume disproportionate effort before core content publishing is validated.

## MVP Definition

### Launch With (v1)

Minimum viable product — what’s needed to validate the concept.

- [ ] Topic index homepage with cluster cards and featured top-level synthesis
- [ ] One dedicated static page per approved synthesis (stable URLs)
- [ ] Plain-language summary + structured sections on each synthesis page
- [ ] References/endnotes section per synthesis page
- [ ] Methodology page describing synthesis + expert-review process
- [ ] Publish metadata (author/reviewer + publish/update dates)
- [ ] Related-content links between syntheses
- [ ] Basic GA tracking (pageviews + outbound link clicks)

### Add After Validation (v1.x)

Features to add once core is working.

- [ ] On-site search/filter — add if analytics shows navigation drop-off or high bounce from index
- [ ] Download/citation toolkit (copy citation, markdown/pdf export) — add when reuse requests become frequent
- [ ] "What changed" page history — add when update cadence increases

### Future Consideration (v2+)

Features to defer until product-market fit is established.

- [ ] Partial multilingual support (starting with abstracts) — defer until stable editorial process exists
- [ ] Interactive data explorer layer — defer until audience demand for deep data interaction is validated
- [ ] Automation from upstream clustering/synthesis pipelines — defer until manual publication quality bar is consistently met

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Topic index homepage | HIGH | LOW | P1 |
| Detail synthesis pages with stable URLs | HIGH | LOW | P1 |
| Plain-language summary blocks | HIGH | LOW | P1 |
| References/endnotes + methodology transparency | HIGH | MEDIUM | P1 |
| Metadata (author/date/updated) | MEDIUM | LOW | P1 |
| Related-content links | MEDIUM | LOW | P1 |
| Search/filter | MEDIUM | MEDIUM | P2 |
| Download/citation toolkit | MEDIUM | MEDIUM | P2 |
| Confidence panels | MEDIUM | MEDIUM | P2 |
| Multilingual abstracts | MEDIUM | HIGH | P3 |
| Interactive data explorer | LOW-MEDIUM | HIGH | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

## Competitor Feature Analysis

| Feature | Competitor A | Competitor B | Our Approach |
|---------|--------------|--------------|--------------|
| Topic-based discovery | **Our World in Data**: strong topic hubs with related topics and data links | **Pew Research Center**: deep topic/format taxonomy and browse structure | Keep simple topic index + featured synthesis in v1; avoid over-complex filtering initially |
| Public-facing methodology transparency | **Cochrane**: explicit explanation of systematic-review method + plain-language summaries | **Pew**: clear “About this research / How did we do this?” blocks + linked methodology docs | Dedicated methodology page + short per-page method note in v1 |
| Evidence traceability and citation | **Our World in Data**: citations, endnotes, reusable licensing/citation guidance | **IPCC**: headline statements linked to report artifacts (SPM/full report/resources) | Mandatory references per synthesis + copyable citation block in v1.x |
| Readability for non-experts | **Cochrane**: plain-language summaries as first-class output | **IPCC**: high-level headline statements before full technical depth | Use layered structure (key takeaways first, full synthesis below) |

## Sources

- Project scope and constraints: `.planning/PROJECT.md` (local project context)
- Our World in Data (topic hub, article structure, citation/reuse patterns):
  - https://ourworldindata.org/energy
  - https://ourworldindata.org/worlds-energy-problem
  - https://ourworldindata.org/about
- Pew Research Center (topic taxonomy, methods transparency, data essay patterns):
  - https://www.pewresearch.org/about/
  - https://www.pewresearch.org/topic/methodological-research/
  - https://www.pewresearch.org/social-trends/2026/03/25/the-united-states-at-250-how-the-country-has-changed-in-the-past-50-years/
- Cochrane (plain-language summaries + evidence trust framing):
  - https://www.cochrane.org/evidence
  - https://www.cochrane.org/about-us
- IPCC (layered report assets, headline statements, summary artifacts):
  - https://www.ipcc.ch/report/ar6/syr/
  - https://www.ipcc.ch/report/ar6/syr/resources/spm-headline-statements/
  - https://www.ipcc.ch/reports/

### Source Confidence Notes

- **MEDIUM confidence overall**: conclusions are grounded in official competitor websites, but discovery breadth is limited because web-search tooling was unavailable in this environment (Google search auth unavailable; Brave API key unavailable).

---
*Feature research for: static research-synthesis publishing websites*
*Researched: 2026-04-02*
