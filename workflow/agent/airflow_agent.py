from datetime import datetime, timedelta

from airflow.operators.bash import BashOperator
from pytz import UTC
from flytekit import workflow

x = (datetime.now(tz=UTC) + timedelta(seconds=21)).time()
cluster_name = "flyte-dataproc-demo"


@workflow
def airflow_wf():
    # TimeSensor(task_id="time_sensor", target_time=x)
    BashOperator(task_id="airflow_bash_operator", bash_command="echo hello")

    # create_cluster = DataprocCreateClusterOperator(
    #     task_id="create_dataproc_cluster1",
    #     image_version="2.0.27-debian10",
    #     storage_bucket="opta-gcp-dogfood-gcp",
    #     service_account="dogfoodgcp-userflyterol-odkb@dogfood-gcp-dataplane.iam.gserviceaccount.com",
    #     # service_account_scopes=["https://www.googleapis.com/auth/cloud-platform"],
    #     master_machine_type="n1-highmem-32",
    #     master_disk_size=1024,
    #     num_workers=2,
    #     worker_machine_type="n1-highmem-64",
    #     worker_disk_size=1024,
    #     region="us-west1",
    #     cluster_name=cluster_name,
    #     project_id="dogfood-gcp-dataplane",
    # )
    #
    # spark_on_dataproc = DataprocSubmitSparkJobOperator(
    #     job_name="spark_pi",
    #     task_id="run_spark",
    #     dataproc_jars=["file:///usr/lib/spark/examples/jars/spark-examples.jar"],
    #     main_class="org.apache.spark.examples.JavaWordCount",
    #     arguments=["gs://opta-gcp-dogfood-gcp/spark/file.txt"],
    #     cluster_name=cluster_name,
    #     region="us-west1",
    #     project_id="dogfood-gcp-dataplane",
    # )
    #
    # delete_cluster = DataprocDeleteClusterOperator(
    #     task_id="delete_dataproc_cluster1",
    #     project_id="dogfood-gcp-dataplane",
    #     cluster_name=cluster_name,
    #     region="us-west1",
    #     retries=3,
    #     retry_delay=timedelta(minutes=5),
    #     email_on_failure=True,
    #     trigger_rule=trigger_rule.TriggerRule.ALL_DONE,
    # )
    #
    # create_cluster >> spark_on_dataproc >> delete_cluster
