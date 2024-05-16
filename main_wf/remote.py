from flytekit.remote import FlyteRemote
from flytekit.configuration import Config, ImageConfig
from wf.dummy_tasks import wf
from flytekit.configuration import SerializationSettings, FastSerializationSettings


remote = FlyteRemote(config=Config.auto(), default_project="flytesnacks", default_domain="development")

_, native_url = remote.fast_package(root=".")

flyte_workflow = remote.register_workflow(
    entity=wf,
    serialization_settings=SerializationSettings(
        image_config=ImageConfig.auto(img_name="ghcr.io/flyteorg/flytekit:l6c_k957io8qqbcgcsrmdw"),
        project="flytesnacks",
        domain="development",
        version="v2",
        fast_serialization_settings=FastSerializationSettings(enabled=True, destination_dir=".", distribution_location=native_url),
    ),
)
