# Setup Instructions

1. In the example directory, run:
    * `flytectl sandbox start --source=$(pwd)`
    * `flytectl sandbox exec -- docker build . --tag "hp:v1" -f house_price_prediction/Dockerfile`
    * `pyflyte --pkgs house_price_prediction package --image hp:v1 --force`
    * `flytectl register files --project flytesnacks --domain development --archive flyte-package.tgz --version v1`
2. Run the command: `flyte-cli setup-config -h localhost:30081 -i`
2. Run the command: `python flyte_remote.py`

To run multiregion code, modify `house_price_prediction.house_price_predictor.house_price_predictor_trainer` to `house_price_prediction.multiregion_house_price_predictor.multi_region_house_price_prediction_model_trainer`.
