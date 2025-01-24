from flytekit import workflow, WorkflowFailurePolicy

from airflow_agent import airflow_wf
from bigquery_agent import bigquery_wf
from flyte_sensors import sensor_wf
from openai_batch import json_iterator_wf, jsons
from dummy_agents import dummy_agents_wf


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def flyte_agent_wf():
    airflow_wf()
    bigquery_wf()
    sensor_wf()
    json_iterator_wf(json_vals=jsons())
    dummy_agents_wf()
