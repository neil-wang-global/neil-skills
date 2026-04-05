---
name: init-commit-hooks
description: Use when user invokes /init-commit-hooks, or when needing to set up commitlint and lefthook for conventional commit enforcement in any project
---

# Init Commit Hooks

## Overview

Initialize commit hooks in **any project** (Node.js, Go, Python, Rust, etc.) using **lefthook** (git hooks manager) and **commitlint** (commit message linter). Enforces conventional commits with required scope and body.

## What Gets Created

| File | Purpose |
|------|---------|
| `commitlint.config.cjs` | Commitlint rules — conventional commits, required scope + body |
| `lefthook.yml` | commit-msg hook — runs commitlint + blocks co-author trailers |
| `package.json` | Adds devDependencies + `prepare` script (created automatically if missing) |

## Step-by-Step

### 1. Ensure `package.json` Exists

If the project does not have a `package.json`, create one first:

```bash
npm init -y
```

This is required because commitlint is distributed as an npm package. Non-Node projects will get a `package.json` + `node_modules` solely for commit hook tooling.

### 2. Install Dependencies

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional lefthook
```

### 3. Create `commitlint.config.cjs`

**MUST use `.cjs` extension** — ensures CommonJS `module.exports` works regardless of whether the project has `"type": "module"` in package.json. Do NOT use `.js` or ESM `export default`.

```js
// commitlint.config.cjs
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore', 'ci', 'perf', 'build'],
    ],
    'scope-case': [2, 'always', 'lower-case'],
    'subject-empty': [2, 'never'],
    'subject-case': [0],
    'scope-empty': [2, 'never'],
    'body-empty': [2, 'never'],
  },
};
```

**All rules are required. Do NOT omit any:**

| Rule | Setting | Why |
|------|---------|-----|
| `type-enum` | 10 allowed types | Restrict commit types |
| `scope-case` | `lower-case` | Consistent scope casing |
| `subject-empty` | `never` | Subject line is required |
| `subject-case` | `0` (off) | Allow any subject casing |
| `scope-empty` | `never` | Scope is required |
| `body-empty` | `never` | Body is required |

### 4. Create `lefthook.yml`

```yaml
# lefthook.yml
commit-msg:
  commands:
    commitlint:
      run: ./node_modules/.bin/commitlint --edit {1}
    no-coauthor:
      run: |
        if grep -iE "^(co-authored-by|made with|generated with|signed-off-by):" {1}; then
          echo "ERROR: Co-authorship information (Co-Authored-By, Made with, etc.) is not allowed in commit messages"
          exit 1
        fi
```

**Critical details:**
- Use `./node_modules/.bin/commitlint`, NOT `npx commitlint` (npx has startup overhead)
- Command name is `no-coauthor` (no extra hyphen)
- `{1}` without quotes — lefthook passes the commit message file path

### 5. Add `prepare` Script to `package.json`

Add to the `scripts` section:

```json
"prepare": "lefthook install --force"
```

**Use `--force`** to ensure hooks are always reinstalled, even if they already exist.

### 6. Activate Hooks

```bash
npx lefthook install --force
```

### 7. Verify

Make a test commit to confirm hooks work:

```bash
git add .
git commit -m "bad message"
# Should FAIL — missing type, scope, body

git commit -m "feat(init): initialize commit hooks

Add commitlint and lefthook for conventional commit enforcement."
# Should PASS
```

## Common Mistakes

| Mistake | Correct |
|---------|---------|
| Use `.js` with ESM `export default` | Use `.cjs` with `module.exports` |
| Use `npx commitlint` in lefthook | Use `./node_modules/.bin/commitlint` |
| Omit `--force` from prepare script | Always use `lefthook install --force` |
| Forget `scope-case` or `subject-case` rules | Include ALL 6 rules from the table above |
| Quote `{1}` in grep command | Leave `{1}` unquoted |
| Name command `no-co-author` | Name is `no-coauthor` (no extra hyphen) |
| Skip `npm init` for non-Node projects | Always ensure `package.json` exists first |
