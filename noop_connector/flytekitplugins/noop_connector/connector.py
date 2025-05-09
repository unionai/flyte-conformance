import asyncio
import typing
from dataclasses import dataclass
from time import sleep

import cloudpickle

from flytekit import logger
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
from datetime import datetime, timedelta


@dataclass
class NoopMetadata(ResourceMeta):
    duration: timedelta
    create_time: datetime
    outputs: typing.Optional[LiteralMap]

    def encode(self) -> bytes:
        return cloudpickle.dumps(self)

    @classmethod
    def decode(cls, data: bytes) -> "NoopMetadata":
        return cloudpickle.loads(data)


class NoopAsyncConnector(AsyncAgentBase):
    """
    Noop async agent that does nothing but wait for a specified duration before completing
    """

    name = "Noop async Connector"

    def __init__(self):
        super().__init__(
            task_type_name="noop_async_agent_task", metadata_type=NoopMetadata
        )

    async def create(
        self,
        task_template: TaskTemplate,
        inputs: typing.Optional[LiteralMap] = None,
        **kwargs,
    ) -> NoopMetadata:
        duration = task_template.custom["duration"]
        # Mock API request
        await asyncio.sleep(0.25)
        return NoopMetadata(
            duration=timedelta(seconds=duration),
            create_time=datetime.now(),
            outputs=inputs,
        )

    async def get(self, resource_meta: NoopMetadata, **kwargs) -> Resource:
        logger.info("Noop async agent is getting the status of the task.")
        end_time = resource_meta.create_time + resource_meta.duration
        # Mock API request
        await asyncio.sleep(0.5)
        if end_time > datetime.now():
            return Resource(phase=TaskExecution.RUNNING)
        return Resource(
            phase=TaskExecution.SUCCEEDED,
            log_links=[
                TaskLog(name="Flyte Console", uri="https://github.com/flyteorg/flyte")
            ],
            outputs=resource_meta.outputs,
        )

    async def delete(self, resource_meta: NoopMetadata, **kwargs):
        assert isinstance(resource_meta, NoopMetadata)
        return


class NoopSyncConnector(SyncAgentBase):
    """
    Noop sync agent that does nothing but wait for a specified duration before completing
    """

    name = "Noop Sync Connector"

    def __init__(self):
        super().__init__(task_type_name="noop_sync_agent_task")

    def do(
        self,
        task_template: TaskTemplate,
        inputs: typing.Optional[LiteralMap] = None,
        **kwargs,
    ) -> Resource:
        logger.info("Noop sync agent is executing the task.")
        # Mock API request
        sleep(0.2)
        return Resource(phase=TaskExecution.SUCCEEDED, outputs=inputs)


AgentRegistry.register(NoopSyncConnector(), override=True)
AgentRegistry.register(NoopAsyncConnector(), override=True)
