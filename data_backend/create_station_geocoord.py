from requests import Response
from read_carpark_api import extract_carpark
from typing import List, Dict, Any
import pandas as pd
import json


def create_geo_coord():
    # get a list of facility id
    # loop the facility id list, query api and find geo coordinates
    # write to coord dict

    df_station: pd.DataFrame = pd.read_parquet("data//station.parquet")

    fid: List[str] = df_station["facility_id"].to_list()

    locations = []

    for id in fid:
        response: Response = extract_carpark(id)

        if response.status_code != 200:
            continue

        rlt: Dict[str, Any] = json.loads(response.text)

        record: Dict[str, Any] = {
            "facility_id": id,
            "full_name": rlt["zones"][0]["zone_name"],
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

    df.to_parquet("data//station_geo.parquet")


if __name__ == "__main__":
    create_geo_coord()
