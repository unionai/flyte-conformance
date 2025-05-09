from datetime import timedelta

from flytekit import workflow, WorkflowFailurePolicy, LaunchPlan, FixedRate

from core.map_task import map_task_wf

# from core.pod_template import pod_template_workflow
from core.flyte_type import test_flyte_type_wf
from core.ephemeral_storage import ephemeral_storage_test
from core.actor import actor_wf
from core.image_spec_composition import composition_image_wf
from core.gcp_secret import gcp_secret_wf
from core.artifact_primitives import artifact_primitives_wf
from core.artifact_files import artifacts_files_wf

# from connector.airflow_connector import airflow_wf
from connector.bigquery_connector import bigquery_wf
from connector.flyte_sensors import sensor_wf
from connector.openai_batch import json_iterator_wf, jsons
from connector.noop_connector import noop_connectors_wf

from flytesnacks.examples.advanced_composition.advanced_composition.chain_entities import (
    chain_tasks_wf,
    chain_workflows_wf,
)
from flytesnacks.examples.advanced_composition.advanced_composition.checkpoint import (
    checkpointing_example,  # noqa: F401
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

from flytesnacks.examples.development_lifecycle.development_lifecycle.task_cache import (
    cached_dataframe_wf,
)
from flytesnacks.examples.development_lifecycle.development_lifecycle.task_cache_serialize import (
    square,
)

from flytesnacks.examples.extending.extending.custom_types import (
    wf as test_custom_type_wf,
)

from flytesnacks.examples.mlflow_plugin.mlflow_plugin.mlflow_example import ml_pipeline
from flytesnacks.examples.pandera_plugin.pandera_plugin.basic_schema_example import (
    process_data,
)
from flytesnacks.examples.pandera_plugin.pandera_plugin.validating_and_testing_ml_pipelines import (
    pipeline,
)
from flytesnacks.examples.kfpytorch_plugin.kfpytorch_plugin.pytorch_mnist import (
    pytorch_training_wf,
)
from flytesnacks.examples.ray_plugin.ray_plugin.ray_example import ray_workflow
from flytesnacks.examples.k8s_spark_plugin.k8s_spark_plugin.dataframe_passing import (
    spark_to_pandas_wf,  # noqa: F401
)
from flytesnacks.examples.k8s_spark_plugin.k8s_spark_plugin.pyspark_pi import my_spark


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
    # checkpointing_example(n_iterations=3)
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
    TODO: Fix the following workflows
    - Databricks
    - Papermill
    - flyteinteractive plugin
    - DBT plugin
    - duckdb plugin
    - Great Expectations
    - AWS batch
    - Dask plugin
    - MPI
    - Modin
    - dolt plugin
    - feast plugin
    - Hive
    - mnist_tensorflow_workflow
    """
    pytorch_training_wf()
    # ray_workflow(n=3)
    process_data()
    pipeline(data_random_state=42, model_random_state=42)
    ml_pipeline(epochs=5)
    spark_to_pandas_wf()
    my_spark()


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def case_study_wf():
    blast_wf()  # TODO: Fix it


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def flyte_connector_wf():
    # airflow_wf()
    bigquery_wf()
    sensor_wf()
    json_iterator_wf(json_vals=jsons())
    noop_connectors_wf()


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def flyte_conformance_wf():
    test_flyte_type_wf()
    # pod_template_workflow()  # uncomment after flytesnacks is updated
    map_task_wf()
    ephemeral_storage_test()
    actor_wf()
    composition_image_wf()
    gcp_secret_wf()
    artifact_primitives_wf()
    artifacts_files_wf()


flytesnacks_lp = LaunchPlan.get_or_create(
    name="flytesnacks_lp",
    workflow=flytesnacks_wf,
    schedule=FixedRate(duration=timedelta(hours=1)),
    max_parallelism=100,
)

flyte_plugin_lp = LaunchPlan.get_or_create(
    name="flyte_plugin_lp",
    workflow=flyte_plugin_wf,
    schedule=FixedRate(duration=timedelta(hours=6)),
    max_parallelism=100,
)


flyte_connector_lp = LaunchPlan.get_or_create(
    name="flyte_connector_lp",
    workflow=flyte_connector_wf,
    schedule=FixedRate(duration=timedelta(hours=6)),
    max_parallelism=100,
)

flyte_conformance_lp = LaunchPlan.get_or_create(
    name="flyte_conformance_lp",
    workflow=flyte_conformance_wf,
    schedule=FixedRate(duration=timedelta(hours=1)),
    max_parallelism=100,
)
