"""
FlyteSchema
-----------

FlyteSchema repesents tabular data, e.g., pandas DataFrame, spark dataframe, etc.

This example demonstrates how to use typed FlyteSchema.
"""

# %%
# First, we import the dependencies.
import pandas
from flytekit import kwtypes, task, workflow

# %%
# Flytekit consists of some pre-built type extenstions, one of them is the FlyteSchema type.
from flytekit.types.schema import FlyteSchema

# %%
# FlyteSchema is an abstract Schema type that can be used to represent any structured dataset which has typed
# (or untyped) columns.
out_schema = FlyteSchema[kwtypes(x=int, y=str)]


# %%
# We define a task to write to the schema using the `write()` method.
@task
def t1() -> out_schema:
    w = out_schema()
    df = pandas.DataFrame(data={"x": [1, 2], "y": ["3", "4"]})
    w.open().write(df)
    return w


# %%
# To read a Schema, one has to invoke the `open()` method. The default mode
# is automatically configured to be `open` and the default returned dataframe type is `pandas.DataFrame`.
# Different types of dataframes can be returned based on the type passed into the open method.
@task
def t2(schema: FlyteSchema[kwtypes(x=int, y=str)]) -> FlyteSchema[kwtypes(x=int)]:
    assert isinstance(schema, FlyteSchema)
    df: pandas.DataFrame = schema.open().all()
    return df[schema.column_names()[:-1]]


@workflow
def wf() -> FlyteSchema[kwtypes(x=int)]:
    return t2(schema=t1())


# %%
# Local execution will convert the data to and from the serialized representation, thus mimicking a complete distributed execution.
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Running wf(), returns columns {wf().columns()}")
