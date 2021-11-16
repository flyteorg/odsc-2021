"""
Predicting House Price in a Region with XGBoost
------------------------------------------------
"""

# %%
# Install the following three libraries before running the model (locally):
#
# .. code-block:: python
#
#       pip install scikit-learn
#       pip install joblib
#       pip install xgboost

# %%
# Importing the Libraries
# =======================
#
# First, import all the required libraries.
import typing

import os
import flytekit
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from flytekit import Resources, task, workflow
from flytekit.types.file import JoblibSerializedFile
from typing import Tuple

# %%
# Initializing the Variables
# ==========================
#
# Initialize the variables to be used while building the model.
NUM_HOUSES_PER_LOCATION = 1000
COLUMNS = [
    "PRICE",
    "YEAR_BUILT",
    "SQUARE_FEET",
    "NUM_BEDROOMS",
    "NUM_BATHROOMS",
    "LOT_ACRES",
    "GARAGE_SPACES",
]
MAX_YEAR = 2021
SPLIT_RATIOS = [0.6, 0.3, 0.1]

# %%
# Defining the Data Generation Functions
# ======================================
#
# Define a function to generate the price of a house.
def gen_price(house) -> int:
    _base_price = int(house["SQUARE_FEET"] * 150)
    _price = int(
        _base_price
        + (10000 * house["NUM_BEDROOMS"])
        + (15000 * house["NUM_BATHROOMS"])
        + (15000 * house["LOT_ACRES"])
        + (15000 * house["GARAGE_SPACES"])
        - (5000 * (MAX_YEAR - house["YEAR_BUILT"]))
    )
    return _price


# %%
# Define a function that returns a DataFrame object constituting all the houses' details.
def gen_houses(num_houses) -> pd.DataFrame:
    _house_list = []
    for _ in range(num_houses):
        _house = {
            "SQUARE_FEET": int(np.random.normal(3000, 750)),
            "NUM_BEDROOMS": np.random.randint(2, 7),
            "NUM_BATHROOMS": np.random.randint(2, 7) / 2,
            "LOT_ACRES": round(np.random.normal(1.0, 0.25), 2),
            "GARAGE_SPACES": np.random.randint(0, 4),
            "YEAR_BUILT": min(MAX_YEAR, int(np.random.normal(1995, 10))),
        }
        _price = gen_price(_house)
        _house_list.append(
            [
                _price,
                _house["YEAR_BUILT"],
                _house["SQUARE_FEET"],
                _house["NUM_BEDROOMS"],
                _house["NUM_BATHROOMS"],
                _house["LOT_ACRES"],
                _house["GARAGE_SPACES"],
            ]
        )
    _df = pd.DataFrame(
        _house_list,
        columns=COLUMNS,
    )
    return _df


# %%
# Split the data into train, val, and test datasets.
def split_data(
    df: pd.DataFrame, seed: int, split: typing.List[float]
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    seed = seed
    val_size = split[1]
    test_size = split[2]

    num_samples = df.shape[0]
    x1 = df.values[
        :num_samples, 1:
    ]  # keep only the features, skip the target, all rows
    y1 = df.values[:num_samples, :1]  # keep only the target, all rows

    # Use split ratios to divide up into train & test
    x_train, x_test, y_train, y_test = train_test_split(
        x1, y1, test_size=test_size, random_state=seed
    )
    # Of the remaining training samples, give proper ratio to train & validation
    x_train, x_val, y_train, y_val = train_test_split(
        x_train,
        y_train,
        test_size=(val_size / (1 - test_size)),
        random_state=seed,
    )

    # Reassemble the datasets with target in first column and features after that
    _train = np.concatenate([y_train, x_train], axis=1)
    _val = np.concatenate([y_val, x_val], axis=1)
    _test = np.concatenate([y_test, x_test], axis=1)

    return (
        pd.DataFrame(
            _train,
            columns=COLUMNS,
        ),
        pd.DataFrame(
            _val,
            columns=COLUMNS,
        ),
        pd.DataFrame(
            _test,
            columns=COLUMNS,
        ),
    )


# %%
# Task: Generating & Splitting the Data
# =====================================
#
# Call the previously defined helper functions to generate and split the data. Finally, return the DataFrame objects.
dataset = typing.NamedTuple(
    "GenerateSplitDataOutputs",
    train_data=pd.DataFrame,
    val_data=pd.DataFrame,
    test_data=pd.DataFrame,
)


@task(cache=True, cache_version="0.1", limits=Resources(mem="600Mi"))
def generate_and_split_data(number_of_houses: int, seed: int) -> dataset:
    # TODO: Generate data and split it into train, val, test by calling gen_houses and split_data
    ...

# %%
# Trigger the task locally by calling the task function.
if __name__ == "__main__":
    # TODO: Call the task function


# %%
# The output will be a list of house price predictions.
