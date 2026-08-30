#!/usr/bin/env node

const fs = require('node:fs');
const path = require('node:path');

const repositoryRoot = path.resolve(__dirname, '..');
const read = (relativePath) => fs.readFileSync(path.join(repositoryRoot, relativePath), 'utf8');
const failures = [];

const expectations = [
  [
    'skills/issue-init/SKILL.md',
    '"pr-auto-delete-branch": true',
    'issue-init default enables post-merge branch deletion',
  ],
  [
    'references/pr-workflow-contract.md',
    '| `pr-auto-delete-branch` | `true` |',
    'shared contract defines the default',
  ],
  [
    'skills/pr-merge/SKILL.md',
    'branch-cleanup failure',
    'pr-merge owns the cleanup lifecycle',
  ],
  [
    'references/pr-workflow-contract.md',
    'Never delete a local branch, worktree, base branch, or a branch before actual merged state.',
    'cleanup waits for confirmed merge completion',
  ],
  [
    'references/github-pr-api.md',
    'git/refs/heads/<head-branch>',
    'GitHub reference deletes the verified head branch explicitly',
  ],
  [
    'references/gitlab-mr-api.md',
    'repository/branches/<encoded-head-branch>',
    'GitLab reference deletes the verified source branch explicitly',
  ],
];

for (const [relativePath, fragment, label] of expectations) {
  if (!read(relativePath).includes(fragment)) {
    failures.push(`${label}: ${relativePath}`);
  }
}

const referenceFiles = [
  'pr-workflow-contract.md',
  'github-pr-api.md',
  'gitlab-mr-api.md',
];
const prSkills = ['pr-create', 'pr-review', 'pr-fix', 'pr-merge'];
for (const skill of prSkills) {
  for (const reference of referenceFiles) {
    const source = read(`references/${reference}`);
    const bundled = read(`skills/${skill}/references/${reference}`);
    if (bundled !== source) {
      failures.push(`bundled reference is stale: skills/${skill}/references/${reference}`);
    }
  }
}

if (failures.length > 0) {
  console.error('PR auto-delete branch contract is incomplete:');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exitCode = 1;
}
