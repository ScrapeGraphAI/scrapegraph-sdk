# SOP: Releasing a New Version

**Last Updated:** January 2025

This document describes the automated and manual release process for both Python and JavaScript SDKs using semantic-release.

## Overview

Both SDKs use **semantic-release** for automated versioning and publishing:
- Analyzes commit messages to determine version bump
- Updates version numbers
- Generates changelog
- Creates GitHub releases
- Publishes to PyPI (Python) / npm (JavaScript)

## Semantic Versioning

Version format: `MAJOR.MINOR.PATCH` (e.g., `1.12.2`)

### Version Bump Rules

Based on commit message prefixes:

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat:` | Minor (0.x.0) | `feat: add pagination support` |
| `fix:` | Patch (0.0.x) | `fix: handle timeout errors` |
| `feat!:` or `BREAKING CHANGE:` | Major (x.0.0) | `feat!: change API interface` |
| `docs:`, `chore:`, `style:`, `refactor:`, `test:` | None | No release triggered |

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Examples:**

```
feat: add scheduled jobs support

Implement full CRUD operations for scheduled jobs including:
- Create job with cron expression
- List all jobs
- Update existing jobs
- Delete jobs
- Get job execution history
```

```
fix: handle network timeout gracefully

Add retry logic with exponential backoff for network failures.
Improves reliability when API is temporarily unavailable.
```

```
feat!: change client initialization API

BREAKING CHANGE: Client() now requires api_key parameter explicitly.
The from_env() class method should be used for environment-based initialization.

Migration:
- Before: client = Client()
- After: client = Client.from_env()
```

---

## Automated Release Process

### Prerequisites

1. All changes committed to feature branch
2. Pull request created and approved
3. All CI checks passing (tests, linting)
4. Semantic commit messages used

### Step-by-Step: Automated Release

**1. Prepare Your Changes**

Ensure commits use semantic format:
```bash
git commit -m "feat: add new endpoint"
git commit -m "fix: resolve timeout issue"
```

**2. Create Pull Request**

```bash
git push origin feature/your-feature
# Create PR on GitHub
```

**3. Code Review**

- Reviewers approve changes
- All GitHub Actions checks pass
- No merge conflicts

**4. Merge to Main**

```bash
# Merge via GitHub UI (Squash & Merge recommended)
# Or via command line:
git checkout main
git merge --squash feature/your-feature
git commit -m "feat: your feature description"
git push origin main
```

**5. Automated Release Triggers**

Once merged to `main`:

**Python SDK** (`.github/workflows/python-sdk-release.yml`):
1. semantic-release analyzes commits since last release
2. Determines version bump (major/minor/patch)
3. Updates `pyproject.toml` version
4. Generates `CHANGELOG.md` entry
5. Creates Git tag (e.g., `v1.13.0`)
6. Builds Python package (`uv build`)
7. Publishes to PyPI via `twine`
8. Creates GitHub release with notes

**JavaScript SDK** (`.github/workflows/js-sdk-release.yml`):
1. semantic-release analyzes commits
2. Updates `package.json` version
3. Generates `CHANGELOG.md` entry
4. Creates Git tag
5. Publishes to npm
6. Creates GitHub release

**6. Verify Release**

Check:
- GitHub Releases page: https://github.com/ScrapeGraphAI/scrapegraph-sdk/releases
- PyPI page: https://pypi.org/project/scrapegraph-py/
- npm page: https://www.npmjs.com/package/scrapegraph-js

---

## Manual Release Process

Use only for emergency releases or when automation fails.

### Python SDK Manual Release

**1. Update Version**

**File**: `scrapegraph-py/pyproject.toml`

```toml
[project]
name = "scrapegraph_py"
version = "1.13.0"  # Increment version
```

**2. Update Changelog**

**File**: `scrapegraph-py/CHANGELOG.md`

```markdown
## [1.13.0] - 2025-01-XX

### Added
- New feature description

### Fixed
- Bug fix description
```

**3. Commit Changes**

```bash
cd scrapegraph-py
git add pyproject.toml CHANGELOG.md
git commit -m "chore(release): 1.13.0"
git tag v1.13.0
git push origin main --tags
```

**4. Build Package**

```bash
cd scrapegraph-py

# Build with uv
uv build

# Or build with python
python -m build
```

This creates files in `dist/`:
- `scrapegraph_py-1.13.0-py3-none-any.whl`
- `scrapegraph_py-1.13.0.tar.gz`

**5. Test Package Locally**

```bash
# Install in test environment
python -m venv test-env
source test-env/bin/activate
pip install dist/scrapegraph_py-1.13.0-py3-none-any.whl

# Test import
python -c "from scrapegraph_py import Client; print('Success!')"
```

**6. Publish to PyPI**

```bash
# Install twine
pip install twine

# Check package
twine check dist/*

# Upload to PyPI
twine upload dist/*

# Enter PyPI credentials when prompted
```

**7. Create GitHub Release**

1. Go to https://github.com/ScrapeGraphAI/scrapegraph-sdk/releases/new
2. Tag: `v1.13.0`
3. Title: `Python SDK v1.13.0`
4. Description: Copy from CHANGELOG.md
5. Attach: `dist/scrapegraph_py-1.13.0.tar.gz`
6. Publish release

### JavaScript SDK Manual Release

**1. Update Version**

**File**: `scrapegraph-js/package.json`

```json
{
  "name": "scrapegraph-js",
  "version": "1.5.0",
  ...
}
```

**2. Update Changelog**

**File**: `scrapegraph-js/CHANGELOG.md`

```markdown
## [1.5.0] - 2025-01-XX

### Added
- New feature description

### Fixed
- Bug fix description
```

**3. Commit Changes**

```bash
cd scrapegraph-js
git add package.json CHANGELOG.md
git commit -m "chore(release): 1.5.0"
git tag v1.5.0-js
git push origin main --tags
```

**4. Test Package Locally**

```bash
cd scrapegraph-js

# Install in test directory
mkdir test-install
cd test-install
npm init -y
npm install ..

# Test import
node -e "const { smartScraper } = require('scrapegraph-js'); console.log('Success!');"
```

**5. Publish to npm**

```bash
cd scrapegraph-js

# Login to npm (if not already)
npm login

# Publish package
npm publish

# Or publish with tag
npm publish --tag beta
```

**6. Create GitHub Release**

1. Go to https://github.com/ScrapeGraphAI/scrapegraph-sdk/releases/new
2. Tag: `v1.5.0-js`
3. Title: `JavaScript SDK v1.5.0`
4. Description: Copy from CHANGELOG.md
5. Publish release

---

## Release Checklist

### Pre-Release

- [ ] All tests passing locally
- [ ] Code formatted and linted
- [ ] Documentation updated
- [ ] Examples updated
- [ ] CHANGELOG.md entries added (if manual)
- [ ] Version number bumped (if manual)
- [ ] Breaking changes documented

### Python SDK Release

- [ ] `pyproject.toml` version updated
- [ ] Tests pass: `pytest tests/ -v`
- [ ] Linting pass: `make lint`
- [ ] Type check pass: `mypy scrapegraph_py/`
- [ ] Package builds: `uv build`
- [ ] GitHub release created
- [ ] PyPI package published
- [ ] Installation tested: `pip install scrapegraph-py==X.Y.Z`

### JavaScript SDK Release

- [ ] `package.json` version updated
- [ ] Tests pass: `npm test`
- [ ] Linting pass: `npm run lint`
- [ ] GitHub release created
- [ ] npm package published
- [ ] Installation tested: `npm install scrapegraph-js@X.Y.Z`

### Post-Release

- [ ] Verify GitHub release appears
- [ ] Verify package on PyPI/npm
- [ ] Test installation from registry
- [ ] Update documentation website (if applicable)
- [ ] Announce release (if major/minor)
- [ ] Monitor for issues

---

## Hotfix Process

For critical bugs requiring immediate fix:

**1. Create Hotfix Branch**

```bash
git checkout main
git pull
git checkout -b hotfix/critical-bug
```

**2. Fix Bug**

Make minimal changes to fix the issue.

**3. Commit with Fix Type**

```bash
git commit -m "fix: critical bug description"
```

**4. Fast-Track PR**

- Create PR
- Request immediate review
- Merge as soon as approved

**5. Release**

Automated release triggers immediately, creating a **patch** version (0.0.x).

---

## Rollback Procedure

If a release has critical issues:

### Option 1: Yank Package (Recommended)

**PyPI:**
```bash
# Yank version (marks as unusable but keeps it)
pip install twine
twine upload --repository pypi --skip-existing dist/*
# Contact PyPI admins to yank version
```

**npm:**
```bash
# Deprecate version
npm deprecate scrapegraph-js@X.Y.Z "Critical bug - use X.Y.Z+1 instead"

# Or unpublish (within 72 hours)
npm unpublish scrapegraph-js@X.Y.Z
```

### Option 2: Publish Fix Version

Faster and preferred:

1. Create hotfix branch
2. Fix issue
3. Commit: `fix: resolve critical issue from vX.Y.Z`
4. Merge to trigger new release (patch bump)
5. Announce fix version

---

## Versioning Strategy

### Major Version (x.0.0)

Breaking changes requiring user code updates:
- API interface changes
- Removing deprecated features
- Changing default behavior

**Example:**
```
feat!: change authentication method

BREAKING CHANGE: API key must now be passed explicitly to Client().
Use Client.from_env() to load from environment variable.
```

### Minor Version (0.x.0)

New features, backward compatible:
- Adding new endpoints
- Adding optional parameters
- New functionality

**Example:**
```
feat: add scheduled jobs endpoint

Implement full CRUD for scheduled jobs with cron support.
```

### Patch Version (0.0.x)

Bug fixes, no new features:
- Fixing bugs
- Performance improvements
- Documentation updates

**Example:**
```
fix: handle network timeout correctly

Add retry logic for transient network failures.
```

---

## Troubleshooting

### Issue: semantic-release not triggering

**Causes:**
- No semantic commits since last release
- Commits use wrong format (e.g., `Fix bug` instead of `fix: bug`)
- GitHub token permissions issue

**Solutions:**
- Check commit messages: `git log --oneline`
- Ensure at least one feat/fix commit exists
- Verify GitHub Actions has write permissions

### Issue: PyPI upload fails

**Causes:**
- Authentication error
- Version already exists
- Package name conflict

**Solutions:**
- Verify `PYPI_API_TOKEN` secret in GitHub
- Check if version already on PyPI
- Try manual upload with `twine upload dist/*`

### Issue: npm publish fails

**Causes:**
- Not logged in
- Version already exists
- Permission error

**Solutions:**
- Run `npm login`
- Increment version number
- Verify npm account has publish rights

### Issue: Tests failing in CI

**Causes:**
- Environment differences
- Missing dependencies
- Network issues

**Solutions:**
- Run tests locally first
- Check CI logs for specific errors
- Verify all dependencies in `pyproject.toml` / `package.json`

---

## Semantic Release Configuration

### Python SDK

**File**: `.releaserc.yml` (root)

```yaml
branches:
  - main
plugins:
  - "@semantic-release/commit-analyzer"
  - "@semantic-release/release-notes-generator"
  - "@semantic-release/changelog"
  - ["semantic-release-pypi", { pkgdir: "scrapegraph-py" }]
  - "@semantic-release/github"
  - ["@semantic-release/git", {
      "assets": ["scrapegraph-py/CHANGELOG.md", "scrapegraph-py/pyproject.toml"],
      "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
    }]
```

### JavaScript SDK

**File**: `scrapegraph-js/.releaserc`

```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    "@semantic-release/github",
    ["@semantic-release/git", {
      "assets": ["package.json", "CHANGELOG.md"],
      "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
    }]
  ]
}
```

---

## Best Practices

1. **Use Descriptive Commits**: Help users understand what changed
2. **Test Before Merge**: Run full test suite locally
3. **Update Examples**: Ensure examples work with new features
4. **Document Breaking Changes**: Clearly explain migration path
5. **Monitor After Release**: Watch for issues in first 24 hours
6. **Communicate Major Changes**: Announce breaking changes in advance

---

**For questions, refer to [.agent/README.md](../README.md) or create a GitHub issue.**
