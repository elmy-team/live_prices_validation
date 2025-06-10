from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional, Sequence


JsonObject = Mapping[str, "JsonObject | str | int | bool | None | JsonArray"]
JsonArray = Sequence["JsonObject | str | int | bool | None"]
Json = JsonArray | JsonObject


@dataclass
class LivePrice:
    bid: float
    ask: float
    price: float
    delivery: str
    last: Optional[float] = float("nan")


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