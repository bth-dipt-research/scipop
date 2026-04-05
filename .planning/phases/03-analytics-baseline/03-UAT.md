---
status: diagnosed
phase: 03-analytics-baseline
source:
  - 03-analytics-baseline-01-SUMMARY.md
  - 03-analytics-baseline-02-SUMMARY.md
started: 2026-04-03T19:19:04Z
updated: 2026-04-05T09:17:40Z
---

## Current Test

[testing complete]

## Tests

### 1. Non-Production Telemetry Gate
expected: When `PUBLIC_SITE_ENV` is not set to production, public pages load without injecting any GA script or `gtag('config', ...)` bootstrap.
result: pass

### 2. Production GA Bootstrap and Privacy Markers
expected: With `PUBLIC_SITE_ENV=production` and a measurement ID set, public pages include GA loader/config with canonical `window.location.pathname` page path and privacy-safe markers (`anonymize_ip`, disabled google signals, disabled ad personalization).
result: issue
reported: "The code looks fine, but I don't see any requests in the network beyond localhost."
severity: major

### 3. Automated Phase 3 Verifier Command
expected: Running `npm --prefix site run verify:phase3` after a production build succeeds and confirms required routes plus GA markers are present.
result: pass

### 4. Manual GA Evidence Checklist Availability
expected: The checklist at `.planning/phases/03-analytics-baseline/03-GA-VERIFICATION-CHECKLIST.md` is present and includes route coverage plus realtime and 24-hour evidence capture fields.
result: pass

## Summary

total: 4
passed: 3
issues: 1
pending: 0
skipped: 0
blocked: 0

## Gaps

- truth: "With `PUBLIC_SITE_ENV=production` and a measurement ID set, public pages include GA loader/config with canonical `window.location.pathname` page path and privacy-safe markers (`anonymize_ip`, disabled google signals, disabled ad personalization)."
  status: failed
  reason: "User reported: The code looks fine, but I don't see any requests in the network beyond localhost."
  severity: major
  test: 2
  root_cause: "GA code is injected correctly in production builds, but runtime visibility of outbound GA calls is environment-dependent (browser tracker/privacy blocking or DevTools filtering), and current verifier only checks static HTML markers, not live request emission."
  artifacts:
    - path: ".planning/phases/03-analytics-baseline/03-UAT.md"
      issue: "Gap report confirms no visible non-localhost requests while automated artifact verifier still passed."
    - path: "site/src/layouts/BaseLayout.astro"
      issue: "Production gate and GA loader/config snippet are present with required privacy markers."
    - path: "site/src/lib/analytics.ts"
      issue: "Telemetry enablement depends solely on PUBLIC_SITE_ENV=production and measurement ID presence."
    - path: "site/scripts/verify-phase3.mjs"
      issue: "Verifier asserts static route artifact markers only and cannot validate runtime outbound requests."
  missing:
    - "Add explicit UAT observation protocol: disable blockers, clear DevTools filters, and verify requests to googletagmanager.com/google-analytics.com."
    - "Add optional runtime smoke check that validates at least one outbound GA request under production env settings."
  debug_session: ".planning/debug/phase3-ga-no-network-requests.md"
