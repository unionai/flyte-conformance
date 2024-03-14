from typing import Tuple

from flytekit import workflow, task


@task
def slope(x: list[int], y: list[int]) -> float:
    sum_xy = sum([x[i] * y[i] for i in range(len(x))])
    sum_x_squared = sum([x[i] ** 2 for i in range(len(x))])
    n = len(x)
    return (n * sum_xy - sum(x) * sum(y)) / (n * sum_x_squared - sum(x) ** 2)


@task
def intercept(x: list[int], y: list[int], slope: float) -> float:
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    intercept = mean_y - slope * mean_x
    return intercept


@workflow
def sphinx_docstring_wf(
    x: list[int] = [-3, 0, 3], y: list[int] = [7, 4, -2]
) -> Tuple[float, float]:
    """
    Slope and intercept of a regression line

    This workflow accepts a list of coefficient pairs for a regression line.
    It calculates both the slope and intercept of the regression line.

    :param x: List of x-coefficients
    :param y: List of y-coefficients
    :return: Slope and intercept values
    """
    slope_value = slope(x=x, y=y)
    intercept_value = intercept(x=x, y=y, slope=slope_value)
    return slope_value, intercept_value


@workflow
def numpy_docstring_wf(
    x: list[int] = [-3, 0, 3], y: list[int] = [7, 4, -2]
) -> Tuple[float, float]:
    """
    Slope and intercept of a regression line

    This workflow accepts a list of coefficient pairs for a regression line.
    It calculates both the slope and intercept of the regression line.

    Parameters
    ----------
    x : list[int]
        List of x-coefficients
    y : list[int]
        List of y-coefficients

    Returns
    -------
    out : Tuple[float, float]
        Slope and intercept values
    """
    slope_value = slope(x=x, y=y)
    intercept_value = intercept(x=x, y=y, slope=slope_value)
    return slope_value, intercept_value


@workflow
def google_docstring_wf(
    x: list[int] = [-3, 0, 3], y: list[int] = [7, 4, -2]
) -> Tuple[float, float]:
    """
    Slope and intercept of a regression line

    This workflow accepts a list of coefficient pairs for a regression line.
    It calculates both the slope and intercept of the regression line.

    Args:
      x (list[int]): List of x-coefficients
      y (list[int]): List of y-coefficients

    Returns:
      Tuple[float, float]: Slope and intercept values
    """
    slope_value = slope(x=x, y=y)
    intercept_value = intercept(x=x, y=y, slope=slope_value)
    return slope_value, intercept_value
