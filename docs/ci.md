# Continuous Integration Pipeline

This repository uses a four-stage GitHub Actions workflow defined in `.github/workflows/ci.yml`. Each stage is an independent job so teams can reason about quality, security, and packaging concerns in isolation.

## 1. Lint
- **Purpose:** Source-of-truth style enforcement (`flake8`) across the Flask app, CLI helpers, and tests.
- **Owner:** Application Engineering.
- **Command:** `pipenv run lint`
- **Failure handling:** Fix Python syntax/style issues before re-running CI.

## 2. Unit Tests
- **Purpose:** Execute request-level and service unit tests (`unittest`) to guard behaviour.
- **Owner:** Application Engineering.
- **Command:** `pipenv run python -m unittest`
- **Dependencies:** Requires Lint to succeed to avoid shipping unformatted code.

## 3. Dependency Audit
- **Purpose:** Run `pipenv run pip-audit` to surface vulnerable dependencies using the locked environment.
- **Owner:** DevOps / Security Engineering.
- **Notes:** Use `pipenv update <package>` (and update the lockfile) when remediation is required.

## 4. Package Artifact
- **Purpose:** Produce a deployment-ready tarball containing application code and configuration for downstream environments.
- **Owner:** DevOps.
- **Output:** Uploaded as the `not-purple-please-build` workflow artifact.
- **Dependencies:** Runs only after quality and security stages pass.

## 5. Deploy Staging (develop branch)
- **Purpose:** Ship the latest `develop` build to the Railway staging environment once quality gates succeed.
- **Owner:** DevOps.
- **Command:** CI executes `railway up --service $RAILWAY_STAGING_SERVICE_ID` using the artifact from the Package stage.
- **Gate:** Only runs for `push` events on `develop` and requires the GitHub `staging` environment secrets.

### Local Reproduction
```
pipenv install --dev
pipenv run ci          # orchestrates lint, tests, audit, packaging
```
`pipenv run ci` executes `scripts/ci.sh`, mirroring the quality/security stages of the GitHub Actions workflow locally (it stops before deployment). The final tarball mirrors the CI artifact, enabling DevOps to validate deployment steps outside of GitHub Actions.

### Secrets & environment setup
1. Create a staging environment in Railway and grab the corresponding service ID (`railway service list` or the UI).
2. Generate a deployment token scoped to that staging environment (`Project Settings → Tokens`).
3. In GitHub, create an environment named `staging` and add:
   - `RAILWAY_STAGING_TOKEN` (token from step 2)
   - `RAILWAY_STAGING_SERVICE_ID`
4. In Railway, disable automatic deploys for the staging service (Autodeploy → **Manual**) so GitHub Actions is the single deploy trigger, or enable *Wait for CI* if you keep branch-based autodeploys.
5. Optional: add protected rules/approvals to the GitHub `staging` environment for added safety.
