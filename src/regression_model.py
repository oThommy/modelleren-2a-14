import pandas as pd
from typing import TypeVar
import numpy as np
import numpy.typing as npt
from sklearn.preprocessing import PolynomialFeatures
import statsmodels.api as sm

battery_data = pd.read_csv('../data/battery_train.csv')

POLYNOMIAL_DEGREE = 3

capacity_points = np.array([])
RUL_points = np.array([])

# Extract (capacity, RUL) points (over all cycles) for every battery into (capacity_points, RUL_points)
for column in battery_data:
    if column == 'Cycle':
        continue

    capacities = battery_data[column].dropna()
    total_useful_life = len(capacities)
    RULs = np.arange(total_useful_life - 1, -1, -1) # The first measured capacity corresponds to an RUL of total_useful_life - 1 as the battery has already consumed a cycle of its life
    capacity_points = np.concatenate((capacity_points, capacities))
    RUL_points = np.concatenate((RUL_points, RULs))

capacity_points = capacity_points.reshape((-1, 1))
transformer = PolynomialFeatures(degree=POLYNOMIAL_DEGREE, include_bias=True) # Set include_bias=True to add a column of 1s to the array, such that the polynomial model becomes: Y = β_0 * 1 + β_1 * x^1 + ... + β_p * x^p + e. This column of 1s represents the intercept term β_0
x = transformer.fit_transform(capacity_points)
y = RUL_points
model = sm.OLS(y, x).fit()

def forecast_RULs(capacities: npt.ArrayLike) -> np.ndarray:
    '''
    Forecast RULs of batteries using the polynomial regression model.

    :param capacities: array-like of shape (n_capacities, 1)
    :returns RUL_preds: ndarray with forecasted RULs, corresponding to the provided capacities
    '''
    transformed_capacities = np.array(capacities).reshape((-1, 1))
    x = transformer.fit_transform(transformed_capacities)
    RUL_preds = model.predict(x)
    return RUL_preds

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

# Prolly convert into one function with overloads