from copy import deepcopy
import logging
from typing import List, cast
from live_prices_validation.common_exception import TimedOut
from live_prices_validation.common_types import JsonArray, JsonObject, LivePrice
import requests
import json


class TeamsApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def post_live_prices(self, live_prices: List[LivePrice]):
        body_blocks = [self._json_table(live_prices)]

        try:
            payload = self._create_adaptive_card("Gyptis", "[DEV] Power Automate test", body_blocks, "Live Price Validation")
            body = json.dumps(payload, separators=(",", ":"))
            headers = {"Content-type": "application/json"}
            response = requests.post(
                url=self.base_url,
                data=body,
                headers=headers
            )
            logging.info("Request status code: %s", response.status_code)
            if response.status_code == 200:
                return self._convert_data_to_live_prices(response.json()["body"])
            elif response.status_code == 408:
                raise TimedOut("Adaptive card timed-out")
            else:
                raise Exception(f"Invalid response code {response.status_code}")
        except Exception as e:
            print("Error Teams: ", e)
            return None


    @staticmethod
    def _convert_data_to_live_prices(data) -> List[LivePrice]:
        prices: List[LivePrice] = []

        del data['adaptive_card_id'] # We don't need the adaptive card's Id
        for key, value in data.items():
            delivery, price_type = key.split("_")[:2]
            price_index = next((i for i, price in enumerate(prices) if price.delivery == delivery), None)
            if price_index is None:
                prices.append(LivePrice(delivery=delivery))
                setattr(prices[-1], price_type, value)
            else:
                setattr(prices[price_index], price_type, value)
        return prices


    @staticmethod
    def _json_table_cell_text(
        value: str,
    ) -> JsonObject:
        return {
            "type": "TableCell",
            "items": [{"type": "TextBlock", "text": value}],
        }
    

    @staticmethod
    def _json_table_cell_input(
        id: str,
        value: float,
    ) -> JsonObject:
        return {
            "type": "TableCell",
            "items": [{
                "type": "Input.Number",
                "id": id,
                "value": value
            }],
        }


    def _json_table(
        self,
        live_prices: List[LivePrice]
    ) -> JsonObject:
        json_table: JsonObject = {
            "type": "Table",
            "columns": cast(JsonArray, []),
            "rows": cast(JsonArray, []),
        }
        json_table_row: JsonObject = {"type": "TableRow", "cells": cast(JsonArray, [])}

        # Add headers to the table
        header_row_index = 0
        headers = ["delivery", "bid", "ask", "lastp", "mid"]
        json_table["rows"].append(deepcopy(json_table_row))
        for i, header in enumerate(headers):
            json_table["columns"].append({"width": 1})
            json_table["rows"][header_row_index]["cells"].append(
                self._json_table_cell_text(header)
            )

        # Add rows to the table
        for live_price_index, live_price in enumerate(live_prices):
            json_table["rows"].append(deepcopy(json_table_row))
            # We skip the header row
            json_table["rows"][live_price_index + 1]["cells"].extend(
                [
                    self._json_table_cell_text(live_price.delivery),
                    self._json_table_cell_input(f"{live_price.delivery}_bid", live_price.bid),
                    self._json_table_cell_input(f"{live_price.delivery}_ask", live_price.ask),
                    self._json_table_cell_input(f"{live_price.delivery}_last", live_price.last),
                    self._json_table_cell_input(f"{live_price.delivery}_price", live_price.price),
                ]
            )
        return json_table


    @staticmethod
    def _create_adaptive_card(
        team_name: str,
        channel_name: str,
        body_blocks: JsonArray,
        issuer_name: str | None = None,
    ) -> JsonObject:
        attachment: JsonObject = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "contentUrl": None,
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.5",
                "body": [
                    {
                        "type": "FactSet",
                        "facts": [
                            {"title": "team_name", "value": team_name},
                            {"title": "channel_name", "value": channel_name},
                            {"title": "issuer_name", "value": issuer_name} if issuer_name else None,
                        ],
                        "isVisible": False,
                    },
                    *body_blocks,
                ],
                "msteams": {"width": "Full"},
            },
        }
        return {
            "type": "message",
            "attachments": [attachment],
        }
