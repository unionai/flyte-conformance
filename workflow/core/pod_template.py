import os
import time

from flytekit import Resources, task, workflow, ImageSpec
from flytekitplugins.pod import Pod
from kubernetes.client.models import (
    V1Container,
    V1EmptyDirVolumeSource,
    V1PodSpec,
    V1ResourceRequirements,
    V1Volume,
    V1VolumeMount,
)
from workflow.utils import registry

_SHARED_DATA_PATH = "/data/message.txt"
image_spec = ImageSpec(
    packages=["flytekitplugins-pod"],
    name="flyte-conformance",
    registry=registry,
)


@task(
    task_config=Pod(
        pod_spec=V1PodSpec(
            containers=[V1Container(name="primary", image=image_spec)],
        ),
    ),
    requests=Resources(
        mem="500Mi",
    ),
    container_image=image_spec,
)
def pod_task() -> str:
    return "Hello from pod task!"


@task(
    task_config=Pod(
        pod_spec=V1PodSpec(
            containers=[
                V1Container(
                    name="primary",
                    resources=V1ResourceRequirements(
                        requests={"cpu": "1", "memory": "100Mi"},
                        limits={"cpu": "1", "memory": "100Mi"},
                    ),
                    volume_mounts=[
                        V1VolumeMount(
                            name="shared-data",
                            mount_path="/data",
                        )
                    ],
                ),
                V1Container(
                    name="secondary",
                    image="alpine",
                    command=["/bin/sh"],
                    args=[
                        "-c",
                        "echo hi pod world > {}".format(_SHARED_DATA_PATH),
                    ],
                    resources=V1ResourceRequirements(
                        requests={"cpu": "1", "memory": "100Mi"},
                        limits={"cpu": "1", "memory": "100Mi"},
                    ),
                    volume_mounts=[
                        V1VolumeMount(
                            name="shared-data",
                            mount_path="/data",
                        )
                    ],
                ),
            ],
            volumes=[
                V1Volume(
                    name="shared-data",
                    empty_dir=V1EmptyDirVolumeSource(medium="Memory"),
                )
            ],
        ),
    ),
    requests=Resources(
        mem="1G",
    ),
    container_image=image_spec,
)
def multiple_containers_pod_task() -> str:
    while not os.path.isfile(_SHARED_DATA_PATH):
        time.sleep(5)

    with open(_SHARED_DATA_PATH, "r") as shared_message_file:
        return shared_message_file.read()


@workflow
def pod_template_workflow():
    # multiple_containers_pod_task()
    pod_task()
