"""
Workflows
----------

Once you have a handle on tasks, we can dive into Flyte workflows. Together, Flyte tasks and workflows make up the fundamental building blocks of Flyte.

Workflows string together two or more tasks. They are also written as Python functions, but it is essential to make a
critical distinction between tasks and workflows.

The body of a task's function runs at "run time", i.e., on a K8s cluster (using the task's container), in a Query
Engine like BigQuery, or some other hosted service like AWS Batch, Sagemaker, etc. The body of a
workflow is not used for computation; it is only used to structure tasks.
The body of a workflow runs at "registration" time, i.e., the workflow unwraps during registration.
Registration refers to uploading the packaged (serialized) code to the Flyte backend so that the workflow can be triggered.
Please refer to the :std:ref:`registration docs <flyte:divedeep-registration>` to understand registration in Flyte.

Now, let's get started with a simple workflow.
"""


def add(a: int, b: int) -> int:
    return a + b


def int_to_str(a: int) -> str:
    return f"{a}"


def add_to_str(a: int, b: int) -> str:
    sum = add(a=a, b=b)
    return int_to_str(a=sum)


if __name__ == "__main__":
    print(f"Running add_to_str(a=50, b=20) {add_to_str(a=50, b=20)}")
