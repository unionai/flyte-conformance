import threading
from union import ActorEnvironment

from flytekit import FlyteRemote, Resources

from flytekit import Config, workflow, ImageSpec, Secret, current_context
from flytekit.configuration import PlatformConfig, AuthType

image_spec = ImageSpec(registry="pingsutw", packages=["union"])

actor = ActorEnvironment(
    name="load-test",
    replica_count=100,
    ttl_seconds=300,
    container_image=image_spec,
    secret_requests=[
        Secret(key="load-test-aws-secret", mount_requirement=Secret.MountType.FILE)
    ],
    requests=Resources(cpu="2", mem="2000Mi")
)


@actor.task()
def launch_load_tests(num_wf: int, workflow_name: str, version: str):
    secret_file = current_context().secrets.get_secrets_file("load-test-aws-secret")
    with open(secret_file, "r") as f:
        secret_value = f.read()
    config = Config(
        platform=PlatformConfig(
            endpoint="load-test-aws.cloud-staging.union.ai",
            auth_mode=AuthType.CLIENTSECRET,
            insecure=False,
            client_id="kevin123",
            client_credentials_secret=secret_value,
        )
    )
    remote = FlyteRemote(config=config, default_domain="development", default_project="kevin")
    wf = remote.fetch_workflow(name=workflow_name, version=version)

    def execute_remote_wf():
        for i in range(num_wf):
            remote.execute(wf, {})

    threads = [threading.Thread(target=execute_remote_wf) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


@workflow()
def load_tests_wf(
    num_wf: int = 10,
    workflow_name: str = "load_tests.agent.text_wf",
    version: str = "ou87icnLvRG9StCK6yJGsA",
):
    """
    :param num_wf: Number of 1000x workflows to launch
    :param workflow_name: Name of the workflow to launch
    :param version: Version of the workflow to launch
    """
    for i in range(100):
        launch_load_tests(
            num_wf=num_wf,
            workflow_name=workflow_name,
            version=version,
        )
