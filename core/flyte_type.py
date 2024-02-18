import os
from dataclasses import dataclass
from enum import Enum
from typing import Annotated, Any, Dict, NamedTuple

import pandas as pd
from mashumaro.mixins.json import DataClassJSONMixin

from flytekit import (
    task,
    workflow,
    FlyteContext,
    BatchSize,
    Resources,
    ImageSpec,
    StructuredDataset,
    kwtypes,
)
from flytekit.types.directory import FlyteDirectory

image_spec = ImageSpec(
    name="flyte-conformance",
    registry="ghcr.io/unionai",
    packages=["pandas"],
)

col = kwtypes(Age=int)


@dataclass
class Datum(DataClassJSONMixin):
    x: int
    y: str
    z: Dict[int, str]


class Coffee(Enum):
    ESPRESSO = "espresso"
    AMERICANO = "americano"
    LATTE = "latte"
    CAPPUCCINO = "cappucccino"


slope_value = NamedTuple("slope_value", [("slope", float)])


class Pickle:
    def __init__(self, size: int):
        self.size = size

    def __str__(self):
        return f"pickle's size is {self.size}"


@task(requests=Resources(mem="1500Mi"), container_image=image_spec)
def create_flyte_directory(
    num_files: int, filesize_mb: int
) -> Annotated[FlyteDirectory, BatchSize(100)]:
    directory = "/tmp/test"
    os.mkdir(directory)
    for i in range(num_files):
        file_path = os.path.join(directory, f"file_{i}.txt")
        with open(file_path, "w") as f:
            f.write(str(os.urandom(filesize_mb * 1024 * 1024)))

    remote_dir = (
        FlyteContext.current_context().file_access.get_random_remote_directory()
    )

    return FlyteDirectory(path=directory, remote_directory=remote_dir)


@task(requests=Resources(mem="1500Mi"), container_image=image_spec)
def download_flyte_directory(directory: Annotated[FlyteDirectory, BatchSize(100)]):
    entity = FlyteDirectory.listdir(directory)
    for e in entity:
        print("s3 object:", e.remote_source)

    f = open(entity[0], "r")
    print(f.read())

    directory.__fspath__()  # download all the files in the directory


@task(container_image=image_spec)
def test_pickle(pickle: Any) -> Any:
    print(pickle)
    return pickle


@task(container_image=image_spec)
def generate_pandas_df() -> pd.DataFrame:
    return pd.DataFrame(
        {"Name": ["Tom", "Joseph"], "Age": [21, 22], "Height": [160, 178]}
    )


@task(container_image=image_spec)
def get_subset_pandas_df(df: StructuredDataset) -> Annotated[StructuredDataset, col]:
    df = df.open(pd.DataFrame).all()
    df = pd.concat([df, pd.DataFrame([[30]], columns=["Age"])])
    return StructuredDataset(dataframe=df)


@task(container_image=image_spec)
def test_dataclass(d: Datum) -> Datum:
    print("dataclass:", d)
    return d


@task(container_image=image_spec)
def test_enum(coffee: Coffee) -> Coffee:
    print("coffee", coffee)
    return coffee


@task(container_image=image_spec)
def slope(x: list[int], y: list[int]) -> slope_value:
    sum_xy = sum([x[i] * y[i] for i in range(len(x))])
    sum_x_squared = sum([x[i] ** 2 for i in range(len(x))])
    n = len(x)
    return (n * sum_xy - sum(x) * sum(y)) / (n * sum_x_squared - sum(x) ** 2)


@workflow
def test_flyte_type_wf():
    flyte_dir = create_flyte_directory(num_files=10, filesize_mb=8)
    download_flyte_directory(directory=flyte_dir)

    # test_pickle(pickle=Pickle(size=15))  # TODO: Failed to Bind variable pickle for function core.flyte_type.test_pickle.

    df = generate_pandas_df()
    get_subset_pandas_df(df=df)

    test_dataclass(d=Datum(x=1, y="hello", z={1: "world"}))
    test_enum(coffee=Coffee.LATTE)
    slope(x=[-3, 0, 3], y=[7, 4, -2])
