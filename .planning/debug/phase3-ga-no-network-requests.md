---
status: diagnosed
trigger: "Diagnose root cause for one Phase 3 UAT gap. Find why user did not observe expected GA network requests."
created: 2026-04-05T09:16:01Z
updated: 2026-04-05T09:17:04Z
---

## Current Focus
<!-- OVERWRITE on each update - reflects NOW -->

hypothesis: No code defect in GA bootstrap; the observed "localhost-only" network view is caused by runtime observation constraints (browser blocking/filtering) that Phase 3 checks do not guard against.
test: Validate that production build injects GA scripts, and confirm verifier only checks static markers (not emitted requests).
expecting: If both are true, gap is a validation/runtime-environment issue rather than missing instrumentation code.
next_action: return root-cause diagnosis and fix-direction for UAT gap closure

## Symptoms
<!-- Written during gathering, then IMMUTABLE -->

expected: With `PUBLIC_SITE_ENV=production` and measurement ID set, production page includes GA loader/config and should emit GA network traffic.
actual: User reports code looks fine but no requests appear in network beyond localhost.
errors: "The code looks fine, but I don't see any requests in the network beyond localhost."
reproduction: UAT Test 2 in Phase 03 analytics baseline.
started: discovered during UAT

## Eliminated
<!-- APPEND only - prevents re-investigating -->

## Evidence
<!-- APPEND only - facts discovered -->

- timestamp: 2026-04-05T09:16:52Z
  checked: site/src/layouts/BaseLayout.astro + built dist/index.html
  found: With `PUBLIC_SITE_ENV=production` and `PUBLIC_GA_MEASUREMENT_ID` set, built HTML includes `https://www.googletagmanager.com/gtag/js?id=...` and inline `gtag('config', ...)` with required privacy flags and `page_path: window.location.pathname`.
  implication: Instrumentation code path is present in production artifacts; this is not a missing-script defect.

- timestamp: 2026-04-05T09:16:31Z
  checked: site/scripts/verify-phase3.mjs and `npm --prefix site run verify:phase3`
  found: Verifier passed and only asserts static HTML markers (`googletagmanager`, `gtag('config')`, privacy flags, pathname marker), not real runtime request emission.
  implication: Automated checks can pass even when browser/network environment blocks third-party GA requests.

- timestamp: 2026-04-05T09:16:52Z
  checked: UAT symptom text + checklist/process guidance
  found: Reported symptom is specifically "no requests beyond localhost," which matches browser-side filter/blocker/privacy behavior; existing checklist lacks explicit steps to disable tracker blocking / clear Network filters when validating requests.
  implication: Most likely failure mode is observation environment, yielding a false-negative UAT result despite correct injected GA bootstrap.

## Resolution
<!-- OVERWRITE as understanding evolves -->

root_cause: "Phase 3 code correctly injects GA in production, but UAT relied on network observation in a browser context where third-party GA traffic was likely hidden/blocked (e.g., tracker blocking, strict privacy mode, or DevTools filtering to localhost). Because the Phase 3 verifier checks only static markers, this runtime observation constraint was not caught, producing a major perceived gap."
fix: "Strengthen manual verification protocol to require clean/incognito session with extensions disabled, Network filter cleared, and explicit checks for requests to googletagmanager.com and google-analytics.com; optionally add a scripted browser-network smoke test in CI/UAT to assert at least one external GA request when production env vars are set."
verification: "Diagnosis-only mode; no code changes applied."
files_changed: []
