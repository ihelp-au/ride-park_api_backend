"""
Fetch car park occupancy data;

API: https://api.transport.nsw.gov.au/v1/carpark

TOKEW: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI4WlZsMm5ENTdYYXVGLXJZSXRzUWYzNnhJdGdUUURSOHVzOHZWWGJYRUFRIiwiaWF0IjoxNzI0NDU3ODQ0fQ.MeUI_yOnPI3Tj5izgGGDP2DEvZmEoXb7eF56Ee_Bm7Y
"""

import json
from rich import print as pprint
from rich import print_json
from typing import Dict, Any
import pandas as pd
import requests

API = "https://api.transport.nsw.gov.au/v1/carpark"
NSW_TRANSPORT_OPEN_DATA_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI4WlZsMm5ENTdYYXVGLXJZSXRzUWYzNnhJdGdUUURSOHVzOHZWWGJYRUFRIiwiaWF0IjoxNzI0NDU3ODQ0fQ.MeUI_yOnPI3Tj5izgGGDP2DEvZmEoXb7eF56Ee_Bm7Y"


def extract_carpark(carpark: str = "") -> requests.Response:
    # df: pd.DataFrame = pd.read_json()
    head: dict[str, str] = {
        "Authorization": "apikey {}".format(NSW_TRANSPORT_OPEN_DATA_TOKEN)
    }

    api: str = f"{API}?facility={carpark}"
    # api = API

    response: requests.Response = requests.get(api, headers=head, timeout=20)

    return response


if __name__ == "__main__":
    # tsn id 213310 is not facility id. Not sure where is the mapping
    # between car park names and facility id

    while True:
        carpark: str = input("key in carpark facility ID, e.g. 6\n")
        response: requests.Response = extract_carpark(carpark)

        print_json(response.text)

        # parking_info: Dict[str, Any] = json.load(response.text)
        # df: pd.DataFrame = pd.read_json(response.text)
        # print(df)
