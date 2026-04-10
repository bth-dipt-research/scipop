import fs from 'node:fs';
import path from 'node:path';

const siteDir = process.cwd();
const distDir = path.join(siteDir, 'dist');
const basePrefix = 'scipop';
const REQUIRED_HEADING = 'Important context';

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

const requiredRoutes = ['/overview'];
for (const slug of readApprovedSynthesisSlugs()) {
  requiredRoutes.push(`/syntheses/${slug}`);
}

const missingRoutes = [];
const missingHeading = [];

for (const route of requiredRoutes) {
  const htmlPath = getExistingHtmlPath(route);
  if (!htmlPath) {
    missingRoutes.push(route);
    continue;
  }

  const html = fs.readFileSync(htmlPath, 'utf8');
  if (!html.includes(REQUIRED_HEADING)) {
    missingHeading.push(route);
  }
}

if (missingRoutes.length > 0) {
  console.error('Missing required Phase 2 routes:');
  for (const route of missingRoutes) {
    console.error(`- ${route}`);
  }
}

if (missingHeading.length > 0) {
  console.error(`Routes missing required disclaimer heading "${REQUIRED_HEADING}":`);
  for (const route of missingHeading) {
    console.error(`- ${route}`);
  }
}

if (missingRoutes.length > 0 || missingHeading.length > 0) {
  process.exit(1);
}

console.log(`Verified Phase 2 disclaimer coverage for ${requiredRoutes.length} route(s).`);
