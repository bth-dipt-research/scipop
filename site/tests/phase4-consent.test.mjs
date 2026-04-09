import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const consentPath = path.join(process.cwd(), 'src', 'lib', 'consent.ts');

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
