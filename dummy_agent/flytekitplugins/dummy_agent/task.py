from dataclasses import dataclass
from typing import Callable, Optional, Union, Dict, Any

from flytekit import PythonFunctionTask, ImageSpec
from flytekit.configuration import SerializationSettings
from flytekit.core.base_task import PythonTask, kwtypes
from flytekit.core.interface import Interface
from flytekit.core.task import TaskPlugins
from flytekit.extend.backend.base_agent import (
    AsyncAgentExecutorMixin,
    SyncAgentExecutorMixin,
)
from flytekit.image_spec.image_spec import ImageBuildEngine
from flytekit.models.literals import LiteralMap


@dataclass
class Sleep(object):
    duration: int


class SleepTask(AsyncAgentExecutorMixin, PythonFunctionTask[Sleep]):
    def __init__(
        self,
        task_config: Sleep,
        task_function: Callable,
        container_image: Optional[Union[str, ImageSpec]] = None,
        **kwargs,
    ):
        super().__init__(
            task_type="sleep",
            container_image="dummy",
            task_config=task_config,
            task_function=task_function,
            **kwargs,
        )

    def get_custom(self, settings: SerializationSettings) -> Optional[Dict[str, Any]]:
        return {"duration": self.task_config.duration}

    def execute(self, **kwargs) -> LiteralMap:
        return AsyncAgentExecutorMixin.execute(self, **kwargs)


@dataclass
class OpenAI(object):
    container_image: Union[str, ImageSpec]


class MockOpenAITask(SyncAgentExecutorMixin, PythonTask):
    def __init__(self, task_config: Optional[OpenAI], **kwargs):
        super().__init__(
            task_type="dummy_openai",
            task_config=task_config,
            interface=Interface(inputs=kwtypes(prompt=str), outputs=kwtypes(o0=str)),
            **kwargs,
        )

    def get_custom(self, settings: SerializationSettings) -> Optional[Dict[str, Any]]:
        if isinstance(self.task_config.container_image, ImageSpec):
            ImageBuildEngine.build(self.task_config.container_image)
            return {"container_image": self.task_config.container_image.image_name()}
        return {"container_image": self.task_config.container_image}


TaskPlugins.register_pythontask_plugin(Sleep, SleepTask)
