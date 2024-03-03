import typing

from flytekit import task, workflow, WorkflowFailurePolicy
from flytekit.types.error.error import FlyteError


@task
def create_cluster(name: str):
    print(f"Creating cluster: {name}")


@task()
def t1(name: str):
    print(f"{name}")
    raise ValueError("Fail!")


@task()
def delete_cluster(name: str, err: typing.Optional[FlyteError] = None):
    print(f"Deleting cluster {name}")
    print(err)


@task()
def clean_up(name: str, err: typing.Optional[FlyteError] = None):
    print(f"Deleting cluster {name} due to {err}")
    print(err)


@workflow(
    on_failure=clean_up,
    failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE,
)
def subwf(name: str = "Flyte"):
    c = create_cluster(name=name)
    t = t1(name="2")
    d = delete_cluster(name=name)
    c >> t >> d


@workflow(
    on_failure=clean_up,
    failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE,
)
def wf1(name: str = "Flyte"):
    c = create_cluster(name=name)
    subwf(name="Flyte")
    t = t1(name="2")
    d = delete_cluster(name=name)
    c >> t >> d


@workflow(
    on_failure=clean_up,
    failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE,
)
def wf2(name: str = "Flyte"):
    c = create_cluster(name=name)
    t = t1(name="2")
    d = delete_cluster(name=name)
    c >> t >> d


@workflow
def clean_up_wf(name: str = "Flyte"):
    return create_cluster(name=name)


@workflow(
    on_failure=clean_up_wf,
    failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE,
)
def wf3(name: str = "Flyte"):
    c = create_cluster(name=name)
    t = t1(name="2")
    d = delete_cluster(name=name)
    c >> t >> d


@workflow
def test_failure_node():
    wf1()
    wf2()
    wf3()
