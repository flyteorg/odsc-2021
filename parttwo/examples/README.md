# Caching

## Code example
Refer to the code in [caching.py](./caching.py) file.

## Local execution
`python parttwo/examples/caching.py`

## Sandbox execution
1. Package and fast-register all examples
    ```
    pyflyte --pkgs parttwo.examples package --image parttwo:v1 --force --fast
    flytectl register files --project flytesnacks --domain development --archive flyte-package.tgz --version v1-fast2
    ```
1. Visit http://localhost:30081/console/projects/flytesnacks/domains/development/workflows/parttwo.examples.caching.caching_wf and trigger the execution
2. Trigger the workflow again to fetch the cached result
3. Modify the task signature:
    ```python
    @task(cache=True, cache_version="1.0")
    def init_dataset(file_name: str) -> FlyteFile:
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        working_dir = flytekit.current_context().working_directory
        out_path = os.path.join(working_dir, file_name)
        df.to_csv(out_path)
        return FlyteFile(path=out_path)

    @workflow
    def caching_wf(file_name: str = "data.csv") -> FlyteFile:
        return init_dataset(file_name=file_name)

    if __name__ == "__main__":
        print(f"Running {__file__} main ...")
        print(f"Running caching_wf(), {caching_wf(file_name)}")
    ```
4. Package the code
    ```
    pyflyte --pkgs parttwo.examples package --image parttwo:v1 --force --fast
    ```
5. Register the example
    ```
    flytectl register files --project flytesnacks --domain development --archive flyte-package.tgz --version v1-fast3
    ```
6. Visit http://localhost:30081/console/projects/flytesnacks/domains/development/workflows/parttwo.examples.caching.caching_wf to trigger the execution

# Dynamic Workflow

## Code example
Refer to the code in [dynamic_workflow.py](./dynamic_workflow.py) file.

## Local execution
`python parttwo/examples/dynamic_workflow.py`

## Sandbox execution
Visit http://localhost:30081/console/projects/flytesnacks/domains/development/workflows/parttwo.examples.dynamic_workflow.wf and trigger the execution

# Conditional Branching

## Code example
Refer to the code in [condition.py](./condition.py) file.

## Local execution
`python parttwo/examples/condition.py`

## Sandbox execution
Visit http://localhost:30081/console/projects/flytesnacks/domains/development/workflows/parttwo.examples.condition.multiplier and trigger the execution

# FlyteFile, FlyteDirectory, and FlyteSchema

## Code examples

Refer to the code examples in [flytefile.py](./flytefile.py), [flytedirectory.py](./flytedirectory.py), and [flyteschema.py](./flyteschema.py) files.

## Local execution
1. FlyteFile: `python parttwo/examples/flytefile.py`
2. FlyteDirectory: `python parttwo/examples/flytedirectory.py`
3. FlyteSchema: `python parttwo/examples/flyteschema.py`

## Sandbox execution
1. Trigger the executions: http://localhost:30081/console/projects/flytesnacks/domains/development/workflows/parttwo.examples.flytefile.rotate_one_workflow, http://localhost:30081/console/projects/flytesnacks/domains/development/workflows/parttwo.examples.flytedirectory.download_and_rotate, and http://localhost:30081/console/projects/flytesnacks/domains/development/workflows/parttwo.examples.flyteschema.wf
2. Some of the tasks' inputs and outputs will have S3 URLs indicating the upload and download of data
