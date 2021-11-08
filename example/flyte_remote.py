from flytekit.remote import FlyteRemote, workflow_execution

remote = FlyteRemote.from_config(
    "flytesnacks",
    "development",
)

flyte_workflow = remote.fetch_workflow(
    name="house_price_prediction.house_price_predictor.house_price_predictor_trainer",
    version="v1",
)

workflow_execution = remote.execute(flyte_workflow, inputs={}, wait=True)
print(workflow_execution.outputs)
