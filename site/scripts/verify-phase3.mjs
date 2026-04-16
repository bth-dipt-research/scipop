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
const isProductionMode = String(process.env.PUBLIC_SITE_ENV ?? '').trim().toLowerCase() === 'production';

const TELEMETRY_MARKERS = [
  'googletagmanager.com/gtag/js?id=',
  "gtag('config'",
  'anonymize_ip: true',
  'allow_google_signals: false',
  'allow_ad_personalization_signals: false',
  'window.location.pathname',
];

const readApprovedSynthesisSlugs = () => {
  const synthDir = path.join(siteDir, 'src', 'content', 'syntheses');
  if (!fs.existsSync(synthDir)) {
    return [];
  }

  const files = fs.readdirSync(synthDir).filter((file) => file.endsWith('.md'));
  const slugs = [];

  for (const file of files) {
    const body = fs.readFileSync(path.join(synthDir, file), 'utf8');
    const statusMatch = body.match(/^status:\s*(.+)$/m);
    const slugMatch = body.match(/^slug:\s*(.+)$/m);
    if (statusMatch && slugMatch && statusMatch[1].trim() === 'approved') {
      slugs.push(slugMatch[1].trim());
    }
  }

  return slugs;
};

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

const coreRoutes = ['/', '/overview', '/methodology'];
const requiredRoutes = [...coreRoutes];
for (const slug of readApprovedSynthesisSlugs()) {
  requiredRoutes.push(`/syntheses/${slug}`);
}

const missingRoutes = [];
const missingMarkersByRoute = [];

for (const route of requiredRoutes) {
  const htmlPath = getExistingHtmlPath(route);
  if (!htmlPath) {
    missingRoutes.push(route);
    continue;
  }

  if (isProductionMode) {
    const html = fs.readFileSync(htmlPath, 'utf8');
    const missingMarkers = TELEMETRY_MARKERS.filter((marker) => !html.includes(marker));

    if (missingMarkers.length > 0) {
      missingMarkersByRoute.push({ route, missingMarkers });
    }
  }
}

if (missingRoutes.length > 0) {
  console.error('Missing required Phase 3 routes:');
  for (const route of missingRoutes) {
    console.error(`- ${route}`);
  }
}

if (isProductionMode && missingMarkersByRoute.length > 0) {
  console.error('Routes missing required GA telemetry markers:');
  for (const result of missingMarkersByRoute) {
    console.error(`- ${result.route}`);
    for (const marker of result.missingMarkers) {
      console.error(`  - ${marker}`);
    }
  }
}

if (missingRoutes.length > 0 || (isProductionMode && missingMarkersByRoute.length > 0)) {
  process.exit(1);
}

if (!isProductionMode) {
  console.log(
    `Verified Phase 3 route coverage for ${requiredRoutes.length} route(s); telemetry markers are checked only when PUBLIC_SITE_ENV=production.`,
  );
} else {
  console.log(`Verified Phase 3 analytics coverage for ${requiredRoutes.length} route(s).`);
}
