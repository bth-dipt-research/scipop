import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const consentPath = path.join(process.cwd(), 'src', 'lib', 'consent.ts');
const baseLayoutPath = path.join(process.cwd(), 'src', 'layouts', 'BaseLayout.astro');
const privacyPagePath = path.join(process.cwd(), 'src', 'pages', 'privacy.astro');
const phase4VerifierPath = path.join(process.cwd(), 'scripts', 'verify-phase4.mjs');
const packageJsonPath = path.join(process.cwd(), 'package.json');

test('readConsentState defaults to unset when no storage values exist', () => {
  assert.equal(fs.existsSync(consentPath), true, 'consent.ts should exist');
  const content = fs.readFileSync(consentPath, 'utf8');

  assert.match(content, /export\s+type\s+ConsentState\s*=\s*'accepted'\s*\|\s*'rejected'\s*\|\s*'unset'/);
  assert.match(content, /export\s+function\s+readConsentState\s*\(\)\s*:\s*ConsentState/);
  assert.match(content, /return\s+'unset'/);
});

test('writeConsentState persists accepted state to localStorage and cookie', () => {
  assert.equal(fs.existsSync(consentPath), true, 'consent.ts should exist');
  const content = fs.readFileSync(consentPath, 'utf8');

  assert.match(content, /localStorage\.setItem\(CONSENT_STORAGE_KEY,\s*next\)/);
  assert.match(content, /document\.cookie\s*=\s*`\$\{CONSENT_STORAGE_KEY\}=\$\{next\};\s*Path=\/;\s*Max-Age=31536000;\s*SameSite=Lax`/);
});

test('writeConsentState persists rejected state for subsequent reads', () => {
  assert.equal(fs.existsSync(consentPath), true, 'consent.ts should exist');
  const content = fs.readFileSync(consentPath, 'utf8');

  assert.match(content, /next\s*===\s*'accepted'\s*\|\|\s*next\s*===\s*'rejected'/);
  assert.match(content, /if\s*\(stored\s*===\s*'accepted'\s*\|\|\s*stored\s*===\s*'rejected'\)/);
});

test('ga snippet is gated by production and accepted consent state', () => {
  assert.equal(fs.existsSync(baseLayoutPath), true, 'BaseLayout.astro should exist');
  const content = fs.readFileSync(baseLayoutPath, 'utf8');

  assert.match(content, /isProductionTelemetryEnabled\(\)\s*&&\s*consentState\s*===\s*'accepted'/);
});

test('banner exposes only accept and reject controls', () => {
  assert.equal(fs.existsSync(baseLayoutPath), true, 'BaseLayout.astro should exist');
  const content = fs.readFileSync(baseLayoutPath, 'utf8');

  assert.match(content, /Accept all/);
  assert.match(content, /Reject all/);
  assert.doesNotMatch(content, /Customize/);
});

test('footer privacy settings re-open flow includes inline confirmation text', () => {
  assert.equal(fs.existsSync(baseLayoutPath), true, 'BaseLayout.astro should exist');
  const content = fs.readFileSync(baseLayoutPath, 'utf8');

  assert.match(content, /Privacy settings/);
  assert.match(content, /Privacy settings updated\./);
  assert.match(content, /Current status: accepted\./);
  assert.match(content, /Current status: rejected\./);
  assert.match(content, /Current status: unset\./);
  assert.match(content, /openPrivacyButton\.addEventListener\('click',\s*\(\)\s*=>\s*{\s*renderCurrentConsentStatus\(\);\s*openConsentBanner\(\);/s);
});

test('dismiss action closes banner without persisting or applying rejected consent', () => {
  assert.equal(fs.existsSync(baseLayoutPath), true, 'BaseLayout.astro should exist');
  const content = fs.readFileSync(baseLayoutPath, 'utf8');

  assert.match(content, /dismissButton\.addEventListener\('click',\s*\(\)\s*=>\s*{\s*closeConsentBanner\(\);\s*setConsentStatus\(''\);/s);
  assert.doesNotMatch(content, /dismissButton\.addEventListener\('click',\s*\(\)\s*=>\s*{[\s\S]*applyConsent\('rejected'\);/);
  assert.doesNotMatch(content, /dismissButton\.addEventListener\('click',\s*\(\)\s*=>\s*{[\s\S]*writeConsentState\('rejected'\);/);
});

test('privacy disclosure page includes required sections', () => {
  assert.equal(fs.existsSync(privacyPagePath), true, 'privacy.astro should exist');
  const content = fs.readFileSync(privacyPagePath, 'utf8');

  assert.match(content, /Google Analytics/);
  assert.match(content, /What we track/);
  assert.match(content, /How to change consent/);
  assert.match(content, /Contact/);
});

test('phase 4 verifier script exists and checks disclosure markers', () => {
  assert.equal(fs.existsSync(phase4VerifierPath), true, 'verify-phase4.mjs should exist');
  const content = fs.readFileSync(phase4VerifierPath, 'utf8');

  assert.match(content, /privacy/);
  assert.match(content, /Accept all/);
  assert.match(content, /Reject all/);
  assert.match(content, /Privacy settings/);
  assert.match(content, /process\.exit\(1\)/);
});

test('package scripts include verify:phase4 command', () => {
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
  assert.equal(typeof packageJson.scripts?.['verify:phase4'], 'string');
  assert.match(packageJson.scripts['verify:phase4'], /node\s+\.\/scripts\/verify-phase4\.mjs/);
});
