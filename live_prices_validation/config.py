import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    THOT_BASE_URL: str
    THOT_API_KEY: str
    TEAMS_POWER_AUTOMATE_WEBHOOK: str


def load_configuration() -> Config:
    return Config(
        THOT_BASE_URL=os.getenv("THOT_BASE_URL"),  # type: ignore
        THOT_API_KEY=os.getenv("THOT_API_KEY"),  # type: ignore
        TEAMS_POWER_AUTOMATE_WEBHOOK=os.getenv("TEAMS_POWER_AUTOMATE_WEBHOOK"),  # type: ignore
    )
