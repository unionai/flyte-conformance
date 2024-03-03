import typing
import ray
from flytekitplugins.ray import RayJobConfig, HeadNodeConfig, WorkerNodeConfig

from flytekit import ImageSpec, Resources, task, workflow

ray_image = ImageSpec(
    name="flyte-conformance",
    registry="ghcr.io/unionai",
    packages=["flytekitplugins-ray"],
)


@ray.remote
def f(x):
    return x * x


ray_config = RayJobConfig(
    head_node_config=HeadNodeConfig(ray_start_params={"log-color": "True"}),
    worker_node_config=[WorkerNodeConfig(group_name="ray-group", replicas=1)],
    runtime_env={"pip": ["numpy", "pandas"]},
)


@task(
    task_config=ray_config,
    requests=Resources(mem="2Gi", cpu="2"),
    container_image=ray_image,
)
def ray_task(n: int) -> typing.List[int]:
    futures = [f.remote(i) for i in range(n)]
    return ray.get(futures)


@workflow
def ray_wf(n: int = 3) -> typing.List[int]:
    return ray_task(n=n)
