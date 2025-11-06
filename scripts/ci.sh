#!/usr/bin/env bash
set -euo pipefail

echo "==> Lint"
flake8 app controller.py gen_slack_theme.py tests

echo "==> Unit tests"
python -m unittest

echo "==> Dependency audit"
pip-audit

echo "==> Package artifact"
BUILD_DIR="build"
ARTIFACT="${BUILD_DIR}/not-purple-please.tar.gz"
rm -f "${ARTIFACT}"
mkdir -p "${BUILD_DIR}"
tar -czf "${ARTIFACT}" \
  app \
  controller.py \
  gen_slack_theme.py \
  Procfile \
  Pipfile \
  Pipfile.lock \
  README.md \
  requirements.txt \
  static

echo "==> Artifact written to ${ARTIFACT}"
