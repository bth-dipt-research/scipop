import fs from 'node:fs';
import path from 'node:path';

const siteDir = process.cwd();
const distDir = path.join(siteDir, 'dist');
const basePrefix = 'scipop';

const args = process.argv.slice(2);
const routeFilters = [];
const routePrefixes = [];

for (let i = 0; i < args.length; i += 1) {
  if (args[i].startsWith('--route=')) {
    routeFilters.push(args[i].slice('--route='.length));
  } else if (args[i].startsWith('--route-prefix=')) {
    routePrefixes.push(args[i].slice('--route-prefix='.length));
  } else if (args[i] === '--route' && args[i + 1]) {
    routeFilters.push(args[i + 1]);
    i += 1;
  } else if (args[i] === '--route-prefix' && args[i + 1]) {
    routePrefixes.push(args[i + 1]);
    i += 1;
  }
}

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

const existsRoute = (route) => routeToCandidates(route).some((candidate) => fs.existsSync(candidate));

const coreRoutes = ['/', '/featured', '/methodology'];
const requiredRoutes = [...coreRoutes];
for (const slug of readApprovedSynthesisSlugs()) {
  requiredRoutes.push(`/syntheses/${slug}`);
}

let finalRoutes = requiredRoutes;

if (routeFilters.length > 0) {
  finalRoutes = finalRoutes.filter((route) => routeFilters.includes(route));
}

if (routePrefixes.length > 0) {
  finalRoutes = finalRoutes.filter((route) => routePrefixes.some((prefix) => route.startsWith(prefix)));
}

if (finalRoutes.length === 0) {
  console.error('No routes selected for verification.');
  process.exit(1);
}

const missing = finalRoutes.filter((route) => !existsRoute(route));

if (missing.length > 0) {
  console.error('Missing required routes:');
  for (const route of missing) {
    console.error(`- ${route}`);
  }
  process.exit(1);
}

console.log(`Verified ${finalRoutes.length} route(s).`);
