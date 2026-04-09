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

const CONSENT_MARKERS = [
  'data-consent-banner',
  'data-consent-accept',
  'data-consent-decline',
  'data-consent-manage',
  'scipop_analytics_consent',
];

const FORBIDDEN_STATIC_GA_LOADER_MARKER = '<script async src="https://www.googletagmanager.com/gtag/js?id=';

const readApprovedSynthesisSlugs = () => {
  const synthDir = path.join(siteDir, '..', 'content', 'syntheses');
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

const coreRoutes = ['/', '/featured', '/methodology', '/privacy'];
const requiredRoutes = [...coreRoutes];
for (const slug of readApprovedSynthesisSlugs()) {
  requiredRoutes.push(`/syntheses/${slug}`);
}

const missingRoutes = [];
const missingMarkersByRoute = [];
const routesWithStaticGaLoader = [];

for (const route of requiredRoutes) {
  const htmlPath = getExistingHtmlPath(route);
  if (!htmlPath) {
    missingRoutes.push(route);
    continue;
  }

  const html = fs.readFileSync(htmlPath, 'utf8');
  const missingMarkers = CONSENT_MARKERS.filter((marker) => !html.includes(marker));

  if (missingMarkers.length > 0) {
    missingMarkersByRoute.push({ route, missingMarkers });
  }

  if (html.includes(FORBIDDEN_STATIC_GA_LOADER_MARKER)) {
    routesWithStaticGaLoader.push(route);
  }
}

if (missingRoutes.length > 0) {
  console.error('Missing required Phase 4 routes:');
  for (const route of missingRoutes) {
    console.error(`- ${route}`);
  }
}

if (missingMarkersByRoute.length > 0) {
  console.error('Routes missing required consent/privacy markers:');
  for (const result of missingMarkersByRoute) {
    console.error(`- ${result.route}`);
    for (const marker of result.missingMarkers) {
      console.error(`  - ${marker}`);
    }
  }
}

if (routesWithStaticGaLoader.length > 0) {
  console.error('Routes still include forbidden static GA loader tags:');
  for (const route of routesWithStaticGaLoader) {
    console.error(`- ${route}`);
  }
}

if (missingRoutes.length > 0 || missingMarkersByRoute.length > 0 || routesWithStaticGaLoader.length > 0) {
  process.exit(1);
}

console.log(`Verified Phase 4 GDPR coverage for ${requiredRoutes.length} route(s).`);
