import os
from flytekit import task, workflow, map_task, dynamic, image_spec, Resources, LaunchPlan
from flytekit.types.file import FlyteFile
from dataclasses import dataclass, fields
from mashumaro.mixins.json import DataClassJSONMixin
from typing import List

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

@task
def aggregate_dataclasses(ins: List[MapInput]) -> int:
    return len(ins)

@workflow
def make_dc_wf(input: int):
      make_dataclass(iter=input)

big_in_wf_lp = LaunchPlan.get_or_create(name="big_in_wf_lp", workflow=make_dc_wf)

@workflow
def big_map_wf():
    mapped = map_task(make_dataclass, concurrency=400)(list(range(6000)))
    aggregate_dataclasses(mapped)

# Simple big message wf
@task
def big_out() -> str:
    return "Hello World" * 1000 * 1024

@task
def big_in(inp: str) -> str:
    return inp

@workflow
def big_msg_wf() -> str:
    out = big_out()
    return big_in(inp=out)

# Big wf input
@task
def noop():
    ...

@workflow
def big_in_wf(input: str = "Hello Work" * 200 * 1024):
    noop()
