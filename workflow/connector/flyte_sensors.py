from flytekit import task, workflow
from flytekit.sensor.file_sensor import FileSensor

sensor = FileSensor(name="test_file_sensor")


@task()
def t1():
    print("success")


@workflow()
def sensor_wf():
    sensor(path="/") >> t1()
