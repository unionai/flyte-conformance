from time import sleep

from flytekit import WorkflowFailurePolicy, task, workflow


@task
def create_cluster(name: str):
    print(f"Creating cluster: {name}")


@task
def t1(a: int, b: str):
    print(f"{a} {b}")
    raise ValueError("Fail!")


@task
def delete_cluster(name: str):
    print(f"Deleting cluster {name}")


@task
def clean_up(name: str):
    sleep(3)
    print(f"Cleaning up cluster {name}")


@workflow
def clean_up_wf(name: str):
    return clean_up(name=name)


@task
def fail_clean_up(name: str):
    sleep(1)
    raise ValueError("Fail!")


@workflow(on_failure=clean_up)
def subwf1(name: str):
    c = create_cluster(name=name)
    t = t1(a=1, b="2")
    d = delete_cluster(name=name)
    c >> t >> d


@workflow(on_failure=clean_up_wf)
def subwf2(name: str):
    c = create_cluster(name=name)
    t = t1(a=1, b="2")
    d = delete_cluster(name=name)
    c >> t >> d


@workflow(on_failure=clean_up)
def subwf3(name: str = "my_cluster"):
    c = create_cluster(name=name)
    subwf1(name="another_cluster")
    t = t1(a=1, b="2")
    d = delete_cluster(name=name)
    c >> t >> d


@workflow(on_failure=subwf3)
def subwf4(name: str = "my_cluster"):
    c = create_cluster(name=name)
    subwf1(name="another_cluster")
    t = t1(a=1, b="2")
    d = delete_cluster(name=name)
    c >> t >> d


@workflow(on_failure=fail_clean_up)
def subwf5(name: str):
    c = create_cluster(name=name)
    t = t1(a=1, b="2")
    d = delete_cluster(name=name)
    c >> t >> d


@workflow(
    on_failure=clean_up,
    failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE,
)
def flyte_failure_node_wf(name: str = "my_cluster"):
    c = create_cluster(name=name)
    subwf1(name="another_cluster")  # -> a failure task node
    subwf2(name="another_cluster")  # -> a failure workflow node
    subwf3(
        name="another_cluster"
    )  # -> a failure task node and a failure task node inside the subsubworkflow
    subwf4(
        name="another_cluster"
    )  # -> a failure workflow node (subwf3). a failure node inside a failure node
    subwf5(
        name="another_cluster"
    )  # -> a failure task node and this failure node will fail
    t = t1(a=1, b="2")
    d = delete_cluster(name=name)
    c >> t >> d
