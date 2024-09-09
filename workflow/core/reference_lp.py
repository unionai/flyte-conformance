import os
from flytekit import task, workflow, map_task, dynamic, image_spec, Resources, reference_launch_plan
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory
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

### Reference the LP and map over
@reference_launch_plan(
    project="flyte-conformance",
    domain="development",
    name="make_dc_wf",
    version="gaFatImOD50c9VedXk08kQ",
)
def make_dc_wf(input: int) -> MapInput:
    ...

@workflow
def map_ref_wf():
    make_dc_wf(input=5)
    map_task(make_dc_wf)(input=[i for i in range(10)])