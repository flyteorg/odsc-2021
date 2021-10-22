"""
Customizing Task Resources
---------------------------

One of the reasons to use a hosted Flyte environment is the potential of leveraging CPU, memory, and storage resources, far greater than what's available locally.
Flytekit makes it possible to specify these requirements declaratively and close to where the task itself is declared.

Tasks can have ``requests`` and ``limits``.
A task can possibly be allocated more resources than it requests, but never more than its limit.
Requests are treated as hints which are used to schedule tasks on nodes with available resources, whereas limits
are hard constraints.

The following attributes can be specified for a ``Resource``.

#. ``cpu``
#. ``mem``
#. ``gpu``
"""

# %%
# In this example, the memory required by the function increases as the dataset size increases.
# Large datasets may not be able to run locally, so we would want to provide hints to Flyte backend to request for more memory.
# This is done by simply decorating the task with the hints as shown in the following code sample.


# %%
# Let's import the dependencies.
# To run the code locally, do `pip install bing-image-downloader`.
import flytekit
import os

from flytekit import Resources, task, workflow
from bing_image_downloader import downloader
from flytekit.types.directory import FlyteDirectory


# %%
# We define a task to fetch _x_ random URLs from the internet.
@task(limits=Resources(mem="600Mi"))
def fetch_urls(query: str, number_of_images: int) -> FlyteDirectory:
    working_dir = flytekit.current_context().working_directory
    downloader.download(
        query, limit=number_of_images, output_dir=os.path.join(working_dir, "images")
    )
    return FlyteDirectory(path=os.path.join(working_dir, "images"))


# %%
# Next, we define a workflow.
@workflow
def wf(query: str, number_of_images: int) -> FlyteDirectory:
    return fetch_urls(query=query, number_of_images=number_of_images)


# %%
# Lastly, we can run the workflow locally.
if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(
        f"Running wf(query='car'), the output is {wf(query='car', number_of_images=5)}"
    )
