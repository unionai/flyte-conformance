from flytekit import workflow, WorkflowFailurePolicy

from workflow.core.map_task import map_task_wf
from workflow.core.pod_template import pod_template_workflow
from workflow.core.flyte_type import test_flyte_type_wf

from workflow.core.ephemeral_storage import ephemeral_storage_test

from workflow.plugins.pytorch_plugin import pytorch_wf
from workflow.plugins.pandera_plugin import pandera_wf
from workflow.plugins.ray_plugin import ray_wf

from workflow.agent.airflow_agent import airflow_wf
from workflow.agent.bigquery_agent import bigquery_wf
from workflow.agent.flyte_sensors import sensor_wf
from workflow.agent.mock_agents import mock_agents_wf

from flytesnacks.examples.advanced_composition.advanced_composition.chain_entities import (
    chain_tasks_wf,
    chain_workflows_wf,
)
from flytesnacks.examples.advanced_composition.advanced_composition.checkpoint import (
    checkpointing_example,
)
from flytesnacks.examples.advanced_composition.advanced_composition.conditional import (
    shape_properties,
    shape_properties_with_multiple_branches,
    shape_properties_accept_conditional_output,
    boolean_wf,
    boolean_input_wf,
    nested_conditions,
    consume_task_output,
)
from flytesnacks.examples.advanced_composition.advanced_composition.decorating_tasks import (
    decorating_task_wf,
)
from flytesnacks.examples.advanced_composition.advanced_composition.decorating_workflows import (
    decorating_workflow,
)
from flytesnacks.examples.advanced_composition.advanced_composition.dynamic_workflow import (
    dynamic_wf,
    merge_sort,
)
from flytesnacks.examples.advanced_composition.advanced_composition.subworkflow import (
    slope_intercept_wf,
    regression_line_wf,
    nested_regression_line_wf,
    nested_regression_line_lp,
)

from flytesnacks.examples.basics.basics.documenting_workflows import (
    sphinx_docstring_wf,
    numpy_docstring_wf,
    google_docstring_wf,
)

from flytesnacks.examples.basics.basics.hello_world import hello_world_wf
from flytesnacks.examples.basics.basics.imperative_workflow import imperative_wf
from flytesnacks.examples.basics.basics.launch_plan import simple_wf_lp_fixed_inputs
from flytesnacks.examples.basics.basics.named_outputs import (
    simple_wf_with_named_outputs,
)
from flytesnacks.examples.basics.basics.shell_task import shell_task_wf
from flytesnacks.examples.basics.basics.task import slope
from flytesnacks.examples.basics.basics.workflow import (
    simple_wf,
    simple_wf_with_partial,
)

from flytesnacks.examples.blast.blast.blastx_example import blast_wf

from flytesnacks.examples.development_lifecycle.development_lifecycle.failure_node import (
    wf1,
    wf2,
)
from flytesnacks.examples.development_lifecycle.development_lifecycle.task_cache import (
    cached_dataframe_wf,
)
from flytesnacks.examples.development_lifecycle.development_lifecycle.task_cache_serialize import (
    square,
)

from flytesnacks.examples.extending.extending.custom_types import (
    wf as test_custom_type_wf,
)

from flytesnacks.examples.k8s_pod_plugin.k8s_pod_plugin.pod import dynamic_pod_workflow
from flytesnacks.examples.mlflow_plugin.mlflow_plugin.mlflow_example import ml_pipeline


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def flytesnacks_wf():
    """
    TODO:
    1. Eager workflow
    2. Gate node
    3. Deck
    """
    # Advanced Composition
    chain_tasks_wf()
    chain_workflows_wf()
    checkpointing_example(n_iterations=3)
    shape_properties(radius=3.0)
    shape_properties_with_multiple_branches(radius=3.0)
    shape_properties_accept_conditional_output(radius=0.5)
    boolean_wf(seed=5)
    boolean_input_wf(boolean_input=True)
    nested_conditions(radius=0.7)
    consume_task_output(radius=0.4)
    decorating_task_wf(x=10)
    decorating_workflow(x=10.0)
    dynamic_wf(s1="Pear", s2="Earth")
    merge_sort(numbers=[3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5], numbers_count=20)
    slope_intercept_wf(x=[1, 2, 3, 4, 5], y=[6, 7, 8, 9, 10])
    regression_line_wf()
    nested_regression_line_wf()
    nested_regression_line_lp()
    simple_wf_with_named_outputs()

    # Basic
    sphinx_docstring_wf()
    numpy_docstring_wf()
    google_docstring_wf()
    hello_world_wf()
    imperative_wf(x=[-3, 0, 3], y=[7, 4, -2])
    simple_wf_lp_fixed_inputs(y=[-3, 2, -2])
    shell_task_wf()
    slope(x=[-3, 0, 3], y=[7, 4, -2])
    simple_wf(x=[-3, 0, 3], y=[7, 4, -2])
    simple_wf_with_partial(x=[-3, 0, 3], y=[7, 4, -2])

    # Development Lifecycle
    cached_dataframe_wf()
    square(n=2)
    square(n=2)
    square(n=2)
    square(n=2)

    # Extending
    test_custom_type_wf()


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def flyte_plugin_wf():
    """
    TODO:
    - Spark
    - MPI
    - Hive
    - Modin
    - Papermill
    - Great Expectations
    - AWS batch
    - DBT plugin
    - Databricks plugin
    - dolt plugin
    - duckdb plugin
    - feast plugin
    - flyteinteractive plugin
    - Dask plugin
    """
    # tensorflow_wf()
    pytorch_wf()
    ray_wf()
    pandera_wf()
    dynamic_pod_workflow()
    ml_pipeline(epochs=5)


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def case_study_wf():
    blast_wf()  # TODO: Fix it


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def flyte_agent_wf():
    airflow_wf()
    bigquery_wf()
    sensor_wf()
    mock_agents_wf()


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def flyte_conformance_wf():
    # Core
    # test_failure_node()
    test_flyte_type_wf()
    pod_template_workflow()
    map_task_wf()
    ephemeral_storage_test()


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def flyte_failure_node_wf():
    wf1()
    wf2()
