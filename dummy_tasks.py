from datetime import datetime
from time import sleep

from flytekit import ImageSpec, task, workflow

image_spec = ImageSpec(
    name="flyte-conformance",
    registry="ghcr.io/unionai",
    packages=["pandas"],
)


@task(container_image=image_spec, cache=True, cache_version="1.0")
def t1(x: int) -> datetime:
    print(x)
    return datetime.now()


@task(container_image=image_spec)
def t2(second: int):
    sleep(second)


@workflow
def wf(second: int = 60):
    for i in range(10):
        t2(second=second)
