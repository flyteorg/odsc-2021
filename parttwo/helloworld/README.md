### Code Example

Refer to the code in [hello_world.py](./hello_world.py) file.

### Test locally
1. `git clone https://github.com/flyteorg/odsc-2021.git`
2. `cd odsc-2021/`
3. Activate virtual environment
    * `python -m venv odsc`
    * `source venv/bin/activate`
4. `pip install flytekit --upgrade`
5. `python parttwo/helloworld/hello_world.py`

### Create a sandbox
1. `brew install flyteorg/homebrew-tap/flytectl`
2. `flytectl upgrade`
3. `flytectl version`
4. `flytectl sandbox start --source $(pwd)`
5. `flytectl config init`

### Build Docker container

`flytectl sandbox exec -- docker build . --tag "myapp:v1" -f parttwo/Dockerfile`

### Package the code

`pyflyte --pkgs parttwo.helloworld package --image myapp:v1 --force`

### Register the example

`flytectl register files --project flytesnacks --domain development --archive flyte-package.tgz --version v1`

### FlyteCTL/UI execution

Visit `localhost:30081/console` to trigger the workflow.

Alternatively, you can execute using the command line through FlyteCTL.

1. Generate an execution spec file.

    `flytectl get launchplan --project flytesnacks --domain development parttwo.helloworld.hello_world.my_wf --latest --execFile exec_spec.yaml`

2. Create an execution using the exec spec file.

    `flytectl create execution --project flytesnacks --domain development --execFile exec_spec.yaml`

3. Monitor the execution by providing the execution name from the create execution command.

    `flytectl get execution --project flytesnacks --domain development <execname>`

## Fast Registration

## Code modifications
1. Open hello_world.py: `parttwo/helloworld/hello_world.py`
2. Add `name: str` as an argument to both `my_wf` and `say_hello` functions. Then update the body of `say_hello` to consume that argument.
    ```
    @task
    def say_hello(name: str) -> str:
        return f"hello world, {name}"
    ```

    ```
    @workflow
    def my_wf(name: str) -> str:
        res = say_hello(name=name)
        return res
    ```
3. Update the simple test at the bottom of the file to pass in a name, e.g.,
    ```
    print(f"Running my_wf(name='adam') {my_wf(name='adam')}")
    ```
4. Test locally by running `python parttwo/helloworld/hello_world.py`.

## Fast serialize

`pyflyte --pkgs parttwo.helloworld package --image myapp:v1 --fast --force`

## Fast register

`flytectl register files --project flytesnacks --domain development --archive flyte-package.tgz  --version v1-fast1`

## FlyteCTL/UI execution

Visit `localhost:30081/console` to trigger the workflow.

Alternatively, you can execute using the command line through FlyteCTL.

1. Generate an execution spec file.

    `flytectl get launchplan --project flytesnacks --domain development parttwo.helloworld.hello_world.my_wf --latest --execFile exec_spec.yaml`

2. Modify the execution spec file and update the input params and save the file. Notice that the version would be changed to your latest one.

    ```
        ....
    inputs:
    name: "adam"
    ....
    version: v1-fast1
    ```

3. Create an execution using the exec spec file.

    `flytectl create execution --project flytesnacks --domain development --execFile exec_spec.yaml`

4. Monitor the execution by providing the execution name from the create execution command.

    `flytectl get execution --project flytesnacks --domain development <execname>`