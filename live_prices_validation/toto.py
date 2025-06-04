from enum import Enum


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