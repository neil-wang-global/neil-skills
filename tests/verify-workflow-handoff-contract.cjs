const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const readSkill = (name) =>
  fs.readFileSync(path.join(root, 'skills', name, 'SKILL.md'), 'utf8');

const issueInit = readSkill('issue-init');
const issueExecuting = readSkill('issue-executing');
const prCreate = readSkill('pr-create');
const coordinator = readSkill('using-neil-workflows');
const prReview = readSkill('pr-review');
const prFix = readSkill('pr-fix');
const prMerge = readSkill('pr-merge');
const issueClose = readSkill('issue-close');

const requireText = (source, text, label) =>
  assert.ok(source.includes(text), `${label} must contain ${JSON.stringify(text)}`);

for (const [name, source, stage] of [
  ['issue-init', issueInit, 'issue-init'],
  ['issue-executing', issueExecuting, 'issue-executing'],
  ['pr-create', prCreate, 'pr-create'],
  ['pr-review', prReview, 'pr-review'],
  ['pr-fix', prFix, 'pr-fix'],
  ['pr-merge', prMerge, 'pr-merge'],
  ['issue-close', issueClose, 'issue-close'],
]) {
  requireText(source, `stage:\"${stage}\"`, name);
  requireText(source, 'status:\"completed\"', name);
  requireText(source, '`handoff`', name);
}

for (const [name, source] of [
  ['issue-executing', issueExecuting],
  ['pr-create', prCreate],
  ['pr-review', prReview],
  ['pr-fix', prFix],
  ['pr-merge', prMerge],
  ['issue-close', issueClose],
]) {
  requireText(source, 're-emits the full validated prior handoff unchanged', name);
}

for (const leaf of [
  '"repository": {',
  '"configIdentity": {',
  '"textLanguage":',
  '"issue": {',
  '"implementationBrief": {',
  '"branch":',
  '"worktree":',
  '"headRepository":',
]) {
  requireText(issueInit, leaf, 'issue-init handoff');
}

for (const leaf of [
  '"repository": {',
  '"configIdentity": {',
  '"textLanguage":',
  '"issue": {',
  '"implementationBrief": {',
  '"branch":',
  '"worktree":',
  '"headRepository":',
  '"git": {',
]) {
  requireText(issueExecuting, leaf, 'issue-executing handoff');
}

for (const leaf of [
  '"target": {',
  '"automation": {',
  '"provider":',
  '"host":',
  '"repository":',
  '"number":',
  '"url":',
  '"baseBranch":',
  '"headRepository":',
  '"headBranch":',
  '"headSha":',
  '"baseRef":',
  '"configBlobSha":',
]) {
  requireText(prCreate, leaf, 'pr-create handoff');
}

requireText(
  coordinator,
  'A completed stage result must contain only `version`, `stage`, `status`, and owned `handoff` at its top level.',
  'coordinator result contract',
);
requireText(
  coordinator,
  'Reject a result with required owned leaves outside `handoff`.',
  'coordinator result contract',
);

console.log('workflow handoff contract: PASS');
