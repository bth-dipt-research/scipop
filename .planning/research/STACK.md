# Stack Research

**Domain:** Static research-synthesis publishing site (Markdown-first, GitHub Pages, basic analytics)
**Researched:** 2026-04-02
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Astro | `^6.0` (acceptable: `^5.0`) | Static site generation from Markdown/content collections | Best fit for content-heavy static publishing: built-in Markdown + content collections + first-party GitHub Pages deploy docs. Minimal client JS by default, so pages stay fast/readable. **Confidence: HIGH** |
| Node.js | `22 LTS` | Build/runtime for Astro in CI and local dev | Astro’s current engine requirement is Node `>=22.12.0`; aligning on Node 22 avoids CI drift and “works locally, fails in Actions” issues. **Confidence: HIGH** |
| GitHub Pages + GitHub Actions | `actions/checkout@v5`, `actions/upload-pages-artifact@v4`, `actions/deploy-pages@v4` (or `withastro/action@v5`) | Hosting and deployment pipeline | Official GitHub guidance recommends Actions-based publishing for non-Jekyll/custom builds. This is now the standard path for modern static generators on Pages. **Confidence: HIGH** |
| Google Analytics 4 (Google tag / gtag.js) | Current GA4 web tagging | Basic page-level usage analytics | GA4 is the current Analytics model; for MVP-level pageview tracking, a single global site tag in the shared layout is enough (no custom analytics backend/UI). **Confidence: HIGH** |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `@astrojs/sitemap` | `^3.7` | Auto-generate `sitemap-index.xml` and sitemap files | Use by default for public content discoverability and cleaner SEO operations. |
| `@astrojs/mdx` | `^5.0` | MDX support for richer synthesis pages | Use only if syntheses need embedded components/charts in Markdown. Skip for pure `.md` content. |
| `rehype-slug` + `rehype-autolink-headings` | latest compatible | Stable anchor links on long-form pages | Use when syntheses are long and need section deep-linking/table-of-contents UX. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| TypeScript | Typed frontmatter/content schemas | Keep Astro content schemas typed to catch missing metadata during build. |
| Prettier (+ `prettier-plugin-astro`) | Consistent formatting | Prevent noisy PR diffs for Markdown/frontmatter/layout files. |
| GitHub Actions cache | Faster repeat builds | Cache package manager dependencies; improves CI turnaround for content-only updates. |

## Installation

```bash
# Core
npm install astro

# Supporting
npm install @astrojs/sitemap @astrojs/mdx rehype-slug rehype-autolink-headings

# Dev dependencies
npm install -D typescript prettier prettier-plugin-astro
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Astro + content collections | Eleventy (11ty) | Choose Eleventy if your team already has deep 11ty/Nunjucks expertise and wants minimal framework conventions. |
| GitHub Actions artifact deploy | Branch-based deploy (`/docs` or `gh-pages`) | Choose branch deploy only for ultra-simple prebuilt HTML and no build pipeline customization needs. |
| Direct GA4 Google tag in layout | Google Tag Manager | Choose GTM when non-engineers must manage multiple marketing tags frequently. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Universal Analytics (UA) docs/snippets | UA is legacy/deprecated for modern Analytics usage | GA4 Google tag (or GTM with GA4 tag) |
| Ruby/Jekyll as default choice for this milestone | Adds Ruby toolchain and GitHub Pages plugin constraints (`safe: true`, supported plugin set) for a Node-centric content app | Astro + Actions deployment |
| SSR-first framework setup (for this MVP) | Adds runtime complexity and hosting mismatch for a read-only static publication site | Pure static build (Astro default prerender) |

## Stack Patterns by Variant

**If content is mostly finalized Markdown with predictable frontmatter:**
- Use Astro content collections + strict schema validation.
- Because the build should fail fast on missing metadata before publish.

**If pages need richer embeds (interactive figures/components):**
- Add `@astrojs/mdx` only for those sections.
- Because MDX gives flexibility without converting the entire site to client-heavy rendering.

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| `astro@^6.0` | `node@22 LTS` | Astro latest requires Node `>=22.12.0`. Pin CI to Node 22. |
| `@astrojs/mdx@^5.0` | `astro@^6.0` | MDX integration peer-dep aligns with Astro 6 major. |
| `@astrojs/sitemap@^3.7` | `astro@^6.0` | Official Astro integration; generated files rely on configured `site` URL. |

## Prescriptive Recommendation (for roadmap)

Use **Astro 6 + content collections + GitHub Actions Pages deploy + GA4 global tag** as the default stack.

Do **not** start with Jekyll or SSR frameworks for this milestone. The project goal is public, static publication of already-reviewed syntheses, and this stack minimizes moving parts while keeping the door open for richer MDX content later.

## Sources

- Astro docs — GitHub Pages deployment (official action, `site`/`base` config): https://docs.astro.build/en/guides/deploy/github/ (HIGH)
- Astro docs — Content collections and static-first guidance: https://docs.astro.build/en/guides/content-collections/ (HIGH)
- Astro docs — Markdown support and plugin model: https://docs.astro.build/en/guides/markdown-content/ (HIGH)
- Astro docs — `@astrojs/sitemap` integration: https://docs.astro.build/en/guides/integrations-guide/sitemap/ (HIGH)
- GitHub Docs — custom workflows with Pages (`configure-pages`, `upload-pages-artifact`, `deploy-pages`): https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages (HIGH)
- GitHub Docs — publishing source guidance and custom workflow recommendation for non-Jekyll builds: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site (HIGH)
- GitHub Docs — Jekyll on Pages constraints (`safe: true`, plugin limits): https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll (HIGH)
- Google Analytics dev docs — tagging options (Tag Manager vs gtag.js): https://developers.google.com/analytics/devguides/collection/ga4/tag-options (HIGH)
- Google Analytics dev docs — web setup + tagging recommendation context: https://developers.google.com/analytics/devguides/collection/ga4/web (HIGH)
- Google Analytics dev docs — pageview behavior (`send_page_view`, manual control): https://developers.google.com/analytics/devguides/collection/ga4/views (HIGH)
- npm registry metadata — current package versions/engines (`astro`, `@astrojs/mdx`, `@astrojs/sitemap`): https://registry.npmjs.org/astro/latest, https://registry.npmjs.org/@astrojs/mdx/latest, https://registry.npmjs.org/@astrojs/sitemap/latest (MEDIUM)

---
*Stack research for: static research-synthesis publishing sites on GitHub Pages*
*Researched: 2026-04-02*
