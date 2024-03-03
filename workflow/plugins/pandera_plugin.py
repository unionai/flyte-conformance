import typing

import flytekitplugins.pandera  # noqa : F401
import pandas as pd
import pandera as pa
from flytekit import task, workflow, ImageSpec
from pandera.typing import DataFrame, Series

image_spec = ImageSpec(
    name="flyte-conformance",
    packages=["flytekitplugins-pandera", "pandas"],
    registry="ghcr.io/unionai",
)


def total_pay(df):
    return df.assign(total_pay=df.hourly_pay * df.hours_worked)


def add_id(df, worker_id):
    return df.assign(worker_id=worker_id)


def process_data(df, worker_id):
    return add_id(df=total_pay(df=df), worker_id=worker_id)


class InSchema(pa.DataFrameModel):
    hourly_pay: Series[float] = pa.Field(ge=7)
    hours_worked: Series[float] = pa.Field(ge=10)

    @pa.check("hourly_pay", "hours_worked")
    def check_numbers_are_positive(cls, series: Series) -> Series[bool]:
        """Defines a column-level custom check."""
        return series > 0

    class Config:
        coerce = True


class IntermediateSchema(InSchema):
    total_pay: Series[float]

    @pa.dataframe_check
    def check_total_pay(cls, df: DataFrame) -> Series[bool]:
        """Defines a dataframe-level custom check."""
        return df["total_pay"] == df["hourly_pay"] * df["hours_worked"]


class OutSchema(IntermediateSchema):
    worker_id: Series[str] = pa.Field()


@task(container_image=image_spec)
def dict_to_dataframe(data: dict) -> DataFrame[InSchema]:
    """Helper task to convert a dictionary input to a dataframe."""
    return pd.DataFrame(data)


@task(container_image=image_spec)
def total_pay(df: DataFrame[InSchema]) -> DataFrame[IntermediateSchema]:  # noqa : F811
    return df.assign(total_pay=df.hourly_pay * df.hours_worked)


@task(container_image=image_spec)
def add_ids(
    df: DataFrame[IntermediateSchema], worker_ids: typing.List[str]
) -> DataFrame[OutSchema]:
    return df.assign(worker_id=worker_ids)


@workflow
def pandera_wf(  # noqa : F811
    data: dict = {
        "hourly_pay": [12.0, 13.5, 10.1],
        "hours_worked": [30.5, 40.0, 41.75],
    },
    worker_ids: typing.List[str] = ["a", "b", "c"],
) -> DataFrame[OutSchema]:
    return add_ids(df=total_pay(df=dict_to_dataframe(data=data)), worker_ids=worker_ids)
