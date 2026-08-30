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
const missingInstructions = [];
const externalInstructions = [];
const requiredInstructionPaths = referenceFiles.map((reference) =>
  `references/${reference}`,
);
const invalidAttestationReferences = [];
const attestationConstruction = [
  "attestation_body=$(printf '%s\\n%s' 'neil-self-reviewed/v1' \"$payload\")",
  '-f "body=$attestation_body"',
];
for (const reference of ['github-pr-api.md', 'gitlab-mr-api.md']) {
  const sourcePath = path.join(repositoryRoot, 'references', reference);
  const source = fs.readFileSync(sourcePath, 'utf8');
  if (!attestationConstruction.every((fragment) => source.includes(fragment))) {
    invalidAttestationReferences.push(sourcePath);
  }
}
for (const skill of prSkills) {
  const skillPath = path.join(skillRoot, skill, 'SKILL.md');
  const skillSource = fs.readFileSync(skillPath, 'utf8');
  for (const instructionPath of requiredInstructionPaths) {
    if (!skillSource.includes(instructionPath)) {
      missingInstructions.push(`${skillPath}: ${instructionPath}`);
    }
  }
  if (/(?:\.\.\/)+references\/|https?:\/\/[^\s`)]*references\//.test(skillSource)) {
    externalInstructions.push(skillPath);
  }

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

if (
  missing.length > 0 ||
  mismatched.length > 0 ||
  missingInstructions.length > 0 ||
  externalInstructions.length > 0 ||
  invalidAttestationReferences.length > 0
) {
  if (missing.length > 0) {
    console.error('Missing bundled PR-skill resources:');
    for (const resourcePath of missing) console.error(`- ${resourcePath}`);
  }
  if (mismatched.length > 0) {
    console.error('Bundled PR-skill resources differ from the shared source:');
    for (const resourcePath of mismatched) console.error(`- ${resourcePath}`);
  }
  if (invalidAttestationReferences.length > 0) {
    console.error('Attestation references must construct a real two-line body:');
    for (const sourcePath of invalidAttestationReferences) console.error(`- ${sourcePath}`);
  }
  if (missingInstructions.length > 0) {
    console.error('PR skills must name every bundled local resource:');
    for (const instructionPath of missingInstructions) console.error(`- ${instructionPath}`);
  }
  if (externalInstructions.length > 0) {
    console.error('PR skills must not instruct reading external resources:');
    for (const skillPath of externalInstructions) console.error(`- ${skillPath}`);
  }
  process.exitCode = 1;
}
