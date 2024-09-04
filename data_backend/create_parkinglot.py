from requests import Response
from read_carpark_api import extract_carpark
from typing import List, Dict, Any
import pandas as pd
import json


def create_parkinglot() -> None:
    # create dataset containing facility_id, timestamp,
    # total car park lots, occupied car park lots and available
    # car park lots

    facility_ids: List[str] = pd.read_parquet("data//station.parquet")[
        "facility_id"
    ].to_list()

    records = []

    for id in facility_ids:
        response: Response = extract_carpark(id)

        if response.status_code != 200:
            # keep updating the records but not overwrite;
            # some station infomration may not be returned,
            # keep the most recent records
            continue

        rlt: Dict[str, Any] = json.loads(response.text)

        processed_rlt: dict[str, Any] = {}

        # clean zones - remove zone with loop as null
        rlt["zones"] = [zone for zone in rlt["zones"] if zone["zone_name"] != ""]

        # load to json file
        # with open(f'data//{id}.json', 'w', encoding='utf-8') as f:
        #     json.dump(rlt, f)

        # TODO: iterate zones to find total spots
        total: int = int(rlt["spots"])
        occupied: int = int(rlt["occupancy"]["total"])
        available: int = total - occupied
        timestamp: str = rlt["MessageDate"]
        zones: str = json.dumps(rlt["zones"])

        # timestamp: str = rlt['time']
        # assert available >= 0, f"{id} with available as {available}"

        # timestamp: int | None = int(
        #     rlt["time"]) if rlt['time'] is not None else None

        processed_rlt = {
            "facility_id": id,
            "total": total,
            "occupied": occupied,
            "available": available,
            "timestamp": timestamp,
            "zones": zones,
        }
        # dump processed station info to json file
        with open(f"data//{id}.json", "w", encoding="utf-8") as f:
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
    df.to_parquet("data//parking_lots.parquet")


if __name__ == "__main__":
    create_parkinglot()
