from workflow.agent.agent_workflows import agent_wf

from workflow.core.map_task import map_task_wf
from workflow.core.pod_template import pod_template_workflow
from workflow.core.shell_task import shell_task_wf
from workflow.core.condictional import (
    shape_properties,
    shape_properties_with_multiple_branches,
    shape_properties_accept_conditional_output,
    boolean_wf,
    boolean_input_wf,
    nested_conditions,
    consume_task_output,
)
from flytekit import workflow, WorkflowFailurePolicy
from workflow.core.flyte_type import test_flyte_type_wf
from workflow.plugins.pandera_plugin import pandera_wf
from workflow.plugins.ray_plugin import ray_wf


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

    # Plugins
    # spark_wf()  # TODO: support fast-register spark task
    # pytorch_wf() # TODO: Fix pytorch plugin
    ray_wf()
    pandera_wf()

    # Agents
    agent_wf()
