import os
from flytekit import task, workflow, map_task, dynamic, image_spec, Resources, reference_launch_plan
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from dataclasses import dataclass, fields
from mashumaro.mixins.json import DataClassJSONMixin
from typing import List

### Reference the LP and map over

@task
def hello_iter(iter: int) -> str:
    return f"Hello {int}"# * 80 * 1024

@reference_launch_plan(
    project="flytesnacks",
    domain="development",
    name="big_fan_wf_lp",
    version="ESqLPNauicjwcXJFHi2l6w",
)
def big_fan_wf_lp(input: str):
    ...

@workflow
def map_ref_wf():
    ins = map_task(hello_iter)([i for i in range(5000)])
    map_task(big_fan_wf_lp)(input=ins)