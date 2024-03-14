from .airflow_agent import airflow_wf
from .flyte_sensors import sensor_wf
from .mock_agents import mock_agents_wf
from flytekit import workflow, WorkflowFailurePolicy


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def agent_wf():
    airflow_wf()
    # bigquery_wf()
    sensor_wf()
    mock_agents_wf()
