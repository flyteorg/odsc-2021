XGBoost Plugin
==============

About XGBoost
-------------

The XGBoost (eXtreme Gradient Boosting) is a popular and efficient open-source implementation of the gradient boosted trees algorithm. Gradient boosting is a supervised learning algorithm that attempts to accurately predict a target variable by combining an ensemble of estimates from a set of simpler and weaker models. The XGBoost algorithm performs well in machine learning competitions because of its robust handling of a variety of data types, relationships, distributions, and the variety of hyperparameters that you can fine-tune. You can use XGBoost for regression, classification (binary and multiclass), and ranking problems.

Integration Prototype
---------------------

XGBoost integration provides a simplified interface to train and evaluate models.

```python
@dataclass_json
@dataclass
class ModelParameters(object):
    """
    ModelParameters are given as arguments to the xgboost.train() method.
    """
    ...

@dataclass_json
@dataclass
class HyperParameters(object):
    """
    Hyperparameters for training a model.
    """
    ...

@dataclass_json
@dataclass
class XGBoostParameters():
    """
    XGBoost Parameter = Model Parameters + Hyperparameters
    """
    ...

class XGBoostTrainerTask(PythonInstanceTask[XGBoostParameters]):

    def __init__(
        self,
        name: str,
        inputs: Dict[str, Type],
        config: Optional[XGBoostParameters] = None,
        **kwargs,
    ):
        """
        Initialize the task configuration.
        """
        ...

    # Train method
    def train(
        self, dtrain: xgboost.DMatrix, dvalid: xgboost.DMatrix, **kwargs
    ) -> Tuple[str, Dict[str, Dict[str, List[float]]]]:
        ...

    # Test method
    def test(self, booster_model: str, dtest: xgboost.DMatrix, **kwargs) -> List[float]:
        ...

    def execute(self, **kwargs) -> Any:
        """
        * Verify if all the necessary arguments are supplied by the user
        * Generate DMatrix from FlyteFile/FlyteSchema
        * Train (optionally validate) the model
        * Generate predictions
        """
        ...
```

Simple Example
--------------

```python
import os
from typing import List

import xgboost
from flytekit import kwtypes, task, workflow
from flytekit.types.file import FlyteFile

from flytekitplugins.xgboost import (
    HyperParameters,
    ModelParameters,
    XGBoostParameters,
    XGBoostTrainerTask,
)

xgboost_trainer = XGBoostTrainerTask(
    name="test1",
    config=XGBoostParameters(
        hyper_parameters=HyperParameters(
            max_depth=2, eta=1, objective="binary:logistic", verbosity=2
        ),
        model_parameters=ModelParameters(num_boost_round=1),
    ),
    inputs=kwtypes(
        train=FlyteFile, test=FlyteFile, model_parameters=ModelParameters
    ),
)

@workflow
def train_test_wf(
    train: FlyteFile = "https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.train",
    test: FlyteFile = "https://raw.githubusercontent.com/dmlc/xgboost/master/demo/data/agaricus.txt.test",
) -> List[float]:
    _, predictions, _ = xgboost_trainer(
        train=train,
        test=test,
        model_parameters=ModelParameters(num_boost_round=2),
    )
    return predictions

assert xgboost_trainer.python_interface.inputs == {
    "train": FlyteFile,
    "test": FlyteFile,
    "model_parameters": ModelParameters,
}
train_test_wf()
```