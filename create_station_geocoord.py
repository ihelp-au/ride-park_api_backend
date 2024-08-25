from requests import Response
from read_carpark_api import extract_carpark
from typing import List, Dict, Tuple
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

        rlt = json.loads(response.text)

        locations.append({**rlt["location"], "facility_id": id})

    df = pd.DataFrame(locations)
    df.to_parquet("data//station_geo.parquet")


if __name__ == "__main__":
    create_geo_coord()
