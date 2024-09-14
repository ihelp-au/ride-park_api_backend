# Create the station parking location dataset
# Columns includes facility_id, station name, latitude, longitude

"""
This module contains a function to create a parquet file with station locations.

The main function is create_carpark_location(), which fetches station information
including facility IDs and station names using the NSW Transport Open Data API,
and saves the processed results to a new parquet file.

The station information includes:
- facility_id: the unique identifier for the station
- station_name: the name of the station

The output file path is hardcoded as "data//station.parquet".
"""

import json
import pandas as pd
from read_carpark_api import extract_station_list


def create_carpark_list() -> None:
    carparks = extract_station_list()
    # print(carparks.text)

    df: pd.DataFrame = pd.DataFrame(
        json.loads(carparks.text), index=[0]).melt()

    df: pd.DataFrame = df.rename(
        columns={"variable": "facility_id", "value": "station_name"}
    )

    df.to_parquet("data//station.parquet")


if __name__ == "__main__":
    create_carpark_list()
