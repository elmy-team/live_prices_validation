from live_prices_validation.common_utils import create_adaptive_card, create_prices_table
from live_prices_validation.config import Config
import logging
from live_prices_validation.common_types import LivePrices
import requests
import json


class TeamsApiClient:
    def post_live_prices(
            self,
            team_name: str,
            channel_name: str,
            live_prices: LivePrices
        ):
        body_blocks = [create_prices_table(live_prices.prices, input_cells=False)]
        message_title = f"Prices at {live_prices.timestamp.format('HH[h]mm')}"
        payload = create_adaptive_card(
            team_name=team_name,
            channel_name=channel_name,
            body_blocks=body_blocks,
            issuer_name=message_title
        )

        return self._post_message(
            Config.TEAMS_WEBHOOK_POST,
            payload
        )


    @staticmethod
    def _post_message(webhook: str, payload):
        try:
            body = json.dumps(payload, separators=(",", ":"))
            headers = {"Content-type": "application/json"}
            response = requests.post(
                url=webhook,
                data=body,
                headers=headers
            )
            logging.info("Request status code: %s", response.status_code)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Invalid response code {response.status_code}")
        except Exception as e:
            print("Error Teams: ", e)
            return None
