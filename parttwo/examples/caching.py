"""
Caching
--------

Flyte provides the ability to cache the output of task executions to make the subsequent executions faster.
A well-behaved Flyte task should generate deterministic output given the same inputs and task functionality.
"""
# %%
# Let's first import the necessary dependencies.
import os

import flytekit
import pandas as pd

from flytekit import task, workflow
from flytekit.types.file import FlyteFile


# %%
# Task caching is disabled by default to avoid unintended consequences of caching tasks with side effects.
# To enable caching and control its behavior, use the ``cache`` and ``cache_version`` parameters when constructing a task.
#
# `cache` is a switch to enable or disable the cache, and `cache_version` pertains to the version of the cache.
# ``cache_version`` field indicates that the task functionality has changed.
# Bumping the ``cache_version`` is akin to invalidating the cache.
#
# Flyte users can manually update this version and Flyte will cache the next execution instead of relying on the old cache.
@task(cache=True, cache_version="1.0")
def init_dataset() -> FlyteFile:
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    working_dir = flytekit.current_context().working_directory
    out_path = os.path.join(working_dir, "dataset.csv")
    df.to_csv(out_path)
    return FlyteFile(path=out_path)


@workflow
def caching_wf() -> FlyteFile:
    return init_dataset()


if __name__ == "__main__":
    print(f"Running {__file__} main ...")
    print(f"Running caching_wf(), the dataset is {caching_wf()}")
# %%
# In the above example, calling `init_dataset()` twice (even if it's across different executions or different workflows) will only execute the dataset initialization once.
# The next time, the output will be made available immediately -- (captured from the previous execution with the same inputs).