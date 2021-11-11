## Setup Instructions

### XGBoost Plugin

In the flytekit-xgboost directory, run:
* `pip install -e .` (development mode)
* `cd tests`
* `pip install pytest`
* `pytest test_task.py -rA`

### XGBoost Example

In the integration directory, run:
* `flytectl sandbox start --source=$(pwd)` (create flyte-sandbox environment)
* `flytectl sandbox exec -- docker build . --tag "xgboost:v1" -f xgboost_example/Dockerfile` (build Docker container)
* `pyflyte --pkgs xgboost_example package --image xgboost:v1 --force` (package code)
* `flytectl register files --project flytesnacks --domain development --archive flyte-package.tgz --version v1` (register code)
