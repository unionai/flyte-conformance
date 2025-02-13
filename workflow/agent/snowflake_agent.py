from flytekit import kwtypes, workflow, task, ImageSpec, StructuredDataset
from flytekitplugins.snowflake import SnowflakeConfig, SnowflakeTask
from flytekit import Secret
import pandas as pd

image = ImageSpec(
    packages=["flytekitplugins-snowflake", "pandas"],
    registry="ghcr.io/unionai",
)

snowflake_task_insert_query = SnowflakeTask(
    name="insert-dynamic-query",
    inputs=kwtypes(id=int, name=str, age=int),
    task_config=SnowflakeConfig(
        account="WNITKUT-UJ60052",
        user="HANRU",
        database="FLYTEAGENT",
        schema="PUBLIC",
        warehouse="COMPUTE_WH",
        table="FLYTEAGENT.PUBLIC.TEST",
    ),
    query_template="""
            INSERT INTO FLYTEAGENT.PUBLIC.TEST (ID, NAME, AGE)
            VALUES (%(id)s, %(name)s, %(age)s);
            """,
)

snowflake_task_templatized_query = SnowflakeTask(
    name="test-simple-query",
    output_schema_type=StructuredDataset,
    task_config=SnowflakeConfig(
        account="WNITKUT-UJ60052",
        user="HANRU",
        database="FLYTEAGENT",
        schema="PUBLIC",
        warehouse="COMPUTE_WH",
        table="FLYTEAGENT.PUBLIC.TEST",
    ),
    query_template="SELECT * FROM FLYTEAGENT.PUBLIC.TEST LIMIT 1;",
)


@task(container_image=image, secret_requests=[Secret(key="snowflake")])
def print_head(input_sd: StructuredDataset) -> pd.DataFrame:
    df = input_sd.open(pd.DataFrame).all()
    print(df)
    return df


@task(container_image=image, secret_requests=[Secret(key="snowflake")])
def write_table() -> StructuredDataset:
    df = pd.DataFrame(
        {"ID": [1, 2, 3], "NAME": ["union", "union", "union"], "AGE": [30, 30, 30]}
    )
    print(df)
    return StructuredDataset(
        dataframe=df,
        uri="snowflake://HANRU/WNITKUT-UJ60052/COMPUTE_WH/FLYTEAGENT/PUBLIC/TEST",
    )


@workflow
def wf() -> StructuredDataset:
    sd = snowflake_task_templatized_query()
    t1 = print_head(input_sd=sd)
    insert_query = snowflake_task_insert_query(id=1, name="Flyte", age=30)
    sd2 = snowflake_task_templatized_query()

    sd >> t1 >> insert_query >> sd2
    write_table()
    return print_head(input_sd=sd2)


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    wf()
    print("Done!")
