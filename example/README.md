## Instructions

* `cd example`
* `flytectl sandbox start --source=$(pwd)` (create flyte-sandbox environment)
* `flytectl sandbox exec -- docker build . --tag "hp:v1" -f house_price_prediction/Dockerfile` (build Docker container)
* `pyflyte --pkgs house_price_prediction package --image hp:v1 --force` (package code)
* `flytectl register files --project flytesnacks --domain development --archive flyte-package.tgz --version v1` (register code)
* `flyte-cli setup-config -h localhost:30081 -i` (initialize config)
* Run the `flyte_remote.ipynb` notebook

To run multiregion code, modify `house_price_prediction.house_price_predictor.house_price_predictor_trainer` to `house_price_prediction.multiregion_house_price_predictor.multi_region_house_price_prediction_model_trainer`.
