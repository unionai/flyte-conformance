from flytekit import workflow, WorkflowFailurePolicy

from workflow.core.map_task import map_task_wf
from workflow.core.pod_template import pod_template_workflow
from workflow.core.shell_task import shell_task_wf
from workflow.core.chaining import chain_tasks_wf
from workflow.core.condictional import (
    shape_properties,
    shape_properties_with_multiple_branches,
    shape_properties_accept_conditional_output,
    boolean_wf,
    boolean_input_wf,
    nested_conditions,
    consume_task_output,
)
from workflow.core.dynamic_workflow import dynamic_wf, merge_sort
from workflow.core.flyte_type import test_flyte_type_wf
from workflow.plugins.pandera_plugin import pandera_wf
from workflow.plugins.ray_plugin import ray_wf

from workflow.agent.airflow_agent import airflow_wf
from workflow.agent.bigquery_agent import bigquery_wf
from workflow.agent.flyte_sensors import sensor_wf
from workflow.agent.mock_agents import mock_agents_wf


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def wf():
    # Core
    # test_failure_node()
    test_flyte_type_wf()
    shell_task_wf()
    pod_template_workflow()
    map_task_wf()
    shape_properties()
    shape_properties_with_multiple_branches()
    shape_properties_accept_conditional_output()
    boolean_wf()
    boolean_input_wf()
    nested_conditions()
    consume_task_output()
    chain_tasks_wf()
    dynamic_wf()
    merge_sort()

    # Plugins
    # spark_wf()  # TODO: support fast-register spark task
    # pytorch_wf() # TODO: Fix pytorch plugin
    ray_wf()
    pandera_wf()

    # Agents
    airflow_wf()
    bigquery_wf()
    sensor_wf()
    mock_agents_wf()
