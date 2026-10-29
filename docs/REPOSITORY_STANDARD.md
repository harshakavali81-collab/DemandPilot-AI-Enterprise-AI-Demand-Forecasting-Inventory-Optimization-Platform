# Repository standard

## Layout

This repository keeps its working source paths. A shared portfolio structure does not require moving a React application, Python package, BI workbook or Verilog project into identical runtime directories.

| Area | Convention |
| --- | --- |
| Landing page | `README.md`: purpose, visuals, demo, features, stack, architecture, setup, tradeoffs and roadmap |
| Detailed reference | `PROJECT_GUIDE.md`: retained project-specific explanation and historical release notes |
| Documentation | `docs/`: design, inventory, reproduction and evidence |
| Work intake | `.github/ISSUE_TEMPLATE/`: bug and feature forms |
| Review | `.github/PULL_REQUEST_TEMPLATE.md`: linked issue, behavior and validation |
| Automation | `.github/workflows/portfolio-docs.yml`: README section and local-link checks |
| Source and tests | Existing project-specific paths listed below; no empty source/test placeholders |

## Workflow

1. Open an issue describing the user problem and measurable acceptance criteria.
2. Add it to a GitHub Project with Todo, In progress, Review and Done states when a board is configured.
3. Use a focused branch and meaningful commits, such as `docs: correct local setup paths` or `fix(api): reject malformed input`.
4. Run the project's documented checks and `python scripts/check_portfolio_docs.py`.
5. Open a pull request with actual validation results and `Closes #<issue-number>`.
6. Merge after review; record release evidence and update the issue/board.

Board creation, profile pins, repository social previews and milestone settings require account-level configuration. This file does not claim those settings have been applied.

## Validation scope

The documentation check validates the landing-page headings and local link targets only. It does not execute models, certify test coverage, inspect Git history for secrets, verify external websites, or prove production readiness. Existing application workflows remain the source of runtime CI evidence.

Keep credentials in local environment variables. A gitignore rule does not remove secrets already tracked or committed. Use only permitted sample data in public demos.

## Inventory at standardization

The following are the pre-existing public project files. New standardization files are described above. Historical guides may mention external bundles that are not part of this list.

- [`Dockerfile`](<../Dockerfile>)
- [`README.md`](<../README.md>)
- [`artifacts`](<../artifacts>)
- [`artifacts/.gitkeep`](<../artifacts/.gitkeep>)
- [`artifacts/metrics.json`](<../artifacts/metrics.json>)
- [`dashboard`](<../dashboard>)
- [`dashboard/app.py`](<../dashboard/app.py>)
- [`data`](<../data>)
- [`data/processed`](<../data/processed>)
- [`data/processed/.gitkeep`](<../data/processed/.gitkeep>)
- [`data/raw`](<../data/raw>)
- [`data/raw/.gitkeep`](<../data/raw/.gitkeep>)
- [`data/sample`](<../data/sample>)
- [`data/sample/sales_demo.csv`](<../data/sample/sales_demo.csv>)
- [`docker-compose.yml`](<../docker-compose.yml>)
- [`docs`](<../docs>)
- [`docs/architecture.md`](<../docs/architecture.md>)
- [`docs/data_dictionary.md`](<../docs/data_dictionary.md>)
- [`docs/deployment.md`](<../docs/deployment.md>)
- [`docs/model_card.md`](<../docs/model_card.md>)
- [`notebooks`](<../notebooks>)
- [`notebooks/01_exploratory_analysis.ipynb`](<../notebooks/01_exploratory_analysis.ipynb>)
- [`pyproject.toml`](<../pyproject.toml>)
- [`reports`](<../reports>)
- [`reports/eda_summary.json`](<../reports/eda_summary.json>)
- [`reports/figures`](<../reports/figures>)
- [`reports/figures/.gitkeep`](<../reports/figures/.gitkeep>)
- [`reports/figures/evaluation.svg`](<../reports/figures/evaluation.svg>)
- [`scripts`](<../scripts>)
- [`scripts/bootstrap.py`](<../scripts/bootstrap.py>)
- [`scripts/forecast_example.py`](<../scripts/forecast_example.py>)
- [`scripts/make_report.py`](<../scripts/make_report.py>)
- [`scripts/prepare_data.py`](<../scripts/prepare_data.py>)
- [`scripts/seed_demo.py`](<../scripts/seed_demo.py>)
- [`scripts/train_model.py`](<../scripts/train_model.py>)
- [`src`](<../src>)
- [`src/demandpilot`](<../src/demandpilot>)
- [`src/demandpilot/__init__.py`](<../src/demandpilot/__init__.py>)
- [`src/demandpilot/api`](<../src/demandpilot/api>)
- [`src/demandpilot/api/__init__.py`](<../src/demandpilot/api/__init__.py>)
- [`src/demandpilot/api/main.py`](<../src/demandpilot/api/main.py>)
- [`src/demandpilot/api/schemas.py`](<../src/demandpilot/api/schemas.py>)
- [`src/demandpilot/config.py`](<../src/demandpilot/config.py>)
- [`src/demandpilot/data`](<../src/demandpilot/data>)
- [`src/demandpilot/data/__init__.py`](<../src/demandpilot/data/__init__.py>)
- [`src/demandpilot/data/generate.py`](<../src/demandpilot/data/generate.py>)
- [`src/demandpilot/data/validate.py`](<../src/demandpilot/data/validate.py>)
- [`src/demandpilot/features`](<../src/demandpilot/features>)
- [`src/demandpilot/features/__init__.py`](<../src/demandpilot/features/__init__.py>)
- [`src/demandpilot/features/build_features.py`](<../src/demandpilot/features/build_features.py>)
- [`src/demandpilot/inventory`](<../src/demandpilot/inventory>)
- [`src/demandpilot/inventory/__init__.py`](<../src/demandpilot/inventory/__init__.py>)
- [`src/demandpilot/inventory/optimizer.py`](<../src/demandpilot/inventory/optimizer.py>)
- [`src/demandpilot/modeling`](<../src/demandpilot/modeling>)
- [`src/demandpilot/modeling/__init__.py`](<../src/demandpilot/modeling/__init__.py>)
- [`src/demandpilot/modeling/evaluate.py`](<../src/demandpilot/modeling/evaluate.py>)
- [`src/demandpilot/modeling/forecast.py`](<../src/demandpilot/modeling/forecast.py>)
- [`src/demandpilot/modeling/train.py`](<../src/demandpilot/modeling/train.py>)
- [`src/demandpilot/storage`](<../src/demandpilot/storage>)
- [`src/demandpilot/storage/__init__.py`](<../src/demandpilot/storage/__init__.py>)
- [`src/demandpilot/storage/database.py`](<../src/demandpilot/storage/database.py>)
- [`tests`](<../tests>)
- [`tests/test_api.py`](<../tests/test_api.py>)
- [`tests/test_features.py`](<../tests/test_features.py>)
- [`tests/test_forecast.py`](<../tests/test_forecast.py>)
- [`tests/test_inventory.py`](<../tests/test_inventory.py>)
- [`tests/test_training.py`](<../tests/test_training.py>)
