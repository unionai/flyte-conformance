import typing

from flytekit import workflow, task
from flytekitplugins.mock_agent import MockSpark
from mock_agent_server.flytekitplugins.mock_agent import MockOpenAITask

openai_task = MockOpenAITask(name="openai")


@task(task_config=MockSpark())
def spark_task() -> str:
    return "What is Flyte?"


@workflow
def wf() -> typing.List[str]:
    question = spark_task()
    return openai_task(prompt=question)


if __name__ == '__main__':
    print(wf())

