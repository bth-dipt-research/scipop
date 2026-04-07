# Phase 3 GA Verification Checklist

Use this checklist after deployment to production to confirm ANLT-01 telemetry behavior.

## Preflight: avoid false negatives before route checks

Complete this once per verification session before visiting routes:

1. **Disable tracker/ad-blocking** extensions (or fully pause them for the session).
2. Relax strict browser privacy protections for this test session (private/incognito is still recommended for isolation).
3. Open DevTools Network and clear any active **Network filter** text (do not keep `localhost`-only filters).
4. Enable `Preserve log` in Network so requests remain visible during route navigation.
5. Confirm Network requests are visible for external domains before continuing.

## Realtime verification checklist

1. Open Google Analytics Realtime view for the production property.
2. In a private/incognito browser window, visit each required production route:
   - `/`
   - `/featured`
   - `/methodology`
   - At least one approved `/syntheses/{slug}` route
3. In DevTools Network, confirm outbound requests are visible for both `googletagmanager.com` and `google-analytics.com` during route visits.
4. Confirm each visited route path appears in GA Realtime.
5. Record evidence in the table below immediately after each route visit, including request-domain observations.

| route | visit_time_utc | request_domain | request_seen | ga_view | notes_if_missing | evidence_note |
| --- | --- | --- | --- |
| / |  | googletagmanager.com / google-analytics.com |  |  |  |  |
| /featured |  | googletagmanager.com / google-analytics.com |  |  |  |  |
| /methodology |  | googletagmanager.com / google-analytics.com |  |  |  |  |
| /syntheses/{slug} |  | googletagmanager.com / google-analytics.com |  |  |  |  |

## Optional runtime smoke check (production env)

Run this optional companion check when request visibility is uncertain or before manual UAT review:

```bash
PUBLIC_SITE_ENV=production PUBLIC_GA_MEASUREMENT_ID=G-TEST123 npm --prefix site run verify:phase3:runtime-smoke
```

Capture command output in evidence notes. This validates outbound request reachability to:
- `www.googletagmanager.com`
- `www.google-analytics.com`

| checked_time_utc | command | request_domain | request_seen | notes_if_missing | output_excerpt |
| --- | --- | --- | --- | --- | --- |
|  | verify:phase3:runtime-smoke | www.googletagmanager.com |  |  |  |
|  | verify:phase3:runtime-smoke | www.google-analytics.com |  |  |  |

## 24-hour standard report checklist

1. Within 24 hours of deployment, open GA standard reports for page/path performance.
2. Confirm the tested production routes are present in the report output.
3. Record report evidence in the table below.

| report_name | checked_time_utc | routes_confirmed | evidence_note |
| --- | --- | --- | --- |
|  |  |  |  |

Status: pending | passed | failed
