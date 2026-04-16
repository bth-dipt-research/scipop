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

const missingRoutes = [];
const missingMarkers = [];
const forbiddenMarkers = [];

const requiredRoutes = ['/', '/overview', '/methodology', '/privacy'];
for (const slug of readApprovedSynthesisSlugs()) {
  requiredRoutes.push(`/syntheses/${slug}`);
}

for (const route of requiredRoutes) {
  const htmlPath = getExistingHtmlPath(route);
  if (!htmlPath) {
    missingRoutes.push(route);
  }
}

const featuredRouteExists = getExistingHtmlPath('/featured');
if (featuredRouteExists) {
  forbiddenMarkers.push('/featured route exists in built output');
}

const indexPath = getExistingHtmlPath('/');
if (indexPath) {
  const indexHtml = fs.readFileSync(indexPath, 'utf8');
  if (!indexHtml.includes('data-phase5-nav')) {
    missingMarkers.push('missing data-phase5-nav marker on /');
  }
  if (!indexHtml.includes('/overview')) {
    missingMarkers.push('missing /overview nav link on /');
  }
  if (indexHtml.includes('/featured')) {
    forbiddenMarkers.push('found /featured link on /');
  }
  if (!indexHtml.includes('data-phase5-map')) {
    missingMarkers.push('missing data-phase5-map marker on /');
  }
  if (!indexHtml.includes('data-phase5-mobile-fallback')) {
    missingMarkers.push('missing data-phase5-mobile-fallback marker on /');
  }
}

const longFormRoutes = ['/overview', '/methodology', '/privacy'];
for (const slug of readApprovedSynthesisSlugs()) {
  longFormRoutes.push(`/syntheses/${slug}`);
}

for (const route of longFormRoutes) {
  const htmlPath = getExistingHtmlPath(route);
  if (!htmlPath) {
    continue;
  }
  const html = fs.readFileSync(htmlPath, 'utf8');
  if (!html.includes('data-long-form="true"')) {
    missingMarkers.push(`${route} missing data-long-form marker`);
  }
}

for (const slug of readApprovedSynthesisSlugs()) {
  const route = `/syntheses/${slug}`;
  const htmlPath = getExistingHtmlPath(route);
  if (!htmlPath) {
    continue;
  }

  const html = fs.readFileSync(htmlPath, 'utf8');
  if (!html.includes('data-phase5-editor-profile')) {
    missingMarkers.push(`${route} missing data-phase5-editor-profile marker`);
  }
  if (!html.includes('data-phase5-editor-contact')) {
    missingMarkers.push(`${route} missing data-phase5-editor-contact marker`);
  }
  if (!html.includes('Questions regarding the research presented on this page? Please contact')) {
    missingMarkers.push(`${route} missing required contact sentence text`);
  }
}

if (missingRoutes.length > 0) {
  console.error('Missing required Phase 5 routes:');
  for (const route of missingRoutes) {
    console.error(`- ${route}`);
  }
}

if (missingMarkers.length > 0) {
  console.error('Missing required Phase 5 markers:');
  for (const marker of missingMarkers) {
    console.error(`- ${marker}`);
  }
}

if (forbiddenMarkers.length > 0) {
  console.error('Found forbidden Phase 5 regressions:');
  for (const marker of forbiddenMarkers) {
    console.error(`- ${marker}`);
  }
}

if (missingRoutes.length > 0 || missingMarkers.length > 0 || forbiddenMarkers.length > 0) {
  process.exit(1);
}

console.log('Verified Phase 5 UI polish route, IA, and editor-profile coverage.');
