from dataclasses import dataclass
from enum import Enum
from typing import List, Mapping, Optional, Sequence

from pendulum import DateTime


JsonObject = Mapping[str, "JsonObject | str | int | bool | None | JsonArray"]
JsonArray = Sequence["JsonObject | str | int | bool | None"]
Json = JsonArray | JsonObject


@dataclass
class LivePrice:
    delivery: str
    bid: Optional[float] = float("nan")
    ask: Optional[float] = float("nan")
    price: Optional[float] = float("nan")
    last: Optional[float] = float("nan")


@dataclass
class LivePrices:
    timestamp: DateTime
    prices: List[LivePrice]


class Country(Enum):
    FR = "FR"
    DE = "DE"
    NL = "NL"


class Profile(Enum):
    BASELOAD = "BASELOAD"


class Commodity(Enum):
    POWER = "POWER"
    GAS = "GAS"
    EUA = "EUA"


class Granularity(Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    WEEKEND = "WEEKEND"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"