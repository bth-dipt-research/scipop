# Project Research Summary

**Project:** Static scipop
**Domain:** Static, public research-synthesis publishing website (Markdown-first)
**Researched:** 2026-04-03
**Confidence:** MEDIUM-HIGH

## Executive Summary

This project is a **static publication product**, not a data app: the fastest credible path is to publish already-reviewed syntheses in a browseable, linkable format for general readers. Across the research, expert teams solve this with a strict content contract (typed frontmatter + schema validation), generated index/detail pages, and a low-complexity deployment target (GitHub Pages via Actions). The recommended implementation is Astro 6 in an isolated `site/` subproject, consuming top-level Markdown content collections and deploying static artifacts.

The strongest recommendation is to sequence work as: **content contract first, page generation second, deployment third, trust/analytics hardening fourth**. This ordering matches dependency reality: without stable metadata and slugs, index generation, provenance display, related links, and analytics instrumentation all become brittle. MVP should focus on table stakes (index, detail pages, methodology, metadata, references, related navigation, basic GA) and defer search, automation, and heavy interactivity until real user behavior justifies them.

Key risks are trust erosion (missing provenance/update clarity), accessibility failures from late QA, GitHub Pages path misconfiguration, and privacy mistakes in analytics setup. Mitigation is clear and testable: enforce required metadata and editorial gates in schema/templates, treat WCAG 2.2 AA as release criteria, smoke-test deployed routes/assets on every release, and define analytics consent/data-minimization policy before turning on tracking.

## Key Findings

### Recommended Stack

The stack research is high-confidence and strongly converges on Astro + GitHub Pages Actions + GA4 for MVP static publication. This stack minimizes runtime complexity, aligns with official deployment guidance, and keeps future expansion possible (MDX, richer components) without overbuilding now.

**Core technologies:**
- **Astro `^6.0` (acceptable `^5.0`)**: static site generation from Markdown/content collections — best fit for content-heavy publishing with minimal client JS.
- **Node.js 22 LTS**: build/runtime baseline — required to satisfy Astro engine constraints and avoid CI/local drift.
- **GitHub Pages + Actions** (`checkout@v5`, `upload-pages-artifact@v4`, `deploy-pages@v4` or `withastro/action@v5`): hosting/deploy pipeline — official modern pattern for non-Jekyll static builds.
- **GA4 (gtag.js)**: basic page/outbound analytics — sufficient for MVP validation without building custom analytics infrastructure.

Critical version requirement: pin CI/runtime to **Node >=22.12** for Astro 6 compatibility.

### Expected Features

Feature research identifies a clear MVP centered on trustable publication UX, not feature breadth.

**Must have (table stakes):**
- Topic index homepage with cluster cards and clear discovery
- Stable permalink detail page per synthesis
- Plain-language key takeaways at top of each synthesis
- References/endnotes and a globally visible methodology page
- Visible publish metadata (author/reviewer, published/updated)
- Related-content navigation
- Mobile-first accessibility baseline
- Basic GA tracking (pageviews + outbound clicks)

**Should have (competitive):**
- Layered reading modes (quick brief + full synthesis)
- Evidence-confidence panel per page
- Per-page “what changed” history
- Download/citation package
- Curated “start here” pathways

**Defer (v2+):**
- Multilingual support beyond limited summary snippets
- Interactive data explorer
- Automatic regeneration pipeline from upstream research workflows
- Accounts/comments and custom analytics dashboards

### Architecture Approach

Architecture research recommends a **contract-first, monorepo-separated design**: keep Astro in `site/`, keep editorial Markdown in top-level `content/`, and enforce frontmatter contracts in `site/src/content.config.ts` using Astro collections + Zod. Pages should be generated from content (not manually registered), deployment should be artifact-based GitHub Actions to Pages, and GA should be injected once at layout level. This preserves clean boundaries with existing Python analysis code while enabling reliable publication operations.

**Major components:**
1. **Content source (`content/`)** — canonical synthesis text + metadata owned by editorial/research.
2. **Schema/collection layer (`content.config.ts`)** — validation gate for required fields, status, slugs, and ordering.
3. **Page composition layer (`site/src/pages` + layouts/components)** — index/detail/featured/methodology generation and rendering.
4. **Build/deploy layer (`.github/workflows/deploy-site.yml`)** — deterministic build and Pages artifact publish.
5. **Observability layer (GA4 in base layout)** — lightweight behavior telemetry for iteration.

### Critical Pitfalls

1. **Late accessibility treatment** — prevent by making WCAG 2.2 AA a release gate and running manual + automated checks each cycle.
2. **Missing provenance/review metadata** — prevent by requiring visible byline/reviewer/dates/methodology + structured metadata parity.
3. **Freshness theater (cosmetic updates)** — prevent with page ownership, review SLAs, and “substantive change required” update rules.
4. **GitHub Pages path/build breakage** — prevent via early URL model decision, link helper usage, and post-deploy smoke tests.
5. **Privacy-risk analytics implementation** — prevent with explicit consent/data-minimization policy and PII-free event discipline.

## Implications for Roadmap

Based on combined findings, suggested phase structure:

### Phase 1: Content Contract & Editorial Trust Foundation
**Rationale:** All downstream rendering and governance depend on stable metadata and content shape.
**Delivers:** Collection schemas, slug policy, required metadata fields, plain-language template rules, accessibility-aware content patterns, methodology content contract.
**Addresses:** Detail page prerequisites, metadata, references coupling, plain-language summary expectations.
**Avoids:** Unvalidated frontmatter, missing provenance, overly academic UX, late accessibility debt.

### Phase 2: Core Publication Experience (Index + Detail + Methodology + Featured)
**Rationale:** Validates the core user value quickly with publishable pages from approved content.
**Delivers:** Topic index, synthesis detail routes, featured synthesis page, methodology page, related-content links, responsive accessible baseline UI.
**Uses:** Astro collections/routes/layout composition patterns.
**Avoids:** Dead-end navigation, brittle manual route registration, incomplete table-stakes MVP.

### Phase 3: Deployment Reliability on GitHub Pages
**Rationale:** Public value is only realized after stable URL delivery and reproducible CI deploys.
**Delivers:** Actions-based build/deploy pipeline, `site/base` correctness, first public deploy, deploy smoke tests for core routes/assets.
**Uses:** Official Pages artifact workflow and Astro GitHub deploy conventions.
**Avoids:** Local-vs-production path drift, broken assets/404s after publish.

### Phase 4: Trust, Transparency & Analytics Hardening
**Rationale:** After stable routing, add confidence/measurement features without destabilizing core publication.
**Delivers:** GA4 layout-level integration, outbound click events, consent-aware instrumentation plan, structured data parity, uncertainty/confidence panel, optional changelog block.
**Addresses:** Differentiators and trust scaffolding.
**Avoids:** Privacy-eroding analytics, trust gaps from opaque methodology or stale metadata.

### Phase 5: Operational Governance & Iteration Loop
**Rationale:** Sustained credibility requires ongoing ownership and quality controls.
**Delivers:** Page ownership + review cadence, stale-content flags, broken-link checks, maintenance checklist, phase-gated v1.x decisions (search/download toolkit).
**Addresses:** Freshness governance and post-launch quality.
**Avoids:** “Looks done but isn’t” regressions and compounding citation/navigation debt.

### Phase Ordering Rationale

- Dependencies run from **contract → pages → deploy → instrumentation/governance**; reversing this order creates avoidable rework.
- One taxonomy/metadata system powers multiple features (index, related links, pathways, confidence/changelog), so model quality should precede UI breadth.
- Risk-heavy concerns (privacy consent, stale-content governance) are best introduced once baseline publishing is stable and observable.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 4:** Consent-mode/legal interpretation by target audience geography (policy/compliance specifics not fully resolved in current research set).
- **Phase 5:** Search introduction criteria and implementation choice (only add if analytics indicates navigation failure; requires decision research at that time).
- **Future v2 multilingual:** Editorial workflow + quality control model needs dedicated research before execution.

Phases with standard patterns (can likely skip extra research-phase):
- **Phase 1-3 core stack and deployment:** Strong official docs coverage (Astro, GitHub Pages, GA4 baseline) and clear established patterns.
- **Core IA/MVP feature set:** Sufficiently validated by competitor pattern review and project constraints.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Based mostly on official Astro/GitHub/Google docs and explicit version constraints. |
| Features | MEDIUM | Good competitor grounding, but breadth limited by constrained discovery tooling in research run. |
| Architecture | MEDIUM-HIGH | Strong alignment with Astro docs and monorepo boundary best practices; some choices remain opinionated. |
| Pitfalls | MEDIUM | High-quality standards/docs used, but some governance/privacy practices are context-dependent and need local policy decisions. |

**Overall confidence:** MEDIUM-HIGH

### Gaps to Address

- **Consent/compliance scope:** Confirm jurisdiction-specific consent requirements and desired consent UX before GA rollout.
- **Definition of “approved” editorial status:** Finalize reviewer roles, approval workflow, and publish gate ownership in process docs.
- **Search threshold policy:** Set measurable triggers (bounce/drop-off targets) that justify moving search from deferred to active.
- **Structured data depth:** Decide whether MVP includes only Article-level metadata or richer schema extensions.

## Sources

### Primary (HIGH confidence)
- Astro official docs (content collections, markdown, routing, project structure, GitHub deploy, sitemap): https://docs.astro.build/
- GitHub Pages official docs (custom workflows, publishing sources, limits, troubleshooting): https://docs.github.com/en/pages/
- Google Analytics developer docs (GA4 tagging options, web setup, page views): https://developers.google.com/analytics/devguides/collection/ga4/
- W3C WCAG 2.2 + WAI guidance (accessibility conformance and evaluation): https://www.w3.org/TR/WCAG22/ and https://www.w3.org/WAI/

### Secondary (MEDIUM confidence)
- Competitor pattern sampling (Our World in Data, Pew, Cochrane, IPCC) for IA/readability/transparency conventions.
- npm registry metadata for package/version compatibility checks.
- Google Search Central guidance for publication date/trust signal framing.

### Tertiary (LOW confidence)
- None explicitly used as sole basis for critical decisions.

---
*Research completed: 2026-04-03*
*Ready for roadmap: yes*
