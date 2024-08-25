import time
from requests import Response
from read_carpark_api import extract_carpark
from typing import List, Dict, Tuple, Any
import pandas as pd
import json


def create_parkinglot():
    # create dataset containing facility_id, timestamp,
    # total car park lots, occupied car park lots and available
    # car park lots

    facility_ids: List[str] = pd.read_parquet("data//station.parquet")[
        "facility_id"
    ].to_list()

    records = []

    for id in facility_ids:
        response = extract_carpark(id)

        if response.status_code != 200:
            # keep updating the records but not overwrite;
            # some station infomration may not be returned,
            # keep the most recent records
            continue

        rlt: Dict[str, Any] = json.loads(response.text)
        # print(rlt)
        # total_lots =

        total: int = int(rlt["zones"][0]["spots"])
        occupied: int = int(rlt["occupancy"]["total"])
        available: int = total - occupied
        assert available >= 0

        timestamp = rlt["time"]

        records.append(
            {
                "facility_id": id,
                "total": total,
                "occupied": occupied,
                "available": available,
                "timestamp": timestamp,
            }
        )

        df = pd.DataFrame(records)
        df.to_parquet("data//parking_lots.parquet")


if __name__ == "__main__":
    create_parkinglot()
