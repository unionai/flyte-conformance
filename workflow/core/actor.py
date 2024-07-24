from flytekit import workflow, ImageSpec
from union.actor import ActorEnvironment


image_spec = ImageSpec(
    name="actor",
    registry="pingsutw",
    packages=["panda", "union>=0.1.52", "flytekit>=1.13.1a2"],
    apt_packages=["git"],
)


actor = ActorEnvironment(
    name="flyte-conformance",
    replica_count=2,
    parallelism=2,
    backlog_length=50,
    ttl_seconds=300,
    container_image=image_spec,
)


@actor.task
def plus_one(input: int) -> int:
    return input + 1


@actor.dynamic
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
