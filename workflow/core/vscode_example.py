from flytekit import task, workflow, ImageSpec
from flytekitplugins.flyteinteractive import vscode
from utils import registry

image_spec = ImageSpec(
    registry=registry,
    name="flyte-conformance",
    packages=["flytekitplugins-flyteinteractive"],
)


@task(container_image=image_spec)
@vscode
def train():
    print("forward")
    print("backward")


@workflow
def wf():
    train()


if __name__ == "__main__":
    wf()
