from flytekit import task, workflow
from flytekit import Secret
import flytekit

SECRET_GROUP = "openai"
GROUP_VERSION = "1"


@task(
    secret_requests=[
        Secret(
            group=SECRET_GROUP,
            group_version=GROUP_VERSION,
        ),
    ],
)
def get_my_secret() -> str:
    secret_val = flytekit.current_context().secrets.get(
        group=SECRET_GROUP, group_version=GROUP_VERSION
    )
    print(secret_val)
    return str(secret_val)


@workflow
def gcp_secret_wf() -> str:
    return get_my_secret()
