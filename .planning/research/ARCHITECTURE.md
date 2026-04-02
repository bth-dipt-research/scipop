# Architecture Research

**Domain:** Static research-synthesis publication layer (markdown-backed) inside an analysis-first repository
**Researched:** 2026-04-02
**Confidence:** MEDIUM-HIGH

## Standard Architecture

### System Overview

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    Authoring + Repository Layer                     │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐   ┌───────────────────────────────────┐  │
│  │ Analysis artifacts   │   │ Markdown publication content      │  │
│  │ (src/, data/, etc.)  │   │ (cluster syntheses, featured,     │  │
│  └──────────────────────┘   │ methodology, metadata manifests)   │  │
│                             └───────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────────┤
│                        Static Site Build Layer                      │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐   ┌───────────────────────────────────┐  │
│  │ Content schema       │→→ │ Page generation (index + detail   │  │
│  │ validation (Zod)     │   │ pages via file-based routes)      │  │
│  └──────────────────────┘   └───────────────────────────────────┘  │
│               └──────────────→ HTML/CSS/JS static bundle (dist/)   │
├─────────────────────────────────────────────────────────────────────┤
│                      Delivery + Observability Layer                 │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐   ┌───────────────────────────────────┐  │
│  │ GitHub Actions       │→→ │ GitHub Pages CDN                 │  │
│  │ build + deploy       │   │                                  │  │
│  └──────────────────────┘   └───────────────────────────────────┘  │
│                                  ↓                                  │
│                      Google Analytics (GA4 page events)             │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Content source | Canonical research-synthesis text and metadata | Markdown + frontmatter files stored in-repo |
| Content schema layer | Enforce required fields and type safety before publish | Astro Content Collections + Zod schema |
| Page composition layer | Render list/detail/method pages from validated entries | Astro `src/pages`, layouts, and collection queries |
| Static asset layer | Host non-processed files (favicons, CNAME, docs assets) | Astro `public/` |
| Build/deploy pipeline | Build, package, and publish on merge | GitHub Actions + `withastro/action` + `actions/deploy-pages` |
| Analytics layer | Capture page-level usage (MVP scope) | GA4 Google tag in base layout |

## Recommended Project Structure

```text
scipop/
├── src/                              # Existing Python analysis workflows (unchanged)
├── data/                             # Existing analysis inputs/outputs (unchanged)
├── prompts/                          # Existing synthesis prompt assets (unchanged)
├── content/                          # Publication content owned by research/editorial
│   ├── syntheses/
│   │   ├── cluster-a.md
│   │   └── cluster-b.md
│   ├── featured/
│   │   └── research-group.md
│   ├── pages/
│   │   └── methodology.md
│   └── taxonomy/
│       └── clusters.json             # Optional ordering/group metadata
├── site/                             # Isolated static publication app
│   ├── src/
│   │   ├── content.config.ts         # Collection schema + filesystem loaders
│   │   ├── layouts/
│   │   │   └── BaseLayout.astro
│   │   ├── components/
│   │   │   ├── ClusterCard.astro
│   │   │   └── AnalyticsTag.astro
│   │   ├── pages/
│   │   │   ├── index.astro           # Cluster listing homepage
│   │   │   ├── syntheses/[slug].astro
│   │   │   ├── featured/index.astro
│   │   │   └── methodology.astro
│   │   └── styles/
│   ├── public/
│   │   └── CNAME                     # Optional custom domain
│   ├── astro.config.mjs
│   └── package.json
└── .github/workflows/deploy-site.yml # Build/deploy workflow targeting /site
```

### Structure Rationale

- **`site/` subproject boundary:** Keeps Node/Astro toolchain isolated from Python analysis runtime. This is the cleanest integration model for mixed-language repos.
- **Top-level `content/` boundary:** Lets researchers edit markdown without touching site internals; site consumes content via filesystem loader.
- **`content.config.ts` contract-first design:** Fails build when frontmatter is invalid, preventing silent broken pages.

## Content Model (Opinionated)

Use **three collections** plus optional taxonomy metadata:

1. **`syntheses`** (many): one per research area/cluster
   - Required frontmatter: `title`, `slug`, `cluster_id`, `summary`, `reviewed_at`, `status` (`approved|draft`), `order`
2. **`featured`** (one in MVP): research-group-level synthesis
   - Required: `title`, `slug`, `summary`, `reviewed_at`
3. **`pages`** (few fixed docs): methodology and about-like static pages
   - Required: `title`, `slug`

Optional `taxonomy/clusters.json` can hold display labels, ordering, or color tokens independent of editorial markdown.

## Architectural Patterns

### Pattern 1: Contract-Validated Markdown Collections

**What:** Markdown is treated like structured data via schema validation at build time.
**When to use:** Always, because publication quality and consistency matter more than authoring flexibility.
**Trade-offs:** Slightly stricter author workflow; major gain in reliability.

**Example:**
```ts
// site/src/content.config.ts
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const syntheses = defineCollection({
  loader: glob({ base: '../content/syntheses', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    cluster_id: z.string(),
    summary: z.string(),
    reviewed_at: z.coerce.date(),
    status: z.enum(['approved', 'draft']).default('draft'),
    order: z.number().int().nonnegative(),
  }),
});

export const collections = { syntheses };
```

### Pattern 2: Generated Routes from Content (No Manual Route Registry)

**What:** Dynamic detail pages are generated from collection entries.
**When to use:** Any repeatable content type (cluster detail pages).
**Trade-offs:** Requires deterministic slug governance.

**Example:**
```ts
// site/src/pages/syntheses/[slug].astro
export async function getStaticPaths() {
  const entries = await getCollection('syntheses', ({ data }) => data.status === 'approved');
  return entries.map((e) => ({ params: { slug: e.data.slug } }));
}
```

### Pattern 3: Layout-Level Analytics Injection

**What:** Inject GA tag once in shared layout, not per page.
**When to use:** Always for page-level analytics in static MPA sites.
**Trade-offs:** Requires env-variable management in CI.

## Data Flow

### Markdown-to-Published-Page Flow (direction explicit)

```text
Researcher edits markdown in /content
    ↓
Git commit/merge to main
    ↓
GitHub Actions workflow triggers
    ↓
Astro build loads content via glob() loader
    ↓
Zod schema validates frontmatter (fail-fast on invalid entries)
    ↓
Route generation (index + dynamic synthesis pages)
    ↓
Static bundle emitted to site/dist
    ↓
Artifact deploy to GitHub Pages
    ↓
Public pages served via Pages CDN
    ↓
Client browser loads GA tag and emits page_view events to GA4
```

### Key Data Flows

1. **Editorial flow:** Markdown/frontmatter → schema validation → rendered HTML.
2. **Navigation flow:** Synthesis collection query → sorted list model → homepage cards/links.
3. **Analytics flow:** Base layout script + measurement ID → page_view events in GA4.

## Deployment Flow (GitHub Pages)

Recommended pipeline:

1. Trigger on pushes to `main` (or release branch).
2. Build inside `site/` using Astro GitHub Action.
3. Ensure `site` and `base` are configured correctly for Pages URL/repo path.
4. Deploy artifact with `actions/deploy-pages`.

For monorepo compatibility, set workflow path input so only `site/` is built.

## Analytics Wiring (MVP scope)

- Use **GA4 Google tag** in `BaseLayout.astro`.
- Configure measurement ID via env var (e.g., `PUBLIC_GA_MEASUREMENT_ID`).
- For multi-page static sites, default `page_view` behavior is sufficient.
- Only disable `send_page_view` and manually emit events if introducing SPA-style navigation later.

## Build Order Implications (for roadmap phasing)

1. **Phase A — Content contract first**
   - Define frontmatter schema + content directories + slug policy.
   - Why first: every page template depends on stable content shape.

2. **Phase B — Core page generation**
   - Implement homepage list, synthesis detail route, featured page, methodology page.
   - Why second: establishes the publishable product skeleton.

3. **Phase C — Deployment pipeline**
   - Add GitHub Pages workflow, `site/base` config, first successful public deploy.
   - Why third: validates end-to-end markdown→public URL path.

4. **Phase D — Analytics + hardening**
   - Add GA4 wiring, draft filtering, content QA checks, 404/redirect polish.
   - Why fourth: instrumentation should follow stable routing and deployment.

## Anti-Patterns

### Anti-Pattern 1: Mixing website source into existing Python `src/`

**What people do:** Add frontend code directly into analysis runtime folders.
**Why it’s wrong:** Increases coupling, dependency conflicts, and cognitive load.
**Do this instead:** Keep `site/` isolated; interface only through `/content` files.

### Anti-Pattern 2: Unvalidated frontmatter

**What people do:** Trust ad hoc markdown metadata and patch template errors later.
**Why it’s wrong:** Breaks builds unpredictably and creates brittle templates.
**Do this instead:** Enforce schema in content collections; fail fast in CI.

### Anti-Pattern 3: Per-page analytics snippets

**What people do:** Copy analytics script into each page/template.
**Why it’s wrong:** Drift and duplicate events over time.
**Do this instead:** Single layout-level injection + env-based measurement ID.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| GitHub Pages | CI artifact deployment | Configure `base` for repo-name path when needed |
| GitHub Actions | Build + deploy orchestration | Use official Pages deploy actions and proper permissions |
| Google Analytics 4 | Client-side tag in base layout | Respect consent/privacy obligations |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| `content/` ↔ `site/src/content.config.ts` | Filesystem loader + schema | Main contract boundary between researchers and site code |
| `site/src/pages` ↔ `site/src/layouts/components` | Props + render composition | Keep page files thin; put shared behavior in layout/components |
| Existing analysis pipeline (`src/`, `data/`) ↔ publication layer | Manual editorial handoff (MVP) | Automation intentionally deferred by project scope |

## Sources

- Astro docs — Content collections (build-time loaders, schemas, route generation): https://docs.astro.build/en/guides/content-collections/ (official)
- Astro docs — Routing and dynamic `getStaticPaths()`: https://docs.astro.build/en/guides/routing/ (official)
- Astro docs — Project structure and `public/` handling: https://docs.astro.build/en/basics/project-structure/ (official)
- Astro docs — Markdown behavior and frontmatter/layout details: https://docs.astro.build/en/guides/markdown-content/ (official)
- Astro docs — GitHub Pages deployment (`site`, `base`, action): https://docs.astro.build/en/guides/deploy/github/ (official)
- GitHub Docs — Custom workflows for Pages deploy permissions/artifact model: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages (official)
- Google Analytics docs — Tagging options and GA4 page view behavior: https://developers.google.com/analytics/devguides/collection/ga4/tag-options and https://developers.google.com/analytics/devguides/collection/ga4/views (official)

---
*Architecture research for: static research-synthesis publication layer*
*Researched: 2026-04-02*
