import os
from datetime import datetime
from time import sleep

from click.testing import CliRunner

from flytekit import ImageSpec, task, workflow
from flytekit.clis.sdk_in_container import pyflyte

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


@task(container_image=image_spec)
def t3() -> str:
    return os.getenv("HELLO")


@workflow
def wf(second: int = 60):
    """
    Dummy workflow for functional tesffgggggttdfffffff.
    """
    for i in range(5):
        t2(second=second)


if __name__ == "__main__":
    runner = CliRunner()
    result = runner.invoke(
        pyflyte.main, ["-vv", "run", "--remote", "dummy_tasks.py", "wf"]
    )
    print(result.output)
