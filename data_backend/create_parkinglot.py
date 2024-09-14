"""
This module contains functions to create and update parking lot information for stations.

The main function is create_parkinglot(), which reads station IDs from a parquet file,
fetches parking lot information for each station using the NSW Transport Open Data API,
and saves the processed results to a new parquet file.

The parking lot information includes:
- facility_id: the unique identifier for the station
- timestamp: the timestamp when the data was retrieved
- total: total number of parking spots
- occupied: number of occupied parking spots
- available: number of available parking spots

It also saves the raw JSON responses for each station in a separate directory for debugging
and further analysis if needed.
"""


import json
import os
from typing import List, Dict, Any
import pandas as pd
from requests import Response
from read_carpark_api import extract_carpark_info
from rich import print as pprint


def create_parkinglot(
    station_filename: str = "data//station.parquet",
    stationinfo_json_dir: str = "data",
    output_stationinfo_filename: str = "data//parking_lots.parquet",
) -> None:
    """create dataset containing facility_id, timestamp,
    total car park lots, occupied car park lots and available
    car park lots
    """

    assert os.path.exists(
        station_filename
    ), f"Input data file {station_filename} not found"

    facility_ids: List[str] = pd.read_parquet(
        station_filename)["facility_id"].to_list()

    records: List[Any] = []

    for id in facility_ids:
        response: Response = extract_carpark_info(id)

        if response.status_code != 200:
            # keep updating the records but not overwrite;
            # some station infomration may not be returned,
            # keep the most recent records
            continue

        rlt: Dict[str, Any] = json.loads(response.text)

        processed_rlt: dict[str, Any] = {}

        # clean zones - remove zone with loop as null
        rlt["zones"] = [zone for zone in rlt["zones"] if zone["zone_name"] != ""]

        total: int = int(rlt["spots"])
        occupied: int = int(rlt["occupancy"]["total"])
        available: int = total - occupied
        timestamp: str = rlt["MessageDate"]
        zones: str = json.dumps(rlt["zones"])

        processed_rlt = {
            "facility_id": id,
            "total": total,
            "occupied": occupied,
            "available": available,
            "timestamp": timestamp,
            # to read json file into polars dataframe, make column
            # zones data type as str; The cost is, the generated json file
            # could not be read by json.load() but could be consumed by
            # pl.read_json()
            "zones": zones,
        }
        # dump processed station info to json file
        with open(f"{stationinfo_json_dir}//{id}.json", "w", encoding="utf-8") as f:
            json.dump(processed_rlt, f)

        records.append(
            {
                "facility_id": id,
                "total": total,
                "occupied": occupied,
                "available": available,
                "timestamp": timestamp,
                "zones": zones,
            }
        )

    df = pd.DataFrame(records)
    df.to_parquet(output_stationinfo_filename)


if __name__ == "__main__":
    pprint("Please run the script from project root directory")
    create_parkinglot()
    pprint("Parking lots JSON files are saved in the data directory")
