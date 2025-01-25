from flytekit import workflow, ImageSpec, dynamic
from union.actor import ActorEnvironment
from workflow.utils import registry

image_spec = ImageSpec(
    name="flyte-conformance",
    registry=registry,
    packages=["panda", "union", "flytekit"],
    apt_packages=["git"],
)


actor = ActorEnvironment(
    name="flyte-conformance",
    replica_count=2,
    ttl_seconds=300,
    container_image=image_spec,
)


@actor.task
def plus_one(input: int) -> int:
    return input + 1


@dynamic(container_image=image_spec)
def d1():
    plus_one(input=1)
    plus_one(input=1)


@workflow
def actor_wf(input: int = 0) -> int:
    """
    actor workflow.

    This is a simple workflow that demonstrates the use of the Actor in Flyte.
    - regular task in the actor
    - dynamic task in the actor
    """

    d1()
    a = plus_one(input=input)
    b = plus_one(input=a)
    c = plus_one(input=b)
    return plus_one(input=c)
