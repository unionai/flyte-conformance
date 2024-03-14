from flytekit import task, workflow

@task
def t0():
    print("Running t0")
    return


@task
def t1():
    print("Running t1")
    return


@task
def t2():
    print("Running t2")
    return


@workflow
def chain_tasks_wf():
    t2_promise = t2()
    t1_promise = t1()
    t0_promise = t0()

    t0_promise >> t1_promise
    t1_promise >> t2_promise
