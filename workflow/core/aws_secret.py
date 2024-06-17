from flytekit import task, workflow
from flytekit import Secret
import flytekit

SECRET_GROUP = "arn:aws:secretsmanager:us-east-2:356633062068:secret:"
SECRET_KEY = "openai-PqfFLj"


@task(
    secret_requests=[
        Secret(
            group=SECRET_GROUP,
            key=SECRET_KEY,
        ),
    ],
)
def get_my_secret() -> str:
    secret_val = flytekit.current_context().secrets.get(SECRET_GROUP, SECRET_KEY)
    print(secret_val)
    return str(secret_val)


@workflow
def wf() -> str:
    return get_my_secret()
