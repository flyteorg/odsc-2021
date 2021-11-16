from typing import Dict, List, NamedTuple

import xgboost
from flytekit import task, workflow
from flytekit.types.file import FlyteFile, JoblibSerializedFile
from flytekitplugins.xgboost import (
    HyperParameters,
    ModelParameters,
    XGBoostParameters,
    XGBoostTrainerTask,
)

xgboost_trainer = XGBoostTrainerTask(
    name="xgboost_trainer",
    config=XGBoostParameters(
        hyper_parameters=HyperParameters(
            max_depth=2, eta=1, objective="binary:logistic", verbosity=2
        ),
    ),
    dataset_type=FlyteFile,
    validate=True,
)


@task
def estimate_accuracy(predictions: List[float], test: FlyteFile) -> float:
    test.download()
    dtest = xgboost.DMatrix(test.path)
    labels = dtest.get_label()
    return (
        sum(
            1 for i in range(len(predictions)) if int(predictions[i] > 0.5) == labels[i]
        )
        / float(len(predictions))
        * 100.0
    )


wf_output = NamedTuple(
    "wf_output",
    model=JoblibSerializedFile,
    accuracy=float,
    evaluation_result=Dict[str, Dict[str, List[float]]],
)


@workflow
def xgboost_sample(
    train: FlyteFile = "https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.train",
    test: FlyteFile = "https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.test",
    validation: FlyteFile = "https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.test",
    params: XGBoostParameters = XGBoostParameters(),
) -> wf_output:
    model, predictions, evaluation_result = xgboost_trainer(
        train=train,
        test=test,
        validation=validation,
        params=params,
    )
    return (
        model,
        estimate_accuracy(
            predictions=predictions,
            test=test,
        ),
        evaluation_result,
    )


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    model, accuracy, eval_result = xgboost_sample()
    print(
        f"Running xgboost_sample(), accuracy of the XGBoost model is {accuracy:.2f}%"
    )
