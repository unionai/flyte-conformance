from dataclasses import dataclass
from typing import Callable, Optional, Union

from flytekit import PythonFunctionTask, ImageSpec
from flytekit.core.base_task import PythonTask, kwtypes
from flytekit.core.interface import Interface
from flytekit.core.task import TaskPlugins
from flytekit.extend.backend.base_agent import (
    AsyncAgentExecutorMixin,
    SyncAgentExecutorMixin,
)
from flytekit.models.literals import LiteralMap


@dataclass
class MockSpark(object):
    ...


class MockSparkTask(AsyncAgentExecutorMixin, PythonFunctionTask[MockSpark]):
    def __init__(
        self,
        task_config: MockSpark,
        task_function: Callable,
        container_image: Optional[Union[str, ImageSpec]] = None,
        **kwargs,
    ):
        super().__init__(
            task_type="mock_spark",
            container_image="dummy",
            task_config=task_config,
            task_function=task_function,
            **kwargs,
        )

    def execute(self, **kwargs) -> LiteralMap:
        return AsyncAgentExecutorMixin.execute(self, **kwargs)


class MockOpenAITask(SyncAgentExecutorMixin, PythonTask):
    def __init__(self, **kwargs):
        super().__init__(
            task_type="mock_openai",
            task_config={},
            interface=Interface(inputs=kwtypes(prompt=str), outputs=kwtypes(o0=str)),
            **kwargs,
        )


TaskPlugins.register_pythontask_plugin(MockSpark, MockSparkTask)
