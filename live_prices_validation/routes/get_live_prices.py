from flask import jsonify
from live_prices_validation.common_utils import create_adaptive_card, create_prices_table, generate_random_id
from live_prices_validation.config import Config
from live_prices_validation.connectors.thot_connector import ThotApiClient
from . import api


@api.route('/get_live_prices', methods=['GET'])
def get_live_prices():
    thot_connector = ThotApiClient(Config.THOT_BASE_URL, Config.THOT_API_KEY)
    
    # Retrieve Live Prices from Thot API
    live_prices = thot_connector.get_live_prices()
    if not live_prices:
        print("Routine failed")
        return

    # Only for testing purposes
    # live_prices = [LivePrice(delivery="Q03-2025", ask=45.7, bid=45.8, last=34.9, price=56.2)]

    # Format prices as editable adaptive card table
    body_blocks = [create_prices_table(live_prices.prices, input_cells=True)]
    message_title = f"Prices at {live_prices.timestamp.format('HH[h]mm')}"
    adaptive_card = create_adaptive_card(
        team_name=Config.TEAMS_TEAM_NAME_POST_AND_WAIT,
        channel_name=Config.TEAMS_CHANNEL_NAME_POST_AND_WAIT,
        body_blocks=body_blocks,
        issuer_name=message_title,
        timestamp=live_prices.timestamp,
        adaptive_card_id=generate_random_id()
    )
    return jsonify(adaptive_card)