import numpy as np
import numpy.typing as npt
import pandas as pd
from typing import Callable, TypeVar
from dataclasses import dataclass
import config
from pathlib import Path
from typing_extensions import Self


_T = TypeVar('_T')
_MathTransformFunction = Callable[[_T], _T]

class MathTransformer:
    def __init__(self, transform: _MathTransformFunction, inverse_transform: _MathTransformFunction):
        self.__transform = transform
        self.__inverse_transform = inverse_transform

    # Proxy functions because Pyright can't infer the returntype of lambdas
    def transform(self, x: _T, /) -> _T:
        return self.__transform(x)

    def inverse_transform(self, x: _T, /) -> _T:
        return self.__inverse_transform(x)

log_transformer = MathTransformer(lambda x: np.log(x + 1), lambda x: np.exp(x) - 1)

@dataclass(frozen=True)
class BatteryData:
    raw: pd.DataFrame
    transformed: pd.DataFrame
    logged: pd.DataFrame
    
    @classmethod
    def from_csv(cls, path: Path) -> Self:
        raw = pd.read_csv(path)
        raw.set_index('Cycle', inplace=True)
        raw.index.names = ['cycle']
        raw.columns = [battery_name.split('.')[1] for battery_name in raw.columns]

        # Transform (cycle, capacity) for every battery into (capacity, RUL)
        transformed = pd.DataFrame(columns=['capacity', 'RUL', 'battery_index'])
        for battery_index in raw:
            capacities = raw[battery_index].dropna()
            total_useful_life = len(capacities)
            RULs = np.arange(total_useful_life - 1, -1, -1) # The first measured capacity corresponds to an RUL of total_useful_life - 1 as the battery has already consumed a cycle of its life
            transformed_new = pd.DataFrame({'capacity': capacities, 'RUL': RULs, 'battery_index': battery_index})
            transformed = pd.concat([transformed, transformed_new])

        logged = transformed.copy()
        logged['RUL'] = logged['RUL'].map(log_transformer.transform)

        return cls(raw, transformed, logged)

test = BatteryData.from_csv(config.DATA_DIR / 'battery_test.csv')
train = BatteryData.from_csv(config.DATA_DIR / 'battery_train.csv')
