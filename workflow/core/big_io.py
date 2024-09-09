from flytekit import task, workflow, map_task, LaunchPlan
from flytekit.types.file import FlyteFile
from dataclasses import dataclass
from mashumaro.mixins.json import DataClassJSONMixin
from typing import List


## Make dataclass wf
@dataclass
class MapInput(DataClassJSONMixin):
    f1: FlyteFile | None = None
    f2: FlyteFile | None = None
    f3: FlyteFile | None = None
    f4: FlyteFile | None = None
    f5: FlyteFile | None = None


@task
def make_dataclass(iter: int) -> MapInput:
    parts = [
        "f1",
        "f2",
        "f3",
        "f4",
        "f5",
    ]
    m = MapInput()
    for p in parts:
        fp = f"{p}.txt"
        with open(fp, "w") as f:
            f.write(str(iter))
        setattr(m, p, FlyteFile(fp))
    return m


@workflow
def make_dc_wf(input: int) -> MapInput:
    return make_dataclass(iter=input)


make_dc_wf = LaunchPlan.get_or_create(name="make_dc_wf", workflow=make_dc_wf)


@workflow
def big_map_wf():
    map_task(make_dataclass, concurrency=50)(list(range(20000)))


## Simple big message wf
@task
def big_out() -> str:
    return "Hello World" * 1000 * 1024


@workflow
def big_msg_wf():
    big_out()


## Big wf input
@task
def noop():
    ...


@workflow
def big_in_wf(input: str = "Hello World" * 185 * 1024):
    noop()


## Big list of files wf
@task
def make_flytefiles(iters: int) -> List[FlyteFile]:
    files = []
    for i in range(iters):
        fp = f"file_{i}.txt"
        with open(fp, "w") as f:
            f.write(str(i))
        files.append(FlyteFile(fp))
        print(f"Created file {fp}")
    return files


@workflow
def big_ff_wf(iters: int = 100000):
    make_flytefiles(iters=iters)


## Big inputs and outputs
@task
def generate_strs(count: int) -> List[str]:
    return ["a"] * count


@task
def my_1mb_task(i: str) -> str:
    return f"Hello world {i}" * 100 * 1024


@workflow
def my_wf(mbs: int) -> List[str]:
    strs = generate_strs(count=mbs)
    return map_task(my_1mb_task)(i=strs)


@workflow
def big_inputs_wf(input: List[str]):
    noop()


@task
def noop():  # noqa: F811
    ...


big_inputs_wf_lp = LaunchPlan.get_or_create(
    name="big_inputs_wf_lp", workflow=big_inputs_wf
)


@workflow
def ref_wf(mbs: int):
    big_inputs_wf_lp(input=my_wf(mbs))
