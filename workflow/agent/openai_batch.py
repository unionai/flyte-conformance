from typing import Iterator

from flytekit import Secret, workflow
from flytekit.types.file import JSONLFile
from flytekit.types.iterator import JSON
from flytekitplugins.openai import BatchResult, create_batch


def jsons():
    for x in [
        {
            "custom_id": "request-1",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What is 2+2?"},
                ],
            },
        },
    ]:
        yield x


it_batch = create_batch(
    name="gpt-3.5-turbo",
    secret=Secret(group="openai", key="1"),
)

file_batch = create_batch(
    name="gpt-3.5-turbo",
    secret=Secret(group="openai", key="1"),
    is_json_iterator=False,
)


@workflow
def json_iterator_wf(json_vals: Iterator[JSON] = jsons()) -> BatchResult:
    return it_batch(jsonl_in=json_vals)


@workflow
def jsonl_wf(jsonl_file: JSONLFile = "data.jsonl") -> BatchResult:
    return file_batch(jsonl_in=jsonl_file)
