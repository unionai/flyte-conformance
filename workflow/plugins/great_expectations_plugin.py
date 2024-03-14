import os
import typing

import pandas as pd
from flytekit import Resources, kwtypes, task, workflow, ImageSpec
from flytekit.extras.sqlite3.task import SQLite3Config, SQLite3Task
from flytekit.types.file import CSVFile
from flytekit.types.schema import FlyteSchema
from flytekitplugins.great_expectations import BatchRequestConfig, GreatExpectationsTask

CONTEXT_ROOT_DIR = "greatexpectations/great_expectations"
DATASET_LOCAL = "yellow_tripdata_sample_2019-01.csv"
DATASET_REMOTE = f"https://raw.githubusercontent.com/superconductive/ge_tutorials/main/data/{DATASET_LOCAL}"
SQLITE_DATASET = "https://cdn.discordapp.com/attachments/545481172399030272/867254085426085909/movies.sqlite"

simple_task_object = GreatExpectationsTask(
    name="great_expectations_task_simple",
    datasource_name="data",
    inputs=kwtypes(dataset=str),
    expectation_suite_name="test.demo",
    data_connector_name="data_example_data_connector",
    context_root_dir=CONTEXT_ROOT_DIR,
)

image_spec = ImageSpec(
    name="flyte-conformance",
    registry="ghcr.io/unionai",
    packages=["flytekitplugins-great_expectations"],
)


@task(limits=Resources(mem="500Mi"), container_image=image_spec)
def simple_task(csv_file: str) -> int:
    # GreatExpectationsTask returns Great Expectations' checkpoint result.
    # You can print the result to know more about the data within it.
    # If the data validation fails, this will return a ValidationError.
    result = simple_task_object(dataset=csv_file)
    print(result)
    df = pd.read_csv(os.path.join("greatexpectations", "data", csv_file))
    return df.shape[0]


@workflow
def simple_wf(dataset: str = DATASET_LOCAL) -> int:
    return simple_task(csv_file=dataset)


file_task_object = GreatExpectationsTask(
    name="great_expectations_task_flytefile",
    datasource_name="data",
    inputs=kwtypes(dataset=CSVFile),
    expectation_suite_name="test.demo",
    data_connector_name="data_flytetype_data_connector",
    local_file_path="/tmp",
    context_root_dir=CONTEXT_ROOT_DIR,
)


@task(limits=Resources(mem="500Mi"), container_image=image_spec)
def file_task(
    dataset: CSVFile,
) -> int:
    file_task_object(dataset=dataset)
    return len(pd.read_csv(dataset))


@workflow
def file_wf(
    dataset: CSVFile = DATASET_REMOTE,
) -> int:
    return file_task(dataset=dataset)


schema_task_object = GreatExpectationsTask(
    name="great_expectations_task_schema",
    datasource_name="data",
    inputs=kwtypes(dataset=FlyteSchema),
    expectation_suite_name="sqlite.movies",
    data_connector_name="data_flytetype_data_connector",
    local_file_path="/tmp/test.parquet",
    context_root_dir=CONTEXT_ROOT_DIR,
)

sql_to_df = SQLite3Task(
    name="greatexpectations.task.sqlite3",
    query_template="select * from movies",
    output_schema_type=FlyteSchema,
    task_config=SQLite3Config(uri=SQLITE_DATASET),
)


@task(limits=Resources(mem="500Mi"), container_image=image_spec)
def schema_task(dataset: pd.DataFrame) -> typing.List[str]:
    schema_task_object(dataset=dataset)
    return list(dataset.columns)


@workflow
def schema_wf() -> typing.List[str]:
    df = sql_to_df()
    return schema_task(dataset=df)


runtime_task_obj = GreatExpectationsTask(
    name="greatexpectations.task.runtime",
    datasource_name="my_pandas_datasource",
    inputs=kwtypes(dataframe=FlyteSchema),
    expectation_suite_name="test.demo",
    data_connector_name="my_runtime_data_connector",
    data_asset_name="validate_pandas_data",
    task_config=BatchRequestConfig(
        batch_identifiers={
            "pipeline_stage": "validation",
        },
    ),
    context_root_dir=CONTEXT_ROOT_DIR,
)


@task(container_image=image_spec)
def runtime_to_df_task(csv_file: str) -> pd.DataFrame:
    df = pd.read_csv(os.path.join("greatexpectations", "data", csv_file))
    return df


@workflow
def runtime_wf(dataset: str = DATASET_LOCAL) -> None:
    dataframe = runtime_to_df_task(csv_file=dataset)
    runtime_task_obj(dataframe=dataframe)
