from datetime import timedelta
from flytekit import workflow, task
from flytekit.types.file import FlyteFile

cluster_name = "flyte-dataproc-demo"


@task
def create_dummy_file() -> FlyteFile:
    with open("/tmp/dummy.txt", "w") as f:
        f.write("hello world ...")
    return FlyteFile(
        path="/tmp/dummy.txt",
        remote_path="gs://opta-gcp-dogfood-gcp/flyte-conformance/dummy.txt",
    )


@workflow
def airflow_wf():
    from airflow.operators.bash import BashOperator
    from airflow.providers.google.cloud.operators.dataproc import (
        DataprocDeleteClusterOperator,
        DataprocSubmitSparkJobOperator,
        DataprocCreateClusterOperator,
    )
    from airflow.utils import trigger_rule

    BashOperator(task_id="airflow_bash_operator", bash_command="echo hello")
    generate_file = create_dummy_file()

    create_cluster = DataprocCreateClusterOperator(
        task_id="create_dataproc_cluster1",
        image_version="2.0.27-debian10",
        storage_bucket="opta-gcp-dogfood-gcp",
        service_account="dogfoodgcp-userflyterol-2xaf@dogfood-gcp-dataplane.iam.gserviceaccount.com",
        # service_account_scopes=["https://www.googleapis.com/auth/cloud-platform"],
        master_machine_type="n1-highmem-32",
        master_disk_size=1024,
        num_workers=2,
        worker_machine_type="n1-highmem-64",
        worker_disk_size=1024,
        region="us-west1",
        cluster_name=cluster_name,
        project_id="dogfood-gcp-dataplane",
    )

    spark_on_dataproc = DataprocSubmitSparkJobOperator(
        job_name="spark_pi",
        task_id="run_spark",
        dataproc_jars=["file:///usr/lib/spark/examples/jars/spark-examples.jar"],
        main_class="org.apache.spark.examples.JavaWordCount",
        arguments=["gs://opta-gcp-dogfood-gcp/flyte-conformance/dummy.txt"],
        cluster_name=cluster_name,
        region="us-west1",
        project_id="dogfood-gcp-dataplane",
    )

    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_dataproc_cluster1",
        project_id="dogfood-gcp-dataplane",
        cluster_name=cluster_name,
        region="us-west1",
        retries=3,
        retry_delay=timedelta(minutes=5),
        email_on_failure=True,
        trigger_rule=trigger_rule.TriggerRule.ALL_DONE,
    )

    generate_file >> create_cluster
    create_cluster >> spark_on_dataproc >> delete_cluster
