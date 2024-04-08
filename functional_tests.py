from datetime import datetime

from flytekit import task, ImageSpec
from flytekit.configuration import Config
from flytekit.remote import FlyteRemote
from flytekit.tools.script_mode import hash_file

image_spec = ImageSpec(
    name="flyte-conformance",
    registry="ghcr.io/unionai",
    packages=["pandas"],
)


@task(container_image=image_spec)
def t1(x: int) -> datetime:
    return datetime.now()


def test_cache_override():
    # TODO: flytekit remote should upload workflow code to s3
    # TODO: update flytekit remote documentation. https://docs.flyte.org/en/latest/api/flytekit/design/control_plane.html#registering-entities
    remote = FlyteRemote(
        config=Config.auto(),
        default_project="flytesnacks",
        default_domain="development",
    )
    _, digest, _ = hash_file(__file__)
    flyte_task = remote.register_task(
        entity=t1,
        version=digest,
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


if __name__ == "__main__":
    test_cache_override()
