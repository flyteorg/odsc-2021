"""
Conditional Branching
---------------------

Flytekit supports conditions as a first class construct in the language. Conditions offer a way to selectively execute
branches of a workflow based on static or dynamic data produced by other tasks or come in as workflow inputs.
Conditions are very performant to be evaluated, however, they are limited to certain binary and logical operators and can
only be performed on primitive values.
"""

# %%
# To start off, import the conditional module.
import random

from flytekit import conditional, task, workflow

# %%
# We define two tasks: `square` and `double`.
@task
def square(n: float) -> float:
    """
    Parameters:
        n (float): name of the parameter for the task will be derived from the name of the input variable
               the type will be automatically deduced to be Types.Integer
    Return:
        float: The label for the output will be automatically assigned and type will be deduced from the annotation
    """
    return n * n


@task
def double(n: float) -> float:
    """
    Parameters:
        n (float): name of the parameter for the task will be derived from the name of the input variable
               the type will be automatically deduced to be Types.Integer
    Return:
        float: The label for the output will be automatically assigned and type will be deduced from the annotation
    """
    return 2 * n


# %%
# Next, we consume the output returned by the conditional() in a subsequent task.
# The conditional() triggers `double()` if the value lies between 0.1 and 1.0, triggers `square()` if the value lies between 1.0 and 10.0, or prints the failure message.
@workflow
def multiplier(my_input: float) -> float:
    d = (
        conditional("fractions")
        .if_((my_input > 0.1) & (my_input < 1.0))
        .then(double(n=my_input))
        .elif_((my_input > 1.0) & (my_input < 10.0))
        .then(square(n=my_input))
        .else_()
        .fail("The input must be between 0 and 10")
    )

    # d will either be the output of `double` or `square`. If the conditional() falls through the fail
    # branch, execution will not reach here.
    return double(n=d)


if __name__ == "__main__":
    print(f"Running {__file__} main ...")
    print(f"Output of multiplier(my_input=5.0): {multiplier(my_input=5.0)}")