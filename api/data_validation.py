"""Модуль с классом-валидатором входящих на модель данных."""

from pydantic.dataclasses import dataclass
from pydantic import BaseModel


# @dataclass
class SimplePredictionModelFeatures(BaseModel):
    stock_name: str


if __name__ == '__main__':
    features = SimplePredictionModelFeatures(stock_name='APPL')

    print(features)