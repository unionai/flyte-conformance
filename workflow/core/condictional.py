import random

from flytekit import conditional, task, workflow


@task
def calculate_circle_circumference(radius: float) -> float:
    return 2 * 3.14 * radius  # Task to calculate the circumference of a circle


@task
def calculate_circle_area(radius: float) -> float:
    return 3.14 * radius * radius  # Task to calculate the area of a circle


@workflow
def shape_properties(radius: float = 2.0) -> float:
    return (
        conditional("shape_properties")
        .if_((radius >= 0.1) & (radius < 1.0))
        .then(calculate_circle_circumference(radius=radius))
        .else_()
        .then(calculate_circle_area(radius=radius))
    )


@workflow
def shape_properties_with_multiple_branches(radius: float = 2.0) -> float:
    return (
        conditional("shape_properties_with_multiple_branches")
        .if_((radius >= 0.1) & (radius < 1.0))
        .then(calculate_circle_circumference(radius=radius))
        .elif_((radius >= 1.0) & (radius <= 10.0))
        .then(calculate_circle_area(radius=radius))
        .else_()
        .fail("The input must be within the range of 0 to 10.")
    )


@workflow
def shape_properties_accept_conditional_output(radius: float = 2.0) -> float:
    result = (
        conditional("shape_properties_accept_conditional_output")
        .if_((radius >= 0.1) & (radius < 1.0))
        .then(calculate_circle_circumference(radius=radius))
        .elif_((radius >= 1.0) & (radius <= 10.0))
        .then(calculate_circle_area(radius=radius))
        .else_()
        .fail("The input must exist between 0 and 10.")
    )
    return calculate_circle_area(radius=result)


@task
def coin_toss(seed: int) -> bool:
    """
    Mimic a condition to verify the successful execution of an operation
    """
    r = random.Random(seed)
    if r.random() < 0.5:
        return True
    return False


@task
def failed() -> int:
    """
    Mimic a task that handles failure
    """
    return -1


@task
def success() -> int:
    """
    Mimic a task that handles success
    """
    return 0


@workflow
def boolean_wf(seed: int = 5) -> int:
    result = coin_toss(seed=seed)
    return (
        conditional("coin_toss")
        .if_(result.is_true())
        .then(success())
        .else_()
        .then(failed())
    )


@workflow
def boolean_input_wf(boolean_input: bool = True) -> int:
    return (
        conditional("boolean_input_conditional")
        .if_(boolean_input.is_true())
        .then(success())
        .else_()
        .then(failed())
    )


@workflow
def nested_conditions(radius: float = 2.0) -> float:
    return (
        conditional("nested_conditions")
        .if_((radius >= 0.1) & (radius < 1.0))
        .then(
            conditional("inner_nested_conditions")
            .if_(radius < 0.5)
            .then(calculate_circle_circumference(radius=radius))
            .elif_((radius >= 0.5) & (radius < 0.9))
            .then(calculate_circle_area(radius=radius))
            .else_()
            .fail("0.9 is an outlier.")
        )
        .elif_((radius >= 1.0) & (radius <= 10.0))
        .then(calculate_circle_area(radius=radius))
        .else_()
        .fail("The input must be within the range of 0 to 10.")
    )


@workflow
def consume_task_output(radius: float = 2.0, seed: int = 5) -> float:
    is_heads = coin_toss(seed=seed)
    return (
        conditional("double_or_square")
        .if_(is_heads.is_true())
        .then(calculate_circle_circumference(radius=radius))
        .else_()
        .then(calculate_circle_area(radius=radius))
    )
