from flytekit import workflow, task, LaunchPlan
from flytekitplugins.mock_agent import Sleep


@task(task_config=Sleep(duration=2))
def sleep_task() -> str:
    return "Hello World!"


@workflow()
def sleep_wf():
    for i in range(50):
        sleep_task()


@workflow
def load_test_wf():
    sleep_lp = LaunchPlan.get_or_create(name="fixed_inputs", workflow=sleep_wf, max_parallelism=100)
    for i in range(64):
        sleep_lp()


if __name__ == "__main__":
    sleep_task()
