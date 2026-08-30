const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const readJson = (relativePath) =>
  JSON.parse(fs.readFileSync(path.join(root, relativePath), 'utf8'));

const packageJson = readJson('package.json');
const packageLock = readJson('package-lock.json');
const plugin = readJson('.claude-plugin/plugin.json');
const marketplace = readJson('.claude-plugin/marketplace.json');
const versions = [
  packageJson.version,
  packageLock.version,
  packageLock.packages[''].version,
  plugin.version,
  marketplace.plugins[0].version,
];

assert.ok(versions.every((version) => version === packageJson.version),
  `root and plugin versions must match: ${versions.join(', ')}`);
assert.equal(packageJson.version, '1.0.5', 'release version must be 1.0.5');

console.log(`version alignment: ${packageJson.version}`);
