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

### Local Reproduction
```
pipenv install --dev
pipenv run ci          # orchestrates lint, tests, audit, packaging
```
`pipenv run ci` executes `scripts/ci.sh`, mirroring the GitHub Actions workflow locally. The final tarball mirrors the CI artifact, enabling DevOps to validate deployment steps outside of GitHub Actions.
