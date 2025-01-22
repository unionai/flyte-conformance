from union import ActorEnvironment

from flytekit import FlyteRemote

from flytekit import Config, workflow, ImageSpec, Secret, current_context
from flytekit.configuration import PlatformConfig, AuthType

image_spec = ImageSpec(registry="pingsutw", packages=["union"])

actor = ActorEnvironment(
    name="flyte-conformance",
    replica_count=10,
    ttl_seconds=300,
    container_image=image_spec,
    secret_requests=[Secret(key="load-test-aws-secret", mount_requirement=Secret.MountType.FILE)]
)


@actor.task
def launch_load_tests(num_wf: int, workflow_name: str, version: str):
    secret_file = current_context().secrets.get_secrets_file("load-test-aws-secret")
    with open(secret_file, "r") as f:
        secret_value = f.read()
    config = Config(platform=PlatformConfig(
        endpoint="load-test-aws.cloud-staging.union.ai",
        auth_mode=AuthType.CLIENTSECRET,
        insecure=False,
        client_id="kevin123",
        client_credentials_secret=secret_value
    ))
    for i in range(num_wf):
        remote = FlyteRemote(config=config, default_domain="development", default_project="kevin")
        wf = remote.fetch_workflow(name=workflow_name, version=version)
        remote.execute_remote_wf(entity=wf, inputs={})


@workflow()
def load_tests_wf(num_wf: int = 100, workflow_name: str = "load_tests.agent.text_wf", version: str = "JLbJclMQ_yikhwZVzKri3g"):
    """
    :param num_wf: Number of 10x workflows to launch
    :param workflow_name: Name of the workflow to launch
    :param version: Version of the workflow to launch
    """
    for i in range(10):
        launch_load_tests(num_wf=num_wf, workflow_name=workflow_name, version=version)
