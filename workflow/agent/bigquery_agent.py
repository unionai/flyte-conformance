import pandas as pd
import pyarrow as pa
from flytekit import StructuredDataset, kwtypes, task, workflow, ImageSpec
from flytekitplugins.bigquery import BigQueryConfig, BigQueryTask
from typing_extensions import Annotated

MyDataset = Annotated[StructuredDataset, kwtypes(name=str)]

image_spec = ImageSpec(
    name="flyte-conformance",
    packages=[
        "flytekitplugins-bigquery",
        "flytekit",
        "google-cloud-bigquery-storage",
        "google-cloud-bigquery",
        "pandas",
        "pyarrow",
    ],
    registry="ghcr.io/unionai",
)


@task(container_image=image_spec)
def create_bq_table() -> StructuredDataset:
    df = pd.DataFrame(data={"name": ["Alice", "bob"], "age": [5, 6]})
    return StructuredDataset(
        dataframe=df, uri="bq://dogfood-gcp-dataplane:dataset.flyte_table333"
    )


bigquery_task_templatized_query = BigQueryTask(
    name="bigquery",
    inputs=kwtypes(version=int),
    output_structured_dataset_type=MyDataset,
    task_config=BigQueryConfig(ProjectID="dogfood-gcp-dataplane"),
    query_template="SELECT * from dataset.flyte_table3;",  # type: ignore
)


@task(container_image=image_spec)
def convert_bq_table_to_arrow_table(sd: MyDataset) -> pa.Table:
    t = sd.open(pa.Table).all()
    print(t)
    return t


@workflow
def bigquery_wf(version: int = 10) -> pa.Table:
    sd = bigquery_task_templatized_query(version=version)
    create_bq_table() >> sd
    return convert_bq_table_to_arrow_table(sd=sd)
