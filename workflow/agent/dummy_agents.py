from flytekit import workflow, task, ImageSpec
from flytekitplugins.dummy_agent import Sleep
from flytekitplugins.dummy_agent import MockOpenAITask
from flytekitplugins.dummy_agent.task import OpenAI

image_spec = ImageSpec(name="flyte-conformance", registry="ghcr.io/unionai")
openai_task = MockOpenAITask(
    name="openai", task_config=OpenAI(container_image=image_spec)
)


@task(task_config=Sleep(duration=1))
def spark_task() -> str:
    return "What is Flyte?"


@workflow()
def dummy_agents_wf() -> str:
    question = spark_task()
    return openai_task(prompt=question)


if __name__ == "__main__":
    print(dummy_agents_wf())
