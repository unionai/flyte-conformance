import os
import tempfile

from flytekit import task, workflow, dynamic
from flytekit.sensor.file_sensor import FileSensor
from flytekit.types.file import FlyteFile

sensor = FileSensor(name="test_file_sensor")


@task()
def create_flyte_file() -> FlyteFile:
    temp_dir = tempfile.mkdtemp(prefix="temp_example_")
    file_path = os.path.join(temp_dir, "file.txt")
    with open(file_path, "w") as file:
        file.write("hello world")
    return file_path

@task()
def t1():
    print("success")


@dynamic
def dynamic_task(f: FlyteFile):
    sensor(path=f.remote_source) >> t1()


@workflow()
def sensor_wf():
    f = create_flyte_file()
    dynamic_task(f=f)

