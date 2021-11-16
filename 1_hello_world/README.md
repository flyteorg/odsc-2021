# Hello World Example

Based on [getting started docs](https://docs.flyte.org/en/latest/getting_started.html).

## Cheat sheet
#. Run Locally:

   ```bash
   python 1_hello_world/step1.py
   ```

#. Start sandbox:
   
   ```bash
   flytectl sandbox start --source=./
   ```
   
#. Build docker image:
   
   ```bash
   flytectl sandbox exec -- docker build -t hello_world:1 -f 1_hello_world.Dockerfile .
   ```

#. Serialize Tasks and workflows:

   ```bash
   pyflyte --pkgs 1_hello_world package --image hello_world:1
   ```

#. Register Tasks and workflows:

   ```bash
   flytectl register files flyte-package.tgz -p flytesnacks -d development --archive --version v2
   ```
