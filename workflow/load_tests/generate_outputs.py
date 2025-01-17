import typing

from flytekit import task


@task(cache_version="1.0", cache=True)
def generate_list(num: int) -> typing.List[int]:
    return list(range(num))
