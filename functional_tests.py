from time import sleep
from flyteidl.core.execution_pb2 import TaskExecution
from dummy_tasks import t1, wf

from flytekit.configuration import Config, SerializationSettings, ImageConfig
from flytekit.remote import FlyteRemote
from flytekit.tools.script_mode import hash_file
from flytekit.tools.translator import Options

remote = FlyteRemote(
    config=Config.auto(),
    default_project="flyte-conformance",
    default_domain="development",
)

_, version, _ = hash_file("dummy_tasks.py")


def test_cache_override():
    # TODO: update flytekit remote documentation. https://docs.flyte.org/en/latest/api/flytekit/design/control_plane.html#registering-entities
    flyte_task = remote.register_task(
        entity=t1, version=version
    )

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
    flyte_task = remote.register_task(
        entity=t1, version=version
    )
    exe = remote.execute(entity=flyte_task, inputs={"x": 2}, wait=True)
    exe = remote.sync_execution(exe, sync_nodes=True)
    old = exe.outputs["o0"]

    exe = remote.execute(entity=flyte_task, inputs={"x": 2}, wait=True)
    exe = remote.sync_execution(exe, sync_nodes=True)
    new = exe.outputs["o0"]
    assert old == new


def test_max_parallelism():
    flyte_workflow = remote.register_workflow(
        entity=wf, version=version
    )
    exe = remote.execute(
        entity=flyte_workflow, inputs={}, wait=False, options=Options(max_parallelism=3)
    )
    sleep(10)  # wait for tasks to start
    exe = remote.sync_execution(exe, sync_nodes=True)
    num_running_tasks = sum(
        1
        for node_id, exe in exe.node_executions.items()
        if exe.task_executions
        and exe.task_executions[0].closure.phase == TaskExecution.RUNNING
    )
    assert num_running_tasks == 3


if __name__ == "__main__":
    test_cache_override()
    test_cache_output()
    test_max_parallelism()
