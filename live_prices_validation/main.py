from live_prices_validation.common_types import LivePrice
from live_prices_validation.config import Config
from live_prices_validation.connectors.teams_connector import TeamsApiClient
from live_prices_validation.connectors.thot_connector import ThotApiClient


def main():
    # Retrieve Live Prices from Thot API
    thot_connector = ThotApiClient(Config.THOT_BASE_URL, Config.THOT_API_KEY)
    prices = thot_connector.get_live_prices()
    if not prices:
        print("Routine failed")
        return
    
    # prices = [LivePrice(delivery="Q03-2025", ask=45.7, bid=45.8, last=34.9, price=56.2)]


    # Post editable Live Prices in Teams and wait for a response
    teams_connector = TeamsApiClient()
    response = teams_connector.post_and_wait_live_prices(
        Config.TEAMS_TEAM_NAME_POST_AND_WAIT,
        Config.TEAMS_CHANNEL_NAME_POST_AND_WAIT,
        prices
    )
    if response is None:
        print("Routine failed")
        return

    # Convert Teams' response back to Live Prices
    updated_prices = teams_connector.convert_data_to_live_prices(response["body"])

    # Post non-editable Live Prices in Teams
    response = teams_connector.post_live_prices(
        Config.TEAMS_TEAM_NAME_POST,
        Config.TEAMS_CHANNEL_NAME_POST,
        updated_prices,
    )
    if response is None:
        print("Routine failed")
        return

    print("Routine succeeded")

if __name__ == "__main__":
    main()