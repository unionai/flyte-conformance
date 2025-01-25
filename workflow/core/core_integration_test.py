from flytekit import workflow, WorkflowFailurePolicy

from .map_task import map_task_wf
# from core.pod_template import pod_template_workflow
from .flyte_type import test_flyte_type_wf
from .ephemeral_storage import ephemeral_storage_test
from .actor import actor_wf
from .image_spec_composition import composition_image_wf
from .gcp_secret import gcp_secret_wf
from .artifact_primitives import artifact_primitives_wf
from .artifact_files import artifacts_files_wf


@workflow(failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
def flyte_conformance_wf():
    test_flyte_type_wf()
    # pod_template_workflow()  # uncomment after flytesnacks is updated
    map_task_wf()
    ephemeral_storage_test()
    actor_wf()
    composition_image_wf()
    gcp_secret_wf()
    artifact_primitives_wf()
    artifacts_files_wf()
