import base64
from copy import deepcopy
from typing import List, cast

from live_prices_validation.common_types import JsonArray, JsonObject, LivePrice
from pendulum import DateTime
import pendulum


def generate_random_id():
    utc_now = pendulum.now().isoformat()
    return base64.b64encode(utc_now.encode('utf-8')).decode('utf-8')


def convert_data_to_live_prices(data) -> List[LivePrice]:
    prices: List[LivePrice] = []

    for key, value in data.items():
        delivery, price_type = key.split("_")[:2]
        price_index = next((i for i, price in enumerate(prices) if price.delivery == delivery), None)
        if price_index is None:
            prices.append(LivePrice(delivery=delivery))
            setattr(prices[-1], price_type, value)
        else:
            setattr(prices[price_index], price_type, value)
    
    return prices


def create_adaptive_card(
    team_name: str,
    channel_name: str,
    body_blocks: JsonArray,
    issuer_name: str | None = None,
    issuer_name_url: str | None  = None,
    timestamp: DateTime | None = None,
    adaptive_card_id: str | None = None
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
                    "facts": list(filter(None, [
                        {"title": "team_name", "value": team_name},
                        {"title": "channel_name", "value": channel_name},
                        {"title": "issuer_name", "value": issuer_name} if issuer_name else None,
                        {"title": "issuer_name_url", "value": issuer_name_url} if issuer_name_url else None,
                        {"title": "timestamp", "value": timestamp.isoformat()} if timestamp else None,
                        {"title": "adaptive_card_id", "value": adaptive_card_id} if adaptive_card_id else None,
                    ])),
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


def create_prices_table(
    prices: List[LivePrice],
    input_cells: bool = False
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
            live_price_cell_text(header)
        )

    # Add rows to the table
    for live_price_index, live_price in enumerate(prices):
        json_table["rows"].append(deepcopy(json_table_row))
        # We skip the header row
        json_table["rows"][live_price_index + 1]["cells"].extend(
            [
                live_price_cell_text(live_price.delivery),
                live_price_cell_input(f"{live_price.delivery}_bid", live_price.bid),
                live_price_cell_input(f"{live_price.delivery}_ask", live_price.ask),
                live_price_cell_input(f"{live_price.delivery}_last", live_price.last),
                live_price_cell_input(f"{live_price.delivery}_price", live_price.price),
            ] if input_cells else
            [
                live_price_cell_text(live_price.delivery),
                live_price_cell_text(live_price.bid),
                live_price_cell_text(live_price.ask),
                live_price_cell_text(live_price.last),
                live_price_cell_text(live_price.price),
            ]
        )
    return json_table


def live_price_cell_text(
    value: str,
) -> JsonObject:
    return {
        "type": "TableCell",
        "items": [{
            "type": "TextBlock",
            "text": value
        }],
    }


def live_price_cell_input(
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