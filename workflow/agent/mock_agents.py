from flytekit import workflow, task, ImageSpec
from flytekitplugins.mock_agent import Spark
from flytekitplugins.mock_agent import MockOpenAITask
from flytekitplugins.mock_agent.task import OpenAI

image_spec = ImageSpec(name="openai", registry="pingsutw")
openai_task = MockOpenAITask(name="openai", task_config=OpenAI(container_image=image_spec))


@task(task_config=Spark(worker=2))
def spark_task() -> str:
    return "What is Flyte?"


@workflow()
def mock_agents_wf() -> str:
    question = spark_task()
    return openai_task(prompt=question)


if __name__ == "__main__":
    print(mock_agents_wf())
