import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    THOT_BASE_URL = os.getenv("THOT_BASE_URL")
    THOT_API_KEY = os.getenv("THOT_API_KEY")
    TEAMS_WEBHOOK_POST = os.getenv("TEAMS_WEBHOOK_POST")
    TEAMS_TEAM_NAME_POST = os.getenv("TEAMS_TEAM_NAME_POST")
    TEAMS_TEAM_NAME_POST_AND_WAIT = os.getenv("TEAMS_TEAM_NAME_POST_AND_WAIT")
    TEAMS_CHANNEL_NAME_POST = os.getenv("TEAMS_CHANNEL_NAME_POST")
    TEAMS_CHANNEL_NAME_POST_AND_WAIT = os.getenv("TEAMS_CHANNEL_NAME_POST_AND_WAIT")