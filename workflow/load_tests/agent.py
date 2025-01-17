from time import sleep
from typing import Optional, List

from flytekit import workflow, task, LaunchPlan, map_task, ImageSpec
from .generate_outputs import generate_list


from pydantic import BaseModel, Field


class Child(BaseModel):
    name: str = Field(..., description="The child's name")
    age: int = Field(..., ge=0, description="The child's age (must be non-negative)")


class Job(BaseModel):
    title: str = Field(..., description="The person's job title")
    company: str = Field(..., description="The company where the person works")
    salary: Optional[float] = Field(None, ge=0, description="The annual salary, if known")


class Home(BaseModel):
    address: str = Field(..., description="The residential address")
    type: Optional[str] = Field(None, description="The type of home, e.g., apartment, house")


class Human(BaseModel):
    first_name: str = Field(..., description="The first name of the person")
    last_name: str = Field(..., description="The last name of the person")
    phone_number: Optional[str] = Field(None, description="The person's phone number")
    gender: Optional[str] = Field(None, description="The gender of the person, if specified")
    children: Optional[List[Child]] = Field(None, description="List of the person's children")
    job: Optional[Job] = Field(None, description="The person's job information")
    home: Optional[Home] = Field(None, description="Details about the person's home")

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "+123456789",
                "gender": "Male",
                "children": [
                    {"name": "Alice", "age": 10},
                    {"name": "Bob", "age": 7}
                ],
                "job": {
                    "title": "Software Engineer",
                    "company": "TechCorp",
                    "salary": 120000
                },
                "home": {
                    "address": "123 Main St, Springfield, USA",
                    "type": "House"
                }
            }
        }


person = Human(
    first_name="Jane",
    last_name="Smith",
    phone_number="+19876543210",
    gender="Female",
    children=[
        {"name": "Emma", "age": 5},
        {"name": "Oliver", "age": 3}
    ],
    job={
        "title": "Product Manager",
        "company": "Innovate Inc.",
        "salary": 95000
    },
    home={
        "address": "789 Park Ave, Metropolis, USA",
        "type": "Apartment"
    }
)

image_spec = ImageSpec(registry="ghcr.io/flyteorg", packages=["pydantic"])


@task(container_image=image_spec.force_push())
def noop_container_task():
    sleep(120)


@workflow()
def noop_wf(num_wf: int):
    noop_container_task()
    noop_container_task()

    from flytekitplugins.noop_agent import NoopAgentAsyncTask
    async_task = NoopAgentAsyncTask(name="noop_agent_task", duration=120, inputs={"person": Human})

    async_task(person=person)
    async_task(person=person)
    async_task(person=person)
    async_task(person=person)


noop_lp = LaunchPlan.get_or_create(name="noop_lp", workflow=noop_wf, max_parallelism=200)


@workflow()
def agent_wf_map_task(num_wf: int = 3):
    map_task(noop_lp)(num_wf=generate_list(num=num_wf))


if __name__ == "__main__":
    agent_wf_map_task(num_wf=1)
