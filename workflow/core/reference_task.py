from flytekit import reference_task, workflow


@reference_task(
    project="flyte-conformance",
    domain="development",
    name="flytesnacks.examples.advanced_composition.advanced_composition.conditional.coin_toss",
    version="iTMAMwb_Zq3RUScvoyFH0w",
)
def t1(seed: int) -> bool:
    ...


@workflow
def wf():
    t1(seed=1)
