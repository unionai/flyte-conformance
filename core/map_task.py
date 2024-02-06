from typing import List
from flytekit import task, workflow, map_task


@task(cache=True, cache_version="1.0")
def a_mappable_task(a: List[str]) -> str:
    return ",".join(a)


@task
def get_input() -> List[List[str]]:
    myinput = []
    for ix in range(0, 40):
        tmp_list = []
        for iy in range(0, 100):
            tmp_list.append(f"{ix}.{iy}")
        myinput.append(tmp_list)
    return myinput


@workflow
def map_task_wf() -> List[str]:
    my_input = get_input()
    mapped_out = map_task(a_mappable_task)(a=my_input)
    return mapped_out
