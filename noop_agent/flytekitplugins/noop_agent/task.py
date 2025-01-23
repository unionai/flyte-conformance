from typing import Optional, Dict, Any, Type

from flytekit.configuration import SerializationSettings
from flytekit.core.base_task import PythonTask
from flytekit.core.interface import Interface
from flytekit.extend.backend.base_agent import (
    AsyncAgentExecutorMixin,
    SyncAgentExecutorMixin,
)


class NoopAgentAsyncTask(AsyncAgentExecutorMixin, PythonTask):
    _TASK_TYPE = "noop_async_agent_task"

    def __init__(
        self,
        name: str,
        inputs: Optional[Dict[str, Type]] = None,
        duration: int = 2,
        **kwargs,
    ):
        """
        NoopAgentAsyncTask Task that does nothing but wait for a specified duration before completing

        :param name: The Name of this task, should be unique in the project
        :param inputs: Name and type of inputs specified as an ordered dictionary
        :param duration: The duration the agent will wait
        :param kwargs: All other args required by Parent type
        """
        super().__init__(
            name=name,
            interface=Interface(inputs=inputs, outputs=inputs),
            task_type=self._TASK_TYPE,
            **kwargs,
        )
        self._duration = duration

    def get_custom(self, settings: SerializationSettings) -> Optional[Dict[str, Any]]:
        return {"duration": self._duration}


class SleepTask(AsyncAgentExecutorMixin, PythonTask):
    _TASK_TYPE = "sleep_agent_task"

    def __init__(
        self,
        name: str,
        datetime: str,
        inputs: Optional[Dict[str, Type]] = None,
        **kwargs,
    ):
        """
        Sleep Task that does nothing but wait for a specified duration before completing

        :param name: The Name of this task, should be unique in the project
        :param inputs: Name and type of inputs specified as an ordered dictionary
        :param duration: The duration the agent will wait
        :param kwargs: All other args required by Parent type
        """
        super().__init__(
            name=name,
            interface=Interface(inputs=inputs, outputs=inputs),
            task_type=self._TASK_TYPE,
            **kwargs,
        )
        self._datetime = datetime

    def get_custom(self, settings: SerializationSettings) -> Optional[Dict[str, Any]]:
        return {"datetime": self._datetime}


class NoopAgentSyncTask(SyncAgentExecutorMixin, PythonTask):
    def __init__(self, inputs: Optional[Dict[str, Type]] = None, **kwargs):
        super().__init__(
            task_type="noop_sync_agent_task",
            interface=Interface(inputs=inputs, outputs=inputs),
            **kwargs,
        )
