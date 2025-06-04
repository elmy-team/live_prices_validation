from typing import List, Optional
import requests
from dataclasses import dataclass
import pendulum
import logging
import pandas as pd

from live_prices_validation.toto import Country, Commodity, Profile, Granularity
from live_prices_validation.config import load_configuration

@dataclass
class LivePriceParams:
    country: Country
    commodity: Commodity
    profile: Profile
    granularity: Granularity
    publication_time_from: pendulum.DateTime
    publication_time_to: pendulum.DateTime
    period_start_time_from: pendulum.DateTime
    period_start_time_to: pendulum.DateTime
    delivery: str

@dataclass
class LivePrice:
    bid: float
    ask: float
    price: float
    delivery: str
    last: Optional[float] = float("nan")

class ThotApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def get_live_price(self, params: LivePriceParams) -> Optional[pd.DataFrame]:
        try:
            url = f"{self.base_url}/commodity/live/price"
            logging.info("Try requesting %s with parameters %s", url, params.__dict__)
            response = requests.get(url, params={
                "api_key": self.api_key,
                **params.__dict__
            }, timeout=600)
            logging.info("Request status code: %s", response.status_code)
            if response.status_code == 200:
                return pd.DataFrame(response.json()["data"])
            else:
                raise Exception("Invalid response code")
        except Exception as e:
            print(e)
        return None


def convert_to_live_price(response: pd.DataFrame) -> LivePrice:
    return LivePrice(
        bid=float(response["bid"][0]),
        ask=float(response["ask"][0]),
        last=float("nan" if response["last"][0] is None else response["last"][0]),
        price=float(response["price"][0]),
        delivery=response["delivery"][0]
    )

def get_live_prices(thot_connector: ThotApiClient) -> List[LivePrice]:
    prices = []
    
    today_date = pendulum.yesterday().at(9) # Today at 9AM
    year_date = pendulum.now().start_of("year")
    params = {
        "country": Country.FR.value,
        "commodity": Commodity.POWER.value,
        "profile": Profile.BASELOAD.value,
        "publication_time_from": today_date.to_iso8601_string(),
        "publication_time_to": today_date.add(hours=1).to_iso8601_string(), # Today at 10AM
        "period_start_time_from": year_date.to_iso8601_string(),
        "period_start_time_to": year_date.add(years=4).to_iso8601_string(),
    }

    prices.append(
        convert_to_live_price(
            thot_connector.get_live_price(LivePriceParams(
                granularity="QUARTERLY",
                delivery="Q04-2025",
                **params
            ))
        )
    )
    return prices

    

def main():
    config = load_configuration()

    thot_connector = ThotApiClient(config.THOT_BASE_URL, config.THOT_API_KEY)
    prices = get_live_prices(thot_connector)
    print(prices)


if __name__ == "__main__":
    main()