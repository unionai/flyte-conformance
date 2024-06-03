from flytekit import task, workflow, ImageSpec, dynamic

image_sklearn = ImageSpec(packages=["scikit-learn"], apt_packages=["git"], registry="pingsutw")
image_tensorflow = ImageSpec(base_image=image_sklearn, packages=["tensorflow"], registry="pingsutw")


@task(container_image=image_sklearn)
def t1(a: int) -> int:
    return a + 2


@task(container_image=image_sklearn)
def t2(a: int) -> int:
    return a + 2


@workflow
def wf(a: int = 3):
    t1(a=a)
    t2(a=a)


if __name__ == "__main__":
    print(f"Running my_wf: {wf(a=50)}")
