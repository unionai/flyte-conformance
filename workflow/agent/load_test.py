from flytekit import workflow, task
from flytekitplugins.mock_agent import Sleep


@task(task_config=Sleep(duration=2))
def sleep_task() -> str:
    return "Hello World!"


@workflow()
def load_test_wf():
    for i in range(100):
        sleep_task()


if __name__ == "__main__":
    print(load_test_wf())
