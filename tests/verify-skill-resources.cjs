#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

const repositoryRoot = path.resolve(__dirname, '..');
const skillRoot = process.env.SKILL_ROOT || path.join(repositoryRoot, 'skills');
const prSkills = ['pr-create', 'pr-review', 'pr-fix', 'pr-merge'];
const referenceFiles = [
  'pr-workflow-contract.md',
  'github-pr-api.md',
  'gitlab-mr-api.md',
];

const missing = [];
const mismatched = [];
const invalidInstructions = [];
for (const skill of prSkills) {
  const skillPath = path.join(skillRoot, skill, 'SKILL.md');
  const skillSource = fs.readFileSync(skillPath, 'utf8');
  if (skillSource.includes('../../references/')) invalidInstructions.push(skillPath);

  for (const reference of referenceFiles) {
    const sourcePath = path.join(repositoryRoot, 'references', reference);
    const resourcePath = path.join(
      skillRoot,
      skill,
      'references',
      reference,
    );
    if (!fs.existsSync(resourcePath)) {
      missing.push(resourcePath);
    } else if (fs.readFileSync(resourcePath, 'utf8') !== fs.readFileSync(sourcePath, 'utf8')) {
      mismatched.push(resourcePath);
    }
  }
}

if (missing.length > 0 || mismatched.length > 0 || invalidInstructions.length > 0) {
  if (missing.length > 0) {
    console.error('Missing bundled PR-skill resources:');
    for (const resourcePath of missing) console.error(`- ${resourcePath}`);
  }
  if (mismatched.length > 0) {
    console.error('Bundled PR-skill resources differ from the shared source:');
    for (const resourcePath of mismatched) console.error(`- ${resourcePath}`);
  }
  if (invalidInstructions.length > 0) {
    console.error('PR skills still reference resources outside their bundle:');
    for (const skillPath of invalidInstructions) console.error(`- ${skillPath}`);
  }
  process.exitCode = 1;
}
