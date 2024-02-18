from datetime import datetime

from flytekit import task
from flytekit.configuration import Config, SerializationSettings, ImageConfig
from flytekit.remote import FlyteRemote


@task()
def t1(x: int) -> datetime:
    return datetime.now()


def test_cache_override():
    # TODO: flytekit remote should upload workflow code to s3
    remote = FlyteRemote(
        config=Config.auto(),
        default_project="flytesnacks",
        default_domain="development",
    )
    # TODO: serialization_settings should be optional
    # TODO: update flytekit remote documentation. https://docs.flyte.org/en/latest/api/flytekit/design/control_plane.html#registering-entities
    flyte_task = remote.register_task(
        entity=t1,
        serialization_settings=SerializationSettings(
            image_config=ImageConfig.auto_default_image()
        ),
        version="v2",
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
