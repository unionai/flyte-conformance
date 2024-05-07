from time import sleep
from flyteidl.core.execution_pb2 import TaskExecution

from flytekit.configuration import Config
from flytekit.remote import FlyteRemote
from flytekit.tools.translator import Options

remote = FlyteRemote(
    config=Config.auto(),
    default_project="flyte-conformance",
    default_domain="development",
)

version = "v1"


def test_cache_override():
    print("test cache override")
    # TODO: update flytekit remote documentation. https://docs.flyte.org/en/latest/api/flytekit/design/control_plane.html#registering-entities
    flyte_task = remote.fetch_task(name="dummy_tasks.t1", version=version)

    exe = remote.execute(entity=flyte_task, inputs={"x": 3}, wait=True)
    exe = remote.sync_execution(exe, sync_nodes=True)
    old = exe.outputs["o0"]

    exe = remote.execute(
        entity=flyte_task, inputs={"x": 3}, overwrite_cache=True, wait=True
    )
    exe = remote.sync_execution(exe, sync_nodes=True)
    new = exe.outputs["o0"]

    assert old != new


def test_cache_output():
    print("test cache output")
    flyte_task = remote.fetch_task(name="dummy_tasks.t1", version=version)
    exe = remote.execute(entity=flyte_task, inputs={"x": 2}, wait=True)
    exe = remote.sync_execution(exe, sync_nodes=True)
    old = exe.outputs["o0"]

    exe = remote.execute(entity=flyte_task, inputs={"x": 2}, wait=True)
    exe = remote.sync_execution(exe, sync_nodes=True)
    new = exe.outputs["o0"]
    assert old == new


def test_default_env():
    print("test default env")
    flyte_task = remote.fetch_task(name="dummy_tasks.t3", version=version)
    exe = remote.execute(
        entity=flyte_task, inputs={}, envs={"HELLO": "WORLD"}, wait=True
    )
    exe = remote.sync_execution(exe, sync_nodes=True)
    assert exe.outputs["o0"] == "WORLD"


def test_max_parallelism():
    print("test max parallelism")
    flyte_workflow = remote.fetch_workflow(name="dummy_tasks.wf", version=version)
    exe = remote.execute(
        entity=flyte_workflow, inputs={}, wait=False, options=Options(max_parallelism=1)
    )
    sleep(40)  # wait for tasks to start
    exe = remote.sync_execution(exe, sync_nodes=True)
    num_running_tasks = sum(
        1
        for node_id, exe in exe.node_executions.items()
        if exe.task_executions
        and exe.task_executions[0].closure.phase == TaskExecution.RUNNING
    )
    assert num_running_tasks == 1


if __name__ == "__main__":
    test_cache_override()
    test_cache_output()
    test_default_env()
    test_max_parallelism()
