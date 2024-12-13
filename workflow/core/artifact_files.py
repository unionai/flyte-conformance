import typing
import tempfile
import os

from flytekit.core.artifact import Artifact
from flytekit.core.task import task
from flytekit.core.workflow import workflow
from flytekit.types.file import FlyteFile
from typing_extensions import Annotated

MyFile = Artifact(name="file-my-file")


@task
def create_or_read_file(f: typing.Optional[FlyteFile]) -> Annotated[FlyteFile, MyFile]:
    if f is None:
        return FlyteFile(__file__)

    temp_dir = tempfile.mkdtemp(prefix="temp_example_")
    file_path = os.path.join(temp_dir, "file.txt")
    with open(file_path, "w") as wr:
        with open(f, "r") as r:
            print(r.read())
            r.seek(0)
            wr.write(r.read())
            wr.write("Hello, World!")

    return FlyteFile(file_path)


@workflow
def wf_create_file(f: typing.Optional[FlyteFile] = MyFile.query()):
    create_or_read_file(f=f)


@workflow
def artifacts_files_wf():
    create_or_read_file(f=None)
