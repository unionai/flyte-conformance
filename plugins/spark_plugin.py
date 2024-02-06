import random

from flytekitplugins.spark import Spark

import flytekit
from flytekit import ImageSpec, task, Resources, workflow
from operator import add

custom_image = ImageSpec(
    name="flyte-conformance",
    registry="ghcr.io/unionai",
    base_image="ghcr.io/flyteorg/flytekit:py3.10-1.10.2",
)


def f(_):
    x = random.random() * 2 - 1
    y = random.random() * 2 - 1
    return 1 if x**2 + y**2 <= 1 else 0


@task(
    task_config=Spark(
        spark_conf={
            "spark.driver.memory": "1000M",
            "spark.executor.memory": "1000M",
            "spark.executor.cores": "1",
            "spark.executor.instances": "2",
            "spark.driver.cores": "1",
        }
    ),
    limits=Resources(mem="2000M"),
    container_image=custom_image,
)
def hello_spark(partitions: int) -> float:
    print("Starting Spark with Partitions: {}".format(partitions))

    n = 1 * partitions
    sess = flytekit.current_context().spark_session
    count = sess.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)

    pi_val = 4.0 * count / n
    return pi_val


@workflow
def spark_wf(partitions: int = 10) -> float:
    return hello_spark(partitions=partitions)
