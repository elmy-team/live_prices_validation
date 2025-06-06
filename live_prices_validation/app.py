from live_prices_validation.connectors.teams_connector import TeamsApiClient
from live_prices_validation.connectors.thot_connector import ThotApiClient
from live_prices_validation.config import load_configuration

def main():
    config = load_configuration()

    thot_connector = ThotApiClient(config.THOT_BASE_URL, config.THOT_API_KEY)
    prices = thot_connector.get_live_prices()
    teams_connector = TeamsApiClient(config.TEAMS_POWER_AUTOMATE_WEBHOOK)
    teams_connector.post_live_prices(prices)


if __name__ == "__main__":
    main()