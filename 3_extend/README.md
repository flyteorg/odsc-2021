## Instructions

### [XGBoost Plugin](./flytekit-xgboost)

* `cd 3_extend/flytekit-xgboost`
* `pip install -e .` (development mode)
* `cd tests`
* `pip install pytest`
* `pytest test_task.py -rA`

**NOTE: If using OSX, XGBoost depends on some c packages to be installed**

`brew install cmake libomp`

### [XGBoost Example](./xgboost_example)

* `cd 3_extend`
* `flytectl sandbox start --source=$(pwd)` (create flyte-sandbox environment)
* `flytectl sandbox exec -- docker build . --tag "xgboost:v1" -f xgboost_example/Dockerfile` (build Docker container)
* `pyflyte --pkgs xgboost_example package --image xgboost:v1 --force` (package code)
* `flytectl register files --project flytesnacks --domain development --archive flyte-package.tgz --version v1` (register code)
* Hit the URL http://localhost:30081/console/projects/flytesnacks/domains/development/workflows/xgboost_example.example.full_pipeline
* Launch the workflow!
