from typing import List
from flytekit import task, workflow, map_task
from flytekit.experimental import map_task as array_node_map_task


@task(cache=True, cache_version="1.0")
def a_mappable_task(a: List[str]) -> str:
    return ",".join(a)


@task
def get_input() -> List[List[str]]:
    my_input = []
    for ix in range(0, 40):
        tmp_list = []
        for iy in range(0, 100):
            tmp_list.append(f"{ix}.{iy}")
        my_input.append(tmp_list)
    return my_input


@task
def is_equal(x: List[str], y: List[str]) -> bool:
    x.sort()
    y.sort()
    return x == y


@workflow
def map_task_wf() -> bool:
    my_input = get_input()
    mapped_out1 = map_task(a_mappable_task)(a=my_input)
    mapped_out2 = array_node_map_task(a_mappable_task)(a=my_input)
    return is_equal(x=mapped_out1, y=mapped_out2)
