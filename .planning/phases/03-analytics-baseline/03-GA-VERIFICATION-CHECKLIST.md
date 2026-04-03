# Phase 3 GA Verification Checklist

Use this checklist after deployment to production to confirm ANLT-01 telemetry behavior.

## Realtime verification checklist

1. Open Google Analytics Realtime view for the production property.
2. In a private/incognito browser window, visit each required production route:
   - `/`
   - `/featured`
   - `/methodology`
   - At least one approved `/syntheses/{slug}` route
3. Confirm each visited route path appears in GA Realtime.
4. Record evidence in the table below immediately after each route visit.

| route | visit_time_utc | ga_view | evidence_note |
| --- | --- | --- | --- |
| / |  |  |  |
| /featured |  |  |  |
| /methodology |  |  |  |
| /syntheses/{slug} |  |  |  |

## 24-hour standard report checklist

1. Within 24 hours of deployment, open GA standard reports for page/path performance.
2. Confirm the tested production routes are present in the report output.
3. Record report evidence in the table below.

| report_name | checked_time_utc | routes_confirmed | evidence_note |
| --- | --- | --- | --- |
|  |  |  |  |

Status: pending | passed | failed
