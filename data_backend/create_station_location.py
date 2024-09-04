# Create the station parking location dataset
# Columns includes facility_id, station name, latitude, longitude

from read_carpark_api import extract_carpark
import pandas as pd
import json


def create_carpark_location() -> None:
    carparks = extract_carpark()

    # print(carparks.text)

    df: pd.DataFrame = pd.DataFrame(json.loads(carparks.text), index=[0]).melt()

    df: pd.DataFrame = df.rename(
        columns={"variable": "facility_id", "value": "station_name"}
    )

    df.to_parquet("data//station.parquet")


if __name__ == "__main__":
    create_carpark_location()
