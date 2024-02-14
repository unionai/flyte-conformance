from dataclasses import dataclass

from flytekit import PythonFunctionTask
from flytekit.core.base_task import PythonTask, kwtypes
from flytekit.core.interface import Interface
from flytekit.extend.backend.base_agent import AsyncAgentExecutorMixin, SyncAgentExecutorMixin


@dataclass
class MockSpark(object):
    ...


class MockSparkTask(AsyncAgentExecutorMixin, PythonFunctionTask[MockSpark]):
    def __init__(self, **kwargs):
        super().__init__(
            task_type="mock_spark",
            container_image="dummy",
            task_config={},
            task_function=lambda: None,
            **kwargs
        )


class MockOpenAITask(SyncAgentExecutorMixin, PythonTask):
    def __init__(self, **kwargs):
        super().__init__(
            task_type="mock_openai",
            task_config={},
            interface=Interface(inputs=kwtypes(prompt=str), outputs=kwtypes(o0=int)),
            **kwargs
        )
