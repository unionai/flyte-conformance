from flytekit import task, workflow, ImageSpec

image_sklearn = ImageSpec(
    packages=["scikit-learn"],
    apt_packages=["git"],
    registry="ghcr.io/unionai",
    name="flyte-conformance",
)
image_tensorflow = ImageSpec(
    base_image=image_sklearn,
    packages=["tensorflow"],
    registry="ghcr.io/unionai",
    name="flyte-conformance",
)


@task(container_image=image_sklearn)
def t1(a: int) -> int:
    return a + 2


@task(container_image=image_tensorflow)
def t2(a: int) -> int:
    return a + 2


@workflow
def composition_image_wf(a: int = 3):
    """
    helloooofffff
    """
    t1(a=a)
    t2(a=a)


if __name__ == "__main__":
    print(f"Running my_wf: {composition_image_wf(a=50)}")
