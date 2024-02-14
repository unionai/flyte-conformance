import json
import typing
from dataclasses import dataclass, asdict

from flytekit import FlyteContext
from flytekit.core.type_engine import TypeEngine, dataclass_from_dict
from flytekit.extend.backend.base_agent import SyncAgentBase, AsyncAgentBase, AgentRegistry
from flytekit.models.literals import LiteralMap
from flytekit.models.task import TaskTemplate
from flyteidl.admin.agent_pb2 import ExecuteTaskSyncResponse, ExecuteTaskSyncResponseHeader, Resource, \
    CreateTaskResponse, GetTaskResponse, DeleteTaskResponse
from flyteidl.core.execution_pb2 import TaskExecution, TaskLog

from flytekitplugins.spark import DatabricksAgent


@dataclass
class Metadata:
    job_id: str

    def encode(self) -> bytes:
        return json.dumps(asdict(self)).encode("utf-8")

    @classmethod
    def decode(cls, data: bytes) -> "Metadata":
        return dataclass_from_dict(cls, json.loads(data.decode("utf-8")))


class MockSparkAgent(AsyncAgentBase):
    name = "Mock Spark Agent"

    def __init__(self):
        super().__init__(task_type_name="mock_spark")

    def create(
        self, output_prefix: str, task_template: TaskTemplate, inputs: typing.Optional[LiteralMap] = None, **kwargs
    ) -> CreateTaskResponse:
        metadata = Metadata(job_id="test")
        return CreateTaskResponse(resource_meta=metadata.encode())

    def get(self, resource_meta: bytes, **kwargs) -> GetTaskResponse:
        Metadata.decode(resource_meta)
        return GetTaskResponse(
            resource=Resource(phase=TaskExecution.SUCCEEDED),
            log_links=[TaskLog(name="console", uri="localhost:3000")],
        )

    def delete(self, resource_meta: bytes, **kwargs) -> DeleteTaskResponse:
        return DeleteTaskResponse()


class MockOpenAIAgent(SyncAgentBase):
    name = "Mock OpenAI Agent"

    def __init__(self):
        super().__init__(task_type_name="mock_openai")

    def do(
        self,
        output_prefix: str,
        task_template: TaskTemplate,
        inputs: typing.Iterable[LiteralMap] = None,
        **kwargs,
    ) -> typing.Iterator[ExecuteTaskSyncResponse]:
        header = ExecuteTaskSyncResponseHeader(resource=Resource(phase=TaskExecution.SUCCEEDED))
        ctx = FlyteContext.current_context()
        output1 = TypeEngine.dict_to_literal_map_idl(ctx, {"o0": "Scalable and flexible workflow orchestration platform"})
        output2 = TypeEngine.dict_to_literal_map_idl(ctx, {"o0": "that seamlessly unifies data, ML and analytics stacks"})
        yield ExecuteTaskSyncResponse(header=header)
        yield ExecuteTaskSyncResponse(outputs=output1)
        yield ExecuteTaskSyncResponse(outputs=output2)


AgentRegistry.register(MockOpenAIAgent(), override=True)
AgentRegistry.register(MockSparkAgent(), override=True)
