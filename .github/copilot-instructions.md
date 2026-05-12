# Copilot Instructions — data-platform-lab

Purpose: quick, repo-specific guidance for Copilot sessions working in this monorepo.

---

1) Build / test / lint commands

- Docs (VitePress):
  - Install dependencies: npm install
  - Local dev server: npm run docs:dev
  - Build static site: npm run docs:build
  - Preview built site: npm run docs:preview
  - CI / deploy: .github/workflows/deploy-docs.yml runs `npm run docs:build` and publishes `docs/.vitepress/dist` to GitHub Pages.

- Tests & linters:
  - No repository-level test or lint scripts are enforced. Tests are placed under `tests/` with subfolders `unit`, `integration`, and `data-quality`.
  - Common Python runner examples (used when adding Python tests):
    - Run full suite: pytest
    - Run a single file: pytest tests/unit/path/to/test_file.py
    - Run a single test: pytest tests/unit/path/to/test_file.py::test_name
  - If adding linting/formatting, prefer tools that integrate into CI (e.g., ruff/flake8/black/mypy) and create scripts in package.json or a Makefile.

---

2) High-level architecture (big picture)

- Monorepo for Data Platform experiments and docs-as-code. Top-level areas:
  - docs/ — VitePress documentation site (see package.json scripts and .vitepress config).
  - platform/ — platform examples and reference implementations:
    - platform/airflow/ — DAGs, custom operators, sensors.
    - platform/beam/ — Apache Beam pipelines and templates.
    - platform/sql/ — example queries and SQL artifacts.
    - platform/shared/ — utilities shared across examples.
  - infra/ — infrastructure code and patterns (docker, kubernetes, terraform).
  - ai/ — ADRs, prompts, patterns (AI-first decision records live here).
  - tests/ — organized test suites by type.
  - experiments/ and sandbox/ — research and playground code.

- Runtime/entry points:
  - Airflow DAG discovery expects DAG files inside platform/airflow/dags/; operators/sensors are referenced from their modules.
  - Beam pipelines live under platform/beam/ and are standalone pipeline scripts or templates.

---

3) Key conventions and repository patterns

- Docs-as-code: author docs in docs/ with VitePress. Validate changes with `npm run docs:build`.

- ADRs & AI artifacts: ai/decisions contains ADR markdown (e.g., adr-001-vitepress.md) documenting chosen patterns — consult these before changing architecture decisions.

- Platform layout conventions:
  - Airflow code: keep DAG definitions in `platform/airflow/dags/`; custom operators and sensors under `platform/airflow/operators` and `platform/airflow/sensors`.
  - Beam: pipelines and transforms grouped under `platform/beam/`.
  - SQL artifacts: organized inside `platform/sql/`.

- Tests: follow the existing tests/ subfolder organisation when adding new tests.

- CI: Only docs deployment is configured. Placeholder workflows exist: `.github/workflows/ci-python.yml`, `lint.yml`, and `validate-docs.yml` are present but empty; use them as insertion points when adding CI for tests/linting/validation.

- AI-first files: ai/prompts and ai/patterns contain useful templates for generating or reviewing architecture and pipeline code — reuse rather than hardcoding new prompts.

- No other assistant configuration files detected (CLAUDE.md, AGENTS.md, .cursorrules, etc.). If adding those, list them here.

---

4) Files to check first in a session

- package.json — docs scripts and vitepress dev dependencies.
- docs/.vitepress — site config and plugin settings.
- ai/decisions and ai/prompts — architecture rationale and prompt templates.
- platform/airflow/dags/ — entrypoints for orchestration work.
- tests/ — where to run or add tests.

---

5) Notes for Copilot actions

- Prefer non-invasive edits for platform code; these modules may be run in cloud environments.
- When modifying docs run `npm run docs:build` locally to validate the site before committing.
- If asked to add CI for tests or linting, use the empty workflow placeholders and add minimal jobs that install dependencies and run the chosen tools.
- When recommending new tools (test runners, linters), suggest concrete package.json scripts and CI steps.

---

Platform conventions:
- use BigQuery as analytical warehouse
- use GCS raw/staging/curated layers
- use Apache Beam for distributed transformations
- use Composer/Airflow for orchestration
- prefer configuration-driven ingestion patterns
- separate control plane and execution plane
- prefer AVRO for raw ingestion storage
- support CMEK-aware architectures when applicable

Observability standards:
- all pipelines must emit structured logs
- all jobs should expose execution metadata
- prefer centralized audit tables
- include retry-safe and idempotent behavior

Documentation standards:
- document architecture decisions using ADRs
- include Mermaid diagrams for workflows
- keep VitePress documentation updated with implementation changes