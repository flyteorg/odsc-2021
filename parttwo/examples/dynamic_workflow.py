"""
Dynamic Workflow

Explore the classification accuracy of the KNN algorithm with k values ranging from 2 to 7

Install the following libraries before running the model (locally).
* pip install scikit-learn
* pip install joblib
"""

import os
from typing import List, Tuple
from statistics import mean, pstdev

import joblib
from flytekit import Resources, dynamic, task, workflow
from flytekit.types.file import JoblibSerializedFile
from sklearn.datasets import make_classification
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

# %%
# Let's first import the libraries.
@task(cache=True, cache_version="0.1", limits=Resources(mem="600Mi"))
def get_dataset() -> Tuple[List[List[float]], List[int]]:
    """Fetch the dataset"""

    # Generate a random n-class classification problem
    X, y = make_classification(
        n_samples=5000, n_features=15, n_informative=10, n_redundant=3, random_state=5
    )
    return X.tolist(), y.tolist()


# %%
# Next, we define tasks to fetch the dataset and build models with different k values.
@task(cache=True, cache_version="0.1", limits=Resources(mem="600Mi"))
def get_models() -> List[JoblibSerializedFile]:
    """Get a list of models to evaluate, each with a specific 'k' value"""

    models = list()

    for n in range(2, 5):
        fname = "model-k" + str(n) + ".joblib.dat"

        # Serialize model using joblib
        joblib.dump(KNeighborsClassifier(n_neighbors=n), fname)
        models.append(fname)

    return models


@task
def helper_evaluate_model(name: str, scores: List[float]) -> List[str]:
    """A helper task to depict calling a task within a dynamic workflow loop"""
    return [
        str(os.path.basename(name)),
        str(round(mean(scores), 2)),
        str(round(pstdev(scores), 3)),
    ]


# %%
# We now define a dynamic workflow that loops through the models and computes the cross-validation score.
# Moreover, we define a helper task that returns the appropriate score for every model.
@dynamic(cache=True, cache_version="0.1", limits=Resources(mem="1000Mi"))
def evaluate_model(
    models: List[JoblibSerializedFile],
    X: List[List[float]],
    y: List[int],
) -> List[List[str]]:
    """
    A dynamic workflow to compute the cross-validation score across different models
    All Promise objects passed as arguments are accessible here
    This is compiled at execution time
    """

    final_result = list()

    """
    models = get_models()
    for model_ser in models:
        ...

    This results in a compilation error as 'models' is a Promise object which cannot be looped over
    """

    # Loop through the list of models
    for model_ser in models:

        # Fetch the unserialized model
        model = joblib.load(model_ser)

        # Cross-validation splitting strategy
        cv = RepeatedStratifiedKFold(n_splits=7, n_repeats=2, random_state=1)

        # Peform cross-validation
        scores = cross_val_score(model, X, y, scoring="accuracy", cv=cv, n_jobs=-1)

        """
        'model', 'cv', and 'scores' are all accessible
        Similarly, return values of Python functions (non-tasks) are accessible
        """

        """
        Call a task and store the file name, accuracy, and standard deviation
        The return value of the task is a Promise object
        """
        final_result.append(
            helper_evaluate_model(name=str(model_ser), scores=scores.tolist())
        )

    return final_result


# %%
# Finally, we define a workflow that calls the above-mentioned tasks and dynamic workflow.
@workflow
def wf() -> List[List[str]]:
    """
    A workflow to call the concerned tasks
    This is compiled at compile time
    """

    """Get the dataset. 'X' and 'y' aren't accessible as they are Promise objects"""
    X, y = get_dataset()

    """Get the models to evaluate. 'models' is a Promise object"""
    models = get_models()

    """
    Fetch the accuracy
    When 'models' is sent to the dynamic workflow, it becomes accessible in the respective Flyte units
    """
    return evaluate_model(models=models, X=X, y=y)


if __name__ == "__main__":
    print(f"Running {__file__} main ...")
    print(f"Running wf(), {wf()}")
