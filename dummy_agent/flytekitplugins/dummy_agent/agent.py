import random
import typing
from dataclasses import dataclass
from time import sleep

from flytekit import FlyteContext, logger
from flytekit.core.type_engine import TypeEngine
from flytekit.extend.backend.base_agent import (
    SyncAgentBase,
    AsyncAgentBase,
    AgentRegistry,
    Resource,
    ResourceMeta,
)
from flytekit.models.literals import LiteralMap
from flytekit.models.task import TaskTemplate
from flyteidl.core.execution_pb2 import TaskExecution, TaskLog


@dataclass
class SleepMetadata(ResourceMeta):
    duration: int


class SleepAgent(AsyncAgentBase):
    name = "Sleep Agent"

    def __init__(self):
        super().__init__(task_type_name="sleep", metadata_type=SleepMetadata)

    def create(
        self,
        task_template: TaskTemplate,
        inputs: typing.Optional[LiteralMap] = None,
        **kwargs,
    ) -> SleepMetadata:
        duration = task_template.custom["duration"]
        return SleepMetadata(duration=duration)

    def get(self, resource_meta: SleepMetadata, **kwargs) -> Resource:
        logger.info("Sleep agent is getting the status of the task.")
        assert isinstance(resource_meta, SleepMetadata)
        sleep(random.random())
        ctx = FlyteContext.current_context()
        output = TypeEngine.dict_to_literal_map(ctx, {"o0": "What is Flyte?"})
        return Resource(
            phase=TaskExecution.SUCCEEDED,
            log_links=[
                TaskLog(name="Flyte Console", uri="https://github.com/flyteorg/flyte")
            ],
            outputs=output,
        )

    def delete(self, resource_meta: SleepMetadata, **kwargs):
        assert isinstance(resource_meta, SleepMetadata)
        return


class MockOpenAIAgent(SyncAgentBase):
    name = "Mock OpenAI Agent"

    def __init__(self):
        super().__init__(task_type_name="dummy_openai")

    def do(
        self,
        task_template: TaskTemplate,
        inputs: typing.Optional[LiteralMap] = None,
        **kwargs,
    ) -> Resource:
        print("Executing task")
        ctx = FlyteContext.current_context()
        python_inputs = TypeEngine.literal_map_to_kwargs(
            ctx, inputs, literal_types=task_template.interface.inputs
        )
        print(python_inputs)
        # Openai Call
        output = {
            "o0": "Flyte is a scalable and flexible workflow orchestration platform"
        }
        return Resource(phase=TaskExecution.SUCCEEDED, outputs=output)


AgentRegistry.register(MockOpenAIAgent(), override=True)
AgentRegistry.register(SleepAgent(), override=True)
