# Pitfalls Research

**Domain:** Static public websites for expert-reviewed research synthesis
**Researched:** 2026-04-02
**Confidence:** MEDIUM

## Critical Pitfalls

### Pitfall 1: Treating accessibility as a QA checkbox at the end

**What goes wrong:**
The site launches with inaccessible reading/navigation patterns (weak heading structure, non-descriptive links, poor keyboard focus behavior, missing alt text/captions), even if content quality is high.

**Why it happens:**
Teams assume static = simple, so they defer accessibility until pre-launch and rely mostly on automated checks.

**How to avoid:**
- Set WCAG 2.2 AA as an explicit non-negotiable release criterion.
- Bake semantic content rules into templates (single H1, heading hierarchy, meaningful link text, image alt requirements, media transcripts/captions).
- Run both automated and manual checks (keyboard-only navigation, zoom/reflow, screen reader spot checks) in every content release cycle.

**Warning signs:**
- Accessibility issues are filed only in “polish” phase.
- Authors/editors can publish pages with missing alt text or skipped heading levels.
- “Passes Lighthouse” is used as the only acceptance evidence.

**Phase to address:**
Phase 1 (Foundations: content model + templates) and Phase 2 (Accessibility verification before launch)

---

### Pitfall 2: Publishing synthesis without visible provenance and review metadata

**What goes wrong:**
Readers cannot tell who wrote/reviewed content, when it was published/updated, or how conclusions were produced. Trust drops, especially for high-impact topics.

**Why it happens:**
Teams focus on prose quality but omit trust scaffolding (author/reviewer identity, methodology, source links, update history, uncertainty notes).

**How to avoid:**
- Require per-page trust metadata: author(s), reviewer(s), published date, last updated date, methodology link, and source references.
- Add machine-readable metadata (`Article` schema with `author`, `datePublished`, `dateModified`) plus matching visible dates.
- Include explicit uncertainty/disagreement sections in synthesis pages.

**Warning signs:**
- Pages have no byline or only organization-level authorship.
- Dates exist in page frontmatter but are not shown to users.
- “Expert-reviewed” is claimed without naming reviewer role/process.

**Phase to address:**
Phase 1 (Content schema + editorial policy) and Phase 3 (Trust & transparency layer)

---

### Pitfall 3: “Freshness theater” instead of real content governance

**What goes wrong:**
Pages look current (new timestamps) without substantive updates; citations age out; contradictory or superseded claims remain live.

**Why it happens:**
No ownership model or review cadence per synthesis page; update dates are treated as cosmetic SEO signals.

**How to avoid:**
- Create an ownership + review SLA per page (owner, review interval, expiry trigger).
- Use a “substantive change required” rule before changing `last updated` date.
- Add stale-content flags and archival rules (e.g., “under review”, “superseded by version X”).

**Warning signs:**
- Date changes with no changelog or content diff.
- Growing number of broken source links/citations.
- No one can answer “who owns this page now?”

**Phase to address:**
Phase 4 (Operational governance and maintenance runbook)

---

### Pitfall 4: GitHub Pages path/build assumptions causing broken public site behavior

**What goes wrong:**
Site deploys, but navigation/assets fail (404s, wrong base paths, missing index/docs source, custom-domain routing regressions).

**Why it happens:**
Teams test locally at root path, then deploy as project site (`/<repo>`) or change publishing source/domain without validating path behavior.

**How to avoid:**
- Decide early: user/org site vs project site URL model.
- Standardize link generation through static-site link helpers (avoid hardcoded absolute paths).
- Add deploy smoke tests for homepage, cluster pages, synthesis detail pages, methodology page, and static assets after every publish.
- Track GitHub Pages limits (build time, site size, bandwidth) and use Actions-based deploy if needed.

**Warning signs:**
- Works locally, fails only after Pages deploy.
- Intermittent 404s after domain or branch/source changes.
- Hardcoded `/` paths in templates/content.

**Phase to address:**
Phase 2 (Deployment architecture) and Phase 5 (Post-deploy verification automation)

---

### Pitfall 5: Analytics instrumentation that undermines user trust/privacy

**What goes wrong:**
Basic GA is added in a way that conflicts with user consent expectations or policy requirements, creating trust and compliance risk.

**Why it happens:**
“Just drop GA script” mindset, no consent mode integration, no explicit data-minimization decision.

**How to avoid:**
- Define analytics policy before implementation (what is measured, legal basis, retention boundaries, no-PII rule).
- Implement consent handling deliberately (default state + consent updates; region-aware behavior where applicable).
- Verify no accidental PII in URLs/events and document measurement behavior publicly.

**Warning signs:**
- GA present but no consent flow/spec.
- Event names/params include identifiable text inputs.
- Team cannot explain what data is collected when consent is denied.

**Phase to address:**
Phase 3 (Trust/privacy policy) and Phase 5 (Instrumentation + audit)

---

### Pitfall 6: Overly academic writing for a general audience

**What goes wrong:**
Public readers bounce because synthesis pages are dense, jargon-heavy, and hard to scan, despite being factually strong.

**Why it happens:**
Source material style is preserved without adaptation for web reading and accessibility-oriented plain language.

**How to avoid:**
- Enforce plain-language editorial standards: concise lead summary, progressive disclosure, glossary for domain terms.
- Use scannable structure: clear headings, meaningful links, short paragraphs, bullet summaries.
- Add “quick read” layer at top of each synthesis (what’s known, confidence, limitations, implications).

**Warning signs:**
- Long unbroken sections with no summary boxes.
- User testing feedback: “too technical” / “don’t know where to start.”
- High exit rates from synthesis detail pages.

**Phase to address:**
Phase 1 (Content design system) and Phase 3 (Editorial quality gate)

---

## Technical Debt Patterns

Shortcuts that feel fast in MVP but hurt trust and maintainability.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hardcode page URLs in markdown/templates | Fast initial publish | Broken links after IA/path changes | Only for throwaway prototype, not MVP release |
| Copy-paste per-page metadata manually | No schema work now | Inconsistent bylines/dates/reviewer fields | Never for expert-reviewed publication |
| Manual post-deploy checking only | No CI setup time | Repeated regressions and silent 404s | Only for first internal dry-run |
| Update “last updated” without changelog | Looks fresh quickly | Trust erosion when changes are unverifiable | Never |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| GitHub Pages | Misconfigured publishing source (`/docs` removed, wrong branch) | Lock source strategy and monitor Pages workflow/build logs |
| GitHub Pages + custom domain | Domain switch without rebuild/path validation | Rebuild + run route smoke tests + verify canonical URL behavior |
| GA4 | Load tracking without explicit consent design | Implement consent mode flow and document expected behavior per consent state |
| Structured data | Add JSON-LD that conflicts with visible metadata | Keep visible byline/date and structured data values consistent |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Shipping oversized media/files in static repo | Slow page loads, failed build budgets | Optimize assets, cap image dimensions, precompress static files | Usually noticeable by first public launch on mobile networks |
| Relying on default Pages build for growing content sets | Slow or timed-out deploys | Move to explicit GitHub Actions build pipeline with artifact deploy | As content volume approaches Pages size/build limits |
| No broken-link checks on release | Trust-impacting dead citations/navigation | Add link-check CI and fail release on critical link errors | Starts small, compounds quickly with each publication cycle |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Publishing private notes/reviewer comments in repo-backed site content | Accidental disclosure of internal deliberation | Separate public vs internal content folders and enforce pre-publish checks |
| Allowing PII in analytics event payloads or query params | Privacy/legal exposure | Ban PII in tracking schema; lint event definitions; review URL/query handling |
| Treating static hosting as “no security work needed” | Unmanaged dependency/template vulnerabilities | Keep static-site generator/theme dependencies patched and audited |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| No clear “methodology + limitations” entry point | Readers mistrust conclusions | Prominent methodology and limitations links on every synthesis page |
| Unclear cluster navigation and hierarchy | Users cannot discover related syntheses | Consistent index/detail IA with breadcrumbs and related-links blocks |
| Long-form synthesis with no summary layer | Non-experts abandon quickly | Add executive summary + key takeaways + confidence labels at top |

## "Looks Done But Isn't" Checklist

- [ ] **Synthesis page template:** Includes visible byline, reviewer, published date, updated date, and methodology link.
- [ ] **Accessibility:** Keyboard-only, heading structure, contrast, alt text, and link purpose checks completed on representative pages.
- [ ] **Deployment:** Public URL smoke-tested for all core routes after deploy (home, cluster, detail, methodology, featured synthesis).
- [ ] **Trust metadata:** Structured data values (`author`, `datePublished`, `dateModified`) match visible page metadata.
- [ ] **Analytics:** Consent behavior validated and no PII in events/URLs.
- [ ] **Maintenance:** Each published page has an owner and next-review date.

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Missing trust/provenance metadata across pages | MEDIUM | Define canonical metadata schema, backfill all published pages, add CI checks |
| Accessibility regressions post-launch | HIGH | Triage by severity, patch templates first, re-audit representative sample before next release |
| Widespread broken links after URL/path change | MEDIUM | Add redirects where possible, regenerate links via helpers, run full link validation |
| Privacy issue in analytics implementation | HIGH | Disable affected tracking, remove offending fields, publish remediation note, re-enable with tested consent config |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Accessibility treated as late QA | Phase 1-2 | WCAG AA acceptance gates + manual test evidence in release checklist |
| Missing provenance/review metadata | Phase 1 & 3 | Every synthesis page renders required trust fields and methodology links |
| Freshness theater / stale content | Phase 4 | Owner + review date present; update-date changes tied to changelog entries |
| GitHub Pages path/build breakage | Phase 2 & 5 | Post-deploy smoke tests and zero critical 404s |
| Privacy-eroding analytics | Phase 3 & 5 | Consent behavior test cases pass; no PII in event payload audits |
| Overly academic UX for general public | Phase 1 & 3 | Readability/editorial QA checklist passed on sampled pages |

## Sources

- W3C WCAG 2.2 (Recommendation, updated 2024-12-12): https://www.w3.org/TR/WCAG22/  
  (HIGH confidence for accessibility conformance expectations)
- W3C Writing for Web Accessibility (updated 2024-07-16): https://www.w3.org/WAI/tips/writing/  
  (HIGH confidence for content clarity/accessibility practices)
- W3C WCAG-EM Overview (updated 2026-02-05): https://www.w3.org/WAI/test-evaluate/conformance/wcag-em/  
  (HIGH confidence for evaluation methodology and lifecycle integration)
- W3C Accessibility Statements guidance: https://www.w3.org/WAI/planning/statements/  
  (MEDIUM confidence; page older but still normative guidance context)
- GitHub Pages overview, config, troubleshooting, limits:  
  https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages  
  https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site  
  https://docs.github.com/en/pages/getting-started-with-github-pages/troubleshooting-404-errors-for-github-pages-sites  
  https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits  
  (HIGH confidence for deployment/hosting pitfalls)
- Jekyll link tag validation and path handling: https://jekyllrb.com/docs/liquid/tags/#links  
  (HIGH confidence for Jekyll-based static link robustness)
- Google Search Central: helpful, reliable content + trust signals (updated 2025-12-10):  
  https://developers.google.com/search/docs/fundamentals/creating-helpful-content  
  https://developers.google.com/search/docs/appearance/publication-dates  
  https://developers.google.com/search/docs/appearance/structured-data/article  
  (MEDIUM-HIGH confidence for trust/provenance discoverability patterns)
- Google Analytics consent mode docs: https://support.google.com/analytics/answer/9976101  
  (MEDIUM confidence for consent/measurement implementation pitfalls)

---
*Pitfalls research for: static expert-reviewed synthesis publication sites*
*Researched: 2026-04-02*
