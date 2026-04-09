import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const cwdSiteCandidate = path.join(process.cwd(), 'site');
const siteDir = fs.existsSync(path.join(process.cwd(), 'package.json'))
  ? process.cwd()
  : fs.existsSync(path.join(cwdSiteCandidate, 'package.json'))
    ? cwdSiteCandidate
    : path.resolve(scriptDir, '..');
const distDir = path.join(siteDir, 'dist');
const basePrefix = 'scipop';

const routeToCandidates = (route) => {
  const normalized = route === '/' ? '' : route.replace(/^\//, '').replace(/\/$/, '');
  const segments = normalized ? normalized.split('/') : [];

  return [
    path.join(distDir, ...segments, 'index.html'),
    path.join(distDir, basePrefix, ...segments, 'index.html'),
  ];
};

const getExistingHtmlPath = (route) => {
  const candidates = routeToCandidates(route);
  return candidates.find((candidate) => fs.existsSync(candidate));
};

const PRIVACY_MARKERS = [
  'Google Analytics',
  'What we track',
  'How to change consent',
  'Contact',
  'privacy@scipop.org',
];

const CONSENT_MARKERS = [
  'Accept all',
  'Reject all',
  'Privacy settings',
  'Privacy settings updated.',
];

const BASE_LAYOUT_GATE_MARKERS = ["isProductionTelemetryEnabled() && consentState === 'accepted'"];

const missingRoutes = [];
const missingPrivacyMarkers = [];
const missingConsentMarkers = [];
const missingGateMarkers = [];

const privacyHtmlPath = getExistingHtmlPath('/privacy');
if (!privacyHtmlPath) {
  missingRoutes.push('/privacy');
} else {
  const privacyHtml = fs.readFileSync(privacyHtmlPath, 'utf8');
  const missing = PRIVACY_MARKERS.filter((marker) => !privacyHtml.includes(marker));
  if (missing.length > 0) {
    missingPrivacyMarkers.push(...missing);
  }
}

const indexHtmlPath = getExistingHtmlPath('/');
if (!indexHtmlPath) {
  missingRoutes.push('/');
} else {
  const indexHtml = fs.readFileSync(indexHtmlPath, 'utf8');
  const missing = CONSENT_MARKERS.filter((marker) => !indexHtml.includes(marker));
  if (missing.length > 0) {
    missingConsentMarkers.push(...missing);
  }
}

const baseLayoutSourcePath = path.join(siteDir, 'src', 'layouts', 'BaseLayout.astro');
if (!fs.existsSync(baseLayoutSourcePath)) {
  missingGateMarkers.push('BaseLayout.astro missing');
} else {
  const source = fs.readFileSync(baseLayoutSourcePath, 'utf8');
  const missing = BASE_LAYOUT_GATE_MARKERS.filter((marker) => !source.includes(marker));
  if (missing.length > 0) {
    missingGateMarkers.push(...missing);
  }
}

if (missingRoutes.length > 0) {
  console.error('Missing required Phase 4 routes:');
  for (const route of missingRoutes) {
    console.error(`- ${route}`);
  }
}

if (missingPrivacyMarkers.length > 0) {
  console.error('Missing required privacy disclosure markers on /privacy:');
  for (const marker of missingPrivacyMarkers) {
    console.error(`- ${marker}`);
  }
}

if (missingConsentMarkers.length > 0) {
  console.error('Missing required consent UI/gate markers on / route artifact:');
  for (const marker of missingConsentMarkers) {
    console.error(`- ${marker}`);
  }
}

if (missingGateMarkers.length > 0) {
  console.error('Missing required consent gate source markers in BaseLayout.astro:');
  for (const marker of missingGateMarkers) {
    console.error(`- ${marker}`);
  }
}

if (
  missingRoutes.length > 0 ||
  missingPrivacyMarkers.length > 0 ||
  missingConsentMarkers.length > 0 ||
  missingGateMarkers.length > 0
) {
  process.exit(1);
}

console.log('Verified Phase 4 consent and privacy disclosure coverage.');
