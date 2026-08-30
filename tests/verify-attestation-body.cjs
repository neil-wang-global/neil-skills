#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

const repositoryRoot = path.resolve(__dirname, '..');
const prSkills = ['pr-create', 'pr-review', 'pr-fix', 'pr-merge'];
const references = ['github-pr-api.md', 'gitlab-mr-api.md'];
const requiredFragments = [
  "attestation_body=$(printf '%s\\n%s' 'neil-self-reviewed/v1' \"$payload\")",
  '-f "body=$attestation_body"',
];
const invalid = [];

for (const reference of references) {
  const sourcePath = path.join(repositoryRoot, 'references', reference);
  const source = fs.readFileSync(sourcePath, 'utf8');
  if (!requiredFragments.every((fragment) => source.includes(fragment))) {
    invalid.push(sourcePath);
  }

  for (const skill of prSkills) {
    const bundledPath = path.join(repositoryRoot, 'skills', skill, 'references', reference);
    const bundled = fs.readFileSync(bundledPath, 'utf8');
    if (bundled !== source) invalid.push(bundledPath);
  }
}

if (invalid.length > 0) {
  console.error('Attestation references must create a real two-line body:');
  for (const filePath of invalid) console.error(`- ${filePath}`);
  process.exitCode = 1;
}
