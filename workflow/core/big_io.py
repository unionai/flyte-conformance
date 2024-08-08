import os
from flytekit import task, workflow, map_task, dynamic, image_spec, Resources, LaunchPlan
from flytekit.types.file import FlyteFile
from dataclasses import dataclass, fields
from mashumaro.mixins.json import DataClassJSONMixin
from typing import List

## Big mapped dataclass wf
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
        fp = f'{p}.txt'
        with open(fp, 'w') as f:
            f.write(str(iter))
        setattr(m, p, FlyteFile(fp))
    return m

@workflow
def make_dc_wf(input: int) -> MapInput:
    return make_dataclass(iter=input)

make_dc_wf = LaunchPlan.get_or_create(name="make_dc_wf", workflow=make_dc_wf)

@task
def aggregate_dataclasses(ins: List[MapInput]) -> int:
    return len(ins)

@workflow
def big_map_wf():
    mapped = map_task(make_dataclass, concurrency=400)(list(range(6000)))
    aggregate_dataclasses(mapped)

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
def big_in_wf(input: str = "Hello Work" * 200 * 1024):
    noop()

## Big list of files wf
@task
def make_flytefiles(iters: int) -> List[FlyteFile]:
    files = []
    for i in range(iters):
        fp = f'file_{i}.txt'
        with open(fp, 'w') as f:
            f.write(str(i))
        files.append(FlyteFile(fp))
        print(f'Created file {fp}')
    return files

@workflow
def big_ff_wf(iters: int=100000):
    make_flytefiles(iters=iters)