from agent.airflow_agent import airflow_wf
from agent.sensors import sensor_wf
from core.failure_node import test_failure_node
from core.map_task import map_task_wf
from core.pod_template import pod_template_workflow
from core.shell_task import shell_task_wf
from flytekit import workflow, WorkflowFailurePolicy
from core.flyte_type import test_flyte_type_wf
from plugins.bigquery_plugin import bigquery_wf
from plugins.pandera_plugin import pandera_wf
from plugins.pytorch_plugin import pytorch_wf
from plugins.ray_plugin import ray_wf


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def wf():
    # Core
    test_flyte_type_wf()
    shell_task_wf()
    pod_template_workflow()
    test_failure_node()
    map_task_wf()

    # Plugins
    # spark_wf()  # TODO: support fast-register spark task
    ray_wf()
    pytorch_wf()
    bigquery_wf()
    pandera_wf()

    # Agents
    airflow_wf()
    sensor_wf()
