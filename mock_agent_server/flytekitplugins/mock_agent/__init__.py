"""
.. currentmodule:: flytekitplugins.mock_agent

This package contains things that are necessary to run a mock agent for Flyte.

.. autosummary::
   :template: custom.rst
   :toctree: generated/

   MockSparkAgent
   MockOpenAIAgent
   BigQueryAgent
"""

from .agent import MockSparkAgent, MockOpenAIAgent
from .task import MockSparkTask, MockOpenAITask, MockSpark
