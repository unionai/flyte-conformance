from flytekit import ImageSpec, task, dynamic, workflow
from utils import registry

repro_img = ImageSpec(
    packages=["mypy"],
    apt_packages=["git"],
    registry=registry,
)

image_foo = repro_img.with_apt_packages(["curl"])
image_d1 = repro_img.with_apt_packages(["wget"])
image_bar = repro_img.with_apt_packages(["vim"])


# hello
@task(container_image=image_foo)
def foo():
    print("foo")


@task(container_image=image_bar)
def bar():
    print("bar")


@dynamic(container_image=image_d1)
def d1():
    bar()


@workflow
def wf():
    foo()
    d1()
