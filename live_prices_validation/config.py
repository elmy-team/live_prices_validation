import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    THOT_BASE_URL: str
    THOT_API_KEY: str


def load_configuration() -> Config:
    return Config(
        THOT_BASE_URL=os.getenv("THOT_BASE_URL"),  # type: ignore
        THOT_API_KEY=os.getenv("THOT_API_KEY"),  # type: ignore
    )
