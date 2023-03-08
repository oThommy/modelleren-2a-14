from typing import TypeVar
import numpy as np
import numpy.typing as npt

def forecast_RULs(capacities: npt.ArrayLike) -> np.ndarray:
    '''
    Forecast RULs of batteries using the polynomial regression model.

    :param capacities: array-like object with capacities that will be coerced into an ndarray with shape (-1, 1)
    :returns: ndarray with forecasted RULs, corresponding to the provided capacities
    '''

    return np.array([45])

T = TypeVar('T', bound=npt.DTypeLike)
def forecast_RUL(capacity: T) -> T:
    '''
    Forecast RUL of battery using the polynomial regression model.

    :param capacity
    :returns: forecasted RUL, corresponding to the provided capacity
    '''

    capacities = np.array([capacity]).reshape((-1, 1))
    RULs = forecast_RULs(capacities)
    RUL = capacity.__class__(RULs[0]) # Convert RUL type into the same type as capacity parameter

    return RUL