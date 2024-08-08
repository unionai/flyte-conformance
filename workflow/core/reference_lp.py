import os
from flytekit import task, workflow, map_task, dynamic, image_spec, Resources, reference_launch_plan
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
from dataclasses import dataclass, fields
from mashumaro.mixins.json import DataClassJSONMixin
from typing import List

### Reference the LP and map over
@reference_launch_plan(
    project="flyte-conformance",
    domain="development",
    name="make_dc_wf",
    version="-qcX4nn0sxP5_jinA7fPbw",
)
def make_dc_wf(input: int):
    ...

@workflow
def map_ref_wf():
    map_task(make_dc_wf)(input=[i for i in range(10)])