import typing
from dataclasses import dataclass

from flytekit import FlyteContext
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
class SparkMetadata(ResourceMeta):
    job_id: str


class MockSparkAgent(AsyncAgentBase):
    name = "Mock Spark Agent"

    def __init__(self):
        super().__init__(task_type_name="mock_spark", metadata_type=SparkMetadata)

    def create(
        self,
        task_template: TaskTemplate,
        inputs: typing.Optional[LiteralMap] = None,
        **kwargs,
    ) -> SparkMetadata:
        return SparkMetadata(job_id="test")

    def get(self, resource_meta: SparkMetadata, **kwargs) -> Resource:
        print("Getting status of task")
        assert isinstance(resource_meta, SparkMetadata)
        ctx = FlyteContext.current_context()
        output = TypeEngine.dict_to_literal_map(ctx, {"o0": "What is Flyte?"})
        return Resource(
            phase=TaskExecution.SUCCEEDED,
            log_links=[TaskLog(name="console", uri="localhost:3000")],
            outputs=output,
        )

    def delete(self, resource_meta: SparkMetadata, **kwargs):
        assert isinstance(resource_meta, SparkMetadata)
        return


class MockOpenAIAgent(SyncAgentBase):
    name = "Mock OpenAI Agent"

    def __init__(self):
        super().__init__(task_type_name="mock_openai")

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
AgentRegistry.register(MockSparkAgent(), override=True)
