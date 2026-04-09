# Phase 4 GDPR Verification Checklist

Use this checklist to validate consent-gated analytics and privacy controls before release.

## Automated preflight

Run both commands from repository root:

```bash
npm --prefix site run build
npm --prefix site run verify:phase4
```

If `verify:phase4` fails, resolve missing route/marker issues before manual checks.

## First-visit consent behavior

1. Open the site in a private/incognito window with empty storage.
2. Visit `/` and confirm the consent banner is visible.
3. In browser storage, confirm `scipop_analytics_consent` is not set before choosing.
4. Open DevTools Network and confirm no GA requests are sent before an explicit consent action.

## Grant consent behavior

1. Click **Accept analytics** in the consent banner.
2. Confirm `scipop_analytics_consent` is set to `granted` in localStorage.
3. Reload and navigate `/`, `/featured`, `/methodology`, `/privacy`, and one `/syntheses/{slug}` route.
4. Confirm GA requests are visible in Network after grant (for example requests to `googletagmanager.com` / `google-analytics.com`).

## Deny/withdraw consent behavior

1. Open **Privacy settings** from site navigation.
2. Click **Decline analytics**.
3. Confirm `scipop_analytics_consent` becomes `denied` in localStorage.
4. Confirm `_ga`, `_gid`, and `_ga_*` cookies are absent after decline.
5. Reload pages and confirm no new GA requests are emitted while consent remains denied.
6. Reopen **Privacy settings** and verify the consent controls are shown again.

## Evidence log

| scenario | route | observed_result | timestamp_utc | notes |
| --- | --- | --- | --- | --- |
| first-visit (unset) | / |  |  |  |
| grant accepted | /featured |  |  |  |
| grant accepted | /privacy |  |  |  |
| denied/withdrawn | /methodology |  |  |  |
| denied/withdrawn | /syntheses/{slug} |  |  |  |

Status: pending | passed | failed
