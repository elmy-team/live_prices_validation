from live_prices_validation.config import load_configuration
from live_prices_validation.connectors.teams_connector import TeamsApiClient
from live_prices_validation.connectors.thot_connector import ThotApiClient


def main():
    config = load_configuration()

    # Retrieve prices from Thot API
    thot_connector = ThotApiClient(config.THOT_BASE_URL, config.THOT_API_KEY)
    prices = thot_connector.get_live_prices()
    if not prices:
        print("Routine failed")
        return

    # Send prices to Teams Power Automate and post prices in channel
    teams_connector = TeamsApiClient(config.TEAMS_POWER_AUTOMATE_WEBHOOK)
    updated_prices = teams_connector.post_live_prices(prices)
    if updated_prices is None:
        print("Routine failed")
        return

    print(updated_prices)

if __name__ == "__main__":
    main()