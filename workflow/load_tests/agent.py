import typing
from time import sleep
from typing import Optional, List

from union import ActorEnvironment

from flytekit import workflow, ImageSpec, Resources
from pydantic import BaseModel, Field

from flytekit.core.task import Echo


class Child(BaseModel):
    name: str = Field(..., description="The child's name")
    age: int = Field(..., ge=0, description="The child's age (must be non-negative)")


class Job(BaseModel):
    title: str = Field(..., description="The person's job title")
    company: str = Field(..., description="The company where the person works")
    salary: Optional[float] = Field(
        None, ge=0, description="The annual salary, if known"
    )


class Home(BaseModel):
    address: str = Field(..., description="The residential address")
    type: Optional[str] = Field(
        None, description="The type of home, e.g., apartment, house"
    )


class Human(BaseModel):
    first_name: str = Field(..., description="The first name of the person")
    last_name: str = Field(..., description="The last name of the person")
    phone_number: Optional[str] = Field(None, description="The person's phone number")
    gender: Optional[str] = Field(
        None, description="The gender of the person, if specified"
    )
    children: Optional[List[Child]] = Field(
        None, description="List of the person's children"
    )
    job: Optional[Job] = Field(None, description="The person's job information")
    home: Optional[Home] = Field(None, description="Details about the person's home")

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+123456789",
                "gender": "Male",
                "children": [{"name": "Alice", "age": 10}, {"name": "Bob", "age": 7}],
                "job": {
                    "title": "Software Engineer",
                    "company": "TechCorp",
                    "salary": 120000,
                },
                "home": {"address": "123 Main St, Springfield, USA", "type": "House"},
            }
        }


person = Human(
    first_name="Jane",
    last_name="Smith",
    phone_number="+19876543210",
    gender="Female",
    children=[{"name": "Emma", "age": 5}, {"name": "Oliver", "age": 3}],
    job={"title": "Product Manager", "company": "Innovate Inc.", "salary": 95000},
    home={"address": "789 Park Ave, Metropolis, USA", "type": "Apartment"},
)

image_spec = ImageSpec(registry="ghcr.io/flyteorg", packages=["pydantic", "union"])

echo = Echo(name="echo", inputs={"a": typing.Optional[float]})

actor = ActorEnvironment(
    name="load-test",
    replica_count=8000,
    ttl_seconds=300,
    container_image=image_spec,
    requests=Resources(cpu="50m", mem="200Mi"),
    limits=Resources(cpu="200m", mem="600Mi"),
)


# @task(requests=Resources(cpu="50m", mem="200Mi"), limits=Resources(cpu="200m", mem="600Mi"), container_image=image_spec)
@actor.task
def noop_container_task(sec: int):
    sleep(sec)


@workflow()
def echo_wf():
    echo(a=1.0)


@workflow()
def video_wf():
    from flytekitplugins.noop_connector import NoopAgentAsyncTask

    async_task = NoopAgentAsyncTask(
        name="video_task", duration=90, inputs={"person": Human}
    )
    a1 = async_task(person=person)
    a2 = async_task(person=person)
    a3 = async_task(person=person)
    a4 = async_task(person=person)
    t1 = noop_container_task(sec=120)
    t2 = noop_container_task(sec=60)

    a1 >> a2
    a1 >> a3
    a3 >> t1
    t1 >> a4
    a4 >> t2


@workflow()
def text_wf():
    from flytekitplugins.noop_connector import NoopAgentAsyncTask

    async_task = NoopAgentAsyncTask(
        name="text_task", duration=40, inputs={"person": Human}
    )
    a1 = async_task(person=person)
    t1 = noop_container_task(sec=60)
    t2 = noop_container_task(sec=60)
    t1 >> a1
    a1 >> t2


@workflow()
def image_wf():
    from flytekitplugins.noop_connector import NoopAgentAsyncTask

    async_task = NoopAgentAsyncTask(
        name="image_task", duration=40, inputs={"person": Human}
    )
    a1 = async_task(person=person)
    a2 = async_task(person=person)
    t1 = noop_container_task(sec=60)
    t2 = noop_container_task(sec=60)
    a1 >> t1
    t1 >> a2
    a2 >> t2
