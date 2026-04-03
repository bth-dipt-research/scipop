# Phase 3: Analytics Baseline - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-03
**Phase:** 03-analytics-baseline
**Areas discussed:** Tracking scope, Script loading behavior, Config and deployment, Verification workflow

---

## Tracking scope

### Q1. Which routes should be required for Phase 3 pageview coverage?

| Option | Description | Selected |
|--------|-------------|----------|
| All public routes (Recommended) | Track pageviews on `/`, `/featured`, `/methodology`, and every approved `/syntheses/{slug}`; matches success criteria. | ✓ |
| Core pages only | Track only `/`, `/featured`, and `/methodology`. | |
| Synthesis pages only | Track only `/syntheses/{slug}` and `/featured`. | |
| You decide | Leave route coverage to implementation discretion. | |

**User's choice:** All public routes (Recommended)

### Q2. How should URL details be handled in the pageview path value?

| Option | Description | Selected |
|--------|-------------|----------|
| Ignore query/hash (Recommended) | Track canonical route path only for cleaner reports. | ✓ |
| Include query/hash | Track full URL details for more granularity and more fragmentation. | |
| Keep query only | Include query parameters, ignore hash fragments. | |
| You decide | Leave URL normalization details to implementation. | |

**User's choice:** Ignore query/hash (Recommended)

### Q3. Which navigation scenarios should trigger a pageview event?

| Option | Description | Selected |
|--------|-------------|----------|
| Full page loads only (Recommended) | Align with current Astro navigation and avoid duplicate event complexity. | ✓ |
| Load + history changes | Add future-proof handling for client-side navigation changes. | |
| Per-page manual calls | Emit events from each page template directly. | |
| You decide | Leave trigger strategy to implementation. | |

**User's choice:** Full page loads only (Recommended)

### Q4. For Phase 3, should we track only pageviews or add other analytics events too?

| Option | Description | Selected |
|--------|-------------|----------|
| Pageviews only (Recommended) | Keep scope to `ANLT-01` baseline telemetry. | ✓ |
| Add outbound clicks | Expand toward deferred `ANLT-02`. | |
| Add nav interactions | Broaden event scope beyond baseline. | |
| You decide | Leave extra events to implementation. | |

**User's choice:** Pageviews only (Recommended)
**Notes:** Area considered complete; user moved to next area.

---

## Script loading behavior

### Q1. Where should the GA bootstrap script be integrated?

| Option | Description | Selected |
|--------|-------------|----------|
| BaseLayout head (Recommended) | Inject once in `site/src/layouts/BaseLayout.astro` for shared coverage. | ✓ |
| Per-page templates | Add script separately in each page template. | |
| Standalone include module | Create shared analytics partial/module and import as needed. | |
| You decide | Leave placement strategy to implementation. | |

**User's choice:** BaseLayout head (Recommended)

### Q2. What loading strategy should we use for the GA library script?

| Option | Description | Selected |
|--------|-------------|----------|
| Async script (Recommended) | Use standard async head snippet to avoid render blocking. | ✓ |
| Defer script | Run after parse; possibly later initialization. | |
| Body-end script | Load at end of body with later startup. | |
| You decide | Leave loading details to implementation. | |

**User's choice:** Async script (Recommended)

### Q3. How should the initial pageview be emitted on each page load?

| Option | Description | Selected |
|--------|-------------|----------|
| Use gtag config (Recommended) | Standard `gtag('config', MEASUREMENT_ID, ...)` initialization flow. | ✓ |
| Manual page_view call | Disable auto pageview and emit explicitly. | |
| Config + manual | Use both and guard against duplicate events. | |
| You decide | Leave initialization style to implementation. | |

**User's choice:** Use gtag config (Recommended)

### Q4. Which privacy-safe defaults should we set in the baseline GA config?

| Option | Description | Selected |
|--------|-------------|----------|
| Anonymize + no ads (Recommended) | Use IP anonymization and disable ad-personalization-oriented flags. | ✓ |
| GA defaults | Use vanilla GA config values. | |
| Only anonymize IP | Enable anonymize_ip only. | |
| You decide | Leave privacy flags to implementation. | |

**User's choice:** Anonymize + no ads (Recommended)
**Notes:** Area considered complete; user moved to next area.

---

## Config and deployment

### Q1. How should the GA measurement ID be provided to the site?

| Option | Description | Selected |
|--------|-------------|----------|
| Public env var (Recommended) | Use public build-time env var (e.g., `PUBLIC_GA_MEASUREMENT_ID`). | ✓ |
| Hardcode in layout | Put measurement ID directly in source template. | |
| Content/config file | Read ID from tracked build config/content. | |
| You decide | Leave sourcing approach to implementation. | |

**User's choice:** Public env var (Recommended)

### Q2. If the measurement ID is missing during a production build, what should happen?

| Option | Description | Selected |
|--------|-------------|----------|
| Fail build (Recommended) | Block release when required telemetry config is missing. | ✓ |
| Build with warning | Continue build, disable tracking, warn only. | |
| Use placeholder ID | Fall back to dummy value. | |
| You decide | Leave missing-ID behavior to implementation. | |

**User's choice:** Fail build (Recommended)

### Q3. Should telemetry run outside production builds (local dev/preview)?

| Option | Description | Selected |
|--------|-------------|----------|
| Production only (Recommended) | Avoid noisy internal/preview traffic in GA reports. | ✓ |
| Prod + preview | Include preview environments in telemetry stream. | |
| All environments | Track local, preview, and production. | |
| You decide | Leave environment gating to implementation. | |

**User's choice:** Production only (Recommended)

### Q4. Where should the production measurement ID be managed for GitHub Pages publishing?

| Option | Description | Selected |
|--------|-------------|----------|
| GitHub repo variable (Recommended) | Keep deployment config in repository CI/CD variables/secrets. | ✓ |
| Tracked env file | Commit value in source-controlled env/config file. | |
| Manual CLI export | Set value manually for each deploy command. | |
| You decide | Leave deployment-value management to implementation. | |

**User's choice:** GitHub repo variable (Recommended)
**Notes:** Area considered complete; user moved to next area.

---

## Verification workflow

### Q1. What should Phase 3 verification include?

| Option | Description | Selected |
|--------|-------------|----------|
| Automated + manual (Recommended) | Combine build checks with GA UI validation to satisfy both success criteria. | ✓ |
| Automated only | Use local/build checks only. | |
| Manual only | Use GA UI checks only, no script enforcement. | |
| You decide | Leave verification approach to implementation. | |

**User's choice:** Automated + manual (Recommended)

### Q2. What should the automated verification script check in built routes?

| Option | Description | Selected |
|--------|-------------|----------|
| Snippet on required routes (Recommended) | Verify GA snippet/config appears on all required route artifacts. | ✓ |
| Home page only | Verify snippet only on homepage. | |
| Route list only | Verify route existence without analytics assertions. | |
| You decide | Leave script assertions to implementation. | |

**User's choice:** Snippet on required routes (Recommended)

### Q3. How should manual GA real-time verification be recorded?

| Option | Description | Selected |
|--------|-------------|----------|
| Checklist with evidence (Recommended) | Record route-hit checklist plus timestamp/report evidence in phase notes. | ✓ |
| Ad-hoc check | Quick real-time check without recorded proof. | |
| Automated synthetic hits | Script traffic generation for evidence. | |
| You decide | Leave verification record format to implementation. | |

**User's choice:** Checklist with evidence (Recommended)

### Q4. When should standard-report verification be performed after deployment?

| Option | Description | Selected |
|--------|-------------|----------|
| Within 24h (Recommended) | Confirm standard page reports same day or next day after route visits. | ✓ |
| Realtime only | Skip standard-report confirmation. | |
| Weekly cadence | Delay confirmation to weekly review cycle. | |
| You decide | Leave timing to implementation. | |

**User's choice:** Within 24h (Recommended)
**Notes:** Area considered complete; user moved to wrap-up and requested context creation.

---

## the agent's Discretion

- No explicit "you decide" selections were made by the user.

## Deferred Ideas

- Outbound click analytics (ANLT-02) acknowledged as deferred and not pulled into Phase 3 scope.
