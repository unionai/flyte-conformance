import typing
from datetime import datetime, timedelta

from flytekit.core.artifact import Artifact
from flytekit.core.task import task
from flytekit.core.workflow import workflow
from typing_extensions import Annotated

PrimitivesInt = Artifact(name="primitive-int")
PrimitivesFloat = Artifact(name="primitive-float")
PrimitivesStr = Artifact(name="primitive-str")
PrimitivesBool = Artifact(name="primitive-bool")
PrimitivesDatetime = Artifact(name="primitive-dt")

ListStr = Artifact(name="list-str")
MapDates = Artifact(name="map-dates")


@task
def make_int(n: typing.Optional[int]) -> Annotated[int, PrimitivesInt]:
    if n is None:
        return 42
    return n + 1


@workflow
def wf_make_int(n: typing.Optional[int] = PrimitivesInt.query()) -> int:
    return make_int(n=n)


@task
def make_float(n: typing.Optional[float]) -> Annotated[float, PrimitivesFloat]:
    if n is None:
        return 1.42
    return n + 3.14


@workflow
def wf_make_float(n: typing.Optional[float] = PrimitivesFloat.query()) -> float:
    return make_float(n=n)


@task
def make_str(s: typing.Optional[str]) -> Annotated[str, PrimitivesStr]:
    if s is None:
        return "hello"
    return s + "!"


@workflow
def wf_make_str(s: typing.Optional[str] = PrimitivesStr.query()) -> str:
    return make_str(s=s)


@task
def make_bool(n: typing.Optional[bool]) -> Annotated[bool, PrimitivesBool]:
    if n is None:
        return True
    return not n


@workflow
def wf_make_bool(n: typing.Optional[bool] = PrimitivesBool.query()) -> bool:
    return make_bool(n=n)


@task
def make_datetime(
    n: typing.Optional[datetime],
) -> Annotated[datetime, PrimitivesDatetime]:
    if n is None:
        return datetime(2063, 4, 5)
    return n + timedelta(days=1)


@workflow
def wf_make_datetime(
    n: typing.Optional[datetime] = PrimitivesDatetime.query(),
) -> datetime:
    return make_datetime(n=n)


@task
def make_list_str(
    n: typing.Optional[typing.List[str]]
) -> Annotated[typing.List[str], ListStr]:
    if n is None:
        return ["hello", "world"]
    n.append(f"{len(n)}")
    return n


@workflow
def wf_make_list_str(
    n: typing.Optional[typing.List[str]] = ListStr.query()
) -> typing.List[str]:
    return make_list_str(n=n)


@workflow
def artifact_primitives_wf():
    wf_make_int(n=None)
    wf_make_float(n=None)
    wf_make_str(s=None)
    wf_make_bool(n=None)
    wf_make_datetime(n=None)
    wf_make_list_str(n=None)


if __name__ == "__main__":
    print(wf_make_int(n=None))
    print(wf_make_int(n=42))
    print(wf_make_float(n=None))
    print(wf_make_float(n=1.42))
    print(wf_make_str(s=None))
    print(wf_make_str(s="hiii"))
    print(wf_make_bool(n=None))
    print(wf_make_bool(n=True))
    print(wf_make_datetime(n=None))
    print(wf_make_datetime(n=datetime.now()))
    print(wf_make_list_str(n=None))
    print(wf_make_list_str(n=["hello", "world"]))
