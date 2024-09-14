"""
This module contains a function to create a parquet file with station geocoordinates.

The main function is create_station_geocoord(), which fetches station information
including facility IDs, station names, latitude, and longitude using the NSW Transport Open Data API,
and saves the processed results to a new parquet file.

The station information includes:
- facility_id: the unique identifier for the station
- station_name: the name of the station
- latitude: the latitude of the station
- longitude: the longitude of the station

The output file path is hardcoded as "data/station_geocoord.parquet".
"""

import os
import json
import pandas as pd
from requests import Response
from read_carpark_api import extract_carpark_info
from typing import List, Dict, Any
from rich import print as pprint


def create_station_geocoord(
    input_station_file: str = "data//station.parquet",
    output_geo_file: str = "data//station_geo.parquet",
) -> None:
    """
    create geographical coordinates parquet file for stations.

    schema:

    facilit_id: str
    full_name: str
    short_name: str
    address: str
    latitude: float
    longitude: float
    """
    # get a list of facility id
    # loop the facility id list, query api and find geo coordinates
    # write to coord dict

    assert os.path.exists(input_station_file)

    df_station: pd.DataFrame = pd.read_parquet(input_station_file)

    fid: List[str] = df_station["facility_id"].to_list()

    locations: list[Any] = []

    for id in fid:
        response: Response = extract_carpark_info(id)

        if response.status_code != 200:
            print(f"facility id {id} does not reutrn parking information")
            continue

        rlt: Dict[str, Any] = json.loads(response.text)

        record: Dict[str, Any] = {
            "facility_id": id,
            # full_name does not make sense
            "full_name": rlt["facility_name"],
            "short_name": rlt["location"]["suburb"],
            "address": rlt["location"]["address"],
            "latitude": rlt["location"]["latitude"],
            "longitude": rlt["location"]["longitude"],
        }
        locations.append(record)

    df = pd.DataFrame(locations)

    # Convert latitude and longitude to float
    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)
    df.to_parquet(output_geo_file)


if __name__ == "__main__":
    pprint("Please run this script from project root directory")
    create_station_geocoord()
    pprint("data//station_geo.parquet is generated")
