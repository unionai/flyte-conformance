from flytekit import workflow, task


@task
def t1():
    with open("/root/test", "wb") as f:
        f.write("Flyte is great!".encode() * 3000000)


@workflow
def ephemeral_storage_test():
    t1()
