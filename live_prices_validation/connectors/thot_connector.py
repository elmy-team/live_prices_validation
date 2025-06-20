from typing import List, Optional
from live_prices_validation.config import Config
import requests
from dataclasses import dataclass
import pendulum
import logging
import pandas as pd

from live_prices_validation.common_types import Country, Commodity, LivePrice, LivePrices, Profile, Granularity

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

class ThotApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key

    def get_live_prices(self) -> LivePrices:
        prices: List[LivePrice] = []
        
        year_date = pendulum.now().start_of("year")
        params = {
            "country": Country.FR.value,
            "commodity": Commodity.POWER.value,
            "profile": Profile.BASELOAD.value,
            "publication_time_from": pendulum.today().at(9).to_iso8601_string(), # Today at 9AM
            "publication_time_to": pendulum.now().to_iso8601_string(), # Now
            "period_start_time_from": year_date.to_iso8601_string(), # Start of current year
            "period_start_time_to": year_date.add(years=4).to_iso8601_string(), # Start of year+4
        }
        deliveries = [
            {"granularity": "QUARTERLY", "delivery": f"Q01-{year_date.year}"},
            {"granularity": "QUARTERLY", "delivery": f"Q02-{year_date.year}"},
            {"granularity": "QUARTERLY", "delivery": f"Q03-{year_date.year}"},
            {"granularity": "QUARTERLY", "delivery": f"Q04-{year_date.year}"},
            {"granularity": "YEARLY", "delivery": f"Y-{year_date.add(years=1).year}"},
            {"granularity": "YEARLY", "delivery": f"Y-{year_date.add(years=2).year}"},
            {"granularity": "YEARLY", "delivery": f"Y-{year_date.add(years=3).year}"},
        ]

        timestamp = None
        for delivery in deliveries:
            price = self.get_live_price(LivePriceParams(
                granularity=delivery["granularity"],
                delivery=delivery["delivery"],
                **params
            ))
            if price is not None and not price.empty:
                # We retrieve only the most recent price which is at the end of the dataframe
                price = price.iloc[-1]

                if timestamp is None:
                    timestamp = pendulum.parse(price["publication_time"])
                prices.append(self.convert_to_live_price(price))

        return LivePrices(timestamp, prices)


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
                raise Exception(f"Invalid response code {response.status_code}")
        except Exception as e:
            print("Error Thot: ", e)
            return None


    @staticmethod
    def convert_to_live_price(response: pd.DataFrame) -> LivePrice:
        return LivePrice(
            delivery=response["delivery"],
            bid=float(response["bid"]),
            ask=float(response["ask"]),
            last=float("nan" if response["last"] is None else response["last"]),
            price=float(response["price"])
        )


# Used as a debug script
def main():
    thot_connector = ThotApiClient(Config.THOT_BASE_URL, Config.THOT_API_KEY)
    prices = thot_connector.get_live_prices()
    print(prices)


if __name__ == "__main__":
    main()