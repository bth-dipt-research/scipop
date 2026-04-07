/**
 * Optional runtime smoke companion to verify-phase3 static artifact checks.
 *
 * This script addresses UAT-diagnosed runtime visibility limitations by
 * validating outbound reachability to GA runtime request domains.
 */

import process from 'node:process';

const REQUIRED_ENV = 'production';
const REQUEST_TIMEOUT_MS = 10000;

const nowIso = () => new Date().toISOString();

const publicSiteEnv = String(process.env.PUBLIC_SITE_ENV ?? '').trim().toLowerCase();
const measurementId = String(process.env.PUBLIC_GA_MEASUREMENT_ID ?? '').trim();

if (publicSiteEnv !== REQUIRED_ENV) {
  console.error(
    `[runtime-smoke] PUBLIC_SITE_ENV must be "${REQUIRED_ENV}" (received: "${publicSiteEnv || '(empty)'}").`,
  );
  console.error('[runtime-smoke] Remediation: run with PUBLIC_SITE_ENV=production.');
  process.exit(1);
}

if (!measurementId) {
  console.error('[runtime-smoke] PUBLIC_GA_MEASUREMENT_ID is required and cannot be empty.');
  console.error('[runtime-smoke] Remediation: set PUBLIC_GA_MEASUREMENT_ID to your GA property ID.');
  process.exit(1);
}

const syntheticTs = Date.now();
const domainChecks = [
  {
    request_domain: 'www.googletagmanager.com',
    label: 'gtag-loader',
    url: `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`,
  },
  {
    request_domain: 'www.google-analytics.com',
    label: 'collect-endpoint',
    url: `https://www.google-analytics.com/g/collect?v=2&tid=${encodeURIComponent(measurementId)}&cid=555.1234567890&ul=en-us&sr=1440x900&dl=https%3A%2F%2Fexample.com%2Fscipop%2Fruntime-smoke&dt=phase3-runtime-smoke&en=page_view&_s=1&sid=${syntheticTs}&sct=1&seg=1`,
  },
];

async function checkDomain({ request_domain, label, url }) {
  const started_at = nowIso();

  try {
    const response = await fetch(url, {
      method: 'GET',
      signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
    });

    return {
      request_domain,
      label,
      url,
      started_at,
      finished_at: nowIso(),
      ok: response.ok,
      status_code: response.status,
      error: null,
    };
  } catch (error) {
    return {
      request_domain,
      label,
      url,
      started_at,
      finished_at: nowIso(),
      ok: false,
      status_code: null,
      error: error instanceof Error ? error.message : String(error),
    };
  }
}

const results = await Promise.all(domainChecks.map((check) => checkDomain(check)));
const failed = results.filter((result) => !result.ok);

console.log('[runtime-smoke] Phase 3 GA runtime smoke summary');
console.log(`[runtime-smoke] checked_at=${nowIso()}`);
console.log(`[runtime-smoke] measurement_id=${measurementId}`);
for (const result of results) {
  console.log(
    [
      `[runtime-smoke] request_domain=${result.request_domain}`,
      `label=${result.label}`,
      `ok=${result.ok}`,
      `status_code=${result.status_code ?? 'n/a'}`,
      `started_at=${result.started_at}`,
      `finished_at=${result.finished_at}`,
      `error=${result.error ?? 'none'}`,
    ].join(' | '),
  );
}

if (failed.length > 0) {
  console.error('[runtime-smoke] FAIL: one or more GA runtime domain checks failed.');
  console.error(
    '[runtime-smoke] Remediation: verify network connectivity and confirm tracker/privacy blockers are disabled for verification session.',
  );
  process.exit(1);
}

console.log('[runtime-smoke] PASS: outbound GA runtime domain checks succeeded.');
