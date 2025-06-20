from flask import request
from live_prices_validation.common_types import LivePrices
from live_prices_validation.common_utils import convert_data_to_live_prices
from live_prices_validation.config import Config
from live_prices_validation.connectors.teams_connector import TeamsApiClient
import pendulum

from . import api


@api.route('/validate_prices', methods=['POST'])
def validate_prices():
    data = request.get_json()

    # Convert Teams' response back to Live Prices
    live_prices = LivePrices(
        timestamp=pendulum.parse(data.get("timestamp")),
        prices=convert_data_to_live_prices(data.get("prices"))
    )

    # Post non-editable Live Prices in Teams
    teams_connector = TeamsApiClient()
    response = teams_connector.post_live_prices(
        Config.TEAMS_TEAM_NAME_POST,
        Config.TEAMS_CHANNEL_NAME_POST,
        live_prices,
    )
    if response is None:
        return 'Error: Teams post live prices', 500
    return 'Ok', 200