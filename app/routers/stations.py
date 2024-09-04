"""
Provide API functions under /stations
"""

from enum import Enum
from typing import Any, Self, List, Tuple, Dict
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from pydantic.dataclasses import dataclass
import os
import polars as pl

router_station = APIRouter(prefix="/stations", tags=["station"])


class DataSource(Enum):
    """
    Data source enum for station info function - JSON or PARQUET
    """
    JSON = "json"
    PARQUET = "parquet"


@dataclass
class StationInfo():
    """
    class for station information
    """
    station_id: str
    short_name: str
    full_name: str
    address: str
    coordinates: Tuple[float, float]
    total: int
    available: int
    occupied: int
    timestamp: str

    def annouce(self) -> str:
        """Return a string describing the station availability briefly

        Returns:
            str: _description_
        """
        return f"The station {self.short_name} has {self.available} available slots"

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation of the station info

        Returns:
            Dict[str, Any]: _description_
        """
        rlt_dict = self.__dict__
        del rlt_dict["__pydantic_initialised__"]
        return rlt_dict


def create_stationinfo_from_polars_row(row: tuple) -> StationInfo:
    """create a StationInfo class from a polars row

    Args:
        row (tuple): polars row

    Returns:
        Self: StationInfo class
    """
    return StationInfo(
        station_id=row[0],
        short_name=row[3],
        full_name=row[2],
        address=row[4],
        coordinates=(row[5], row[6]),
        available=row[9],
        timestamp=row[10],
        total=row[7],
        occupied=row[8],
    )


def return_stationinfo_dataframe_from_json(
        station_geo_filename: str = "../data/station_geo.parquet",
        station_filename: str = "../data/station.parquet",
        parking_lots_dir: str = "../data/") -> pl.DataFrame:
    """Load station info from parquet files and parking lot info from JSON files in a directory

    Args:
        station_geo_filename (str): parquet file storing station geo coordinates
        station_filename (str): parquet file storing station name
        parking_lots_dir (str): directory containing JSON files with parking information

    Returns:
        pl.DataFrame: The merged dataframe
    """
    df_geo: pl.DataFrame = pl.read_parquet(station_geo_filename)
    df_station: pl.DataFrame = pl.read_parquet(station_filename)

    # Read all JSON files in the directory and concatenate them into a single DataFrame

    parking_lots_dfs: List[pl.DataFrame] = []

    for json_file in os.listdir(parking_lots_dir):
        if json_file.endswith(".json"):

            df: pl.DataFrame = pl.read_json(os.path.join(parking_lots_dir,
                                                         json_file))
            parking_lots_dfs.append(df)

            # with open(os.path.join(parking_lots_dir, json_file),
            #           'r',
            #           encoding='utf8') as f:

            # parking_lots_info: dict[str, Any] = json.load(f)
            # parking_lots_list.append(parking_lots_info)
    # parking_lots_list.append(json.load(f))
    # df_parking: pl.DataFrame = pl.read_json("../data/")

    df_parking: pl.DataFrame = pl.concat(parking_lots_dfs)

    # print(df_parking)

    df: pl.DataFrame =\
        df_station.join(other=df_geo,
                        on="facility_id",
                        how="left")\
        .join(other=df_parking,
              on="facility_id",
              how="left")
    return df


def return_stationinfo_dataframe_from_parquet(
        station_geo_filename: str = "../data/station_geo.parquet",
        station_filename: str = "../data/station.parquet",
        parking_lots_filename: str = "../data/parking_lots.parquet") -> pl.DataFrame:
    """Load station info from parquet files and parking lot info from JSON files in a directory

    Args:
        station_geo_filename (str): parquet file storing station geo coordinates
        station_filename (str): parquet file storing station name
        parking_lots_dir (str): directory containing JSON files with parking information

    Returns:
        pl.DataFrame: The merged dataframe
    """
    df_geo: pl.DataFrame = pl.read_parquet(station_geo_filename)
    df_station: pl.DataFrame = pl.read_parquet(station_filename)
    df_parking: pl.DataFrame = pl.read_parquet(parking_lots_filename)

    df: pl.DataFrame =\
        df_station.join(other=df_geo,
                        on="facility_id",
                        how="left")\
        .join(other=df_parking,
              on="facility_id",
              how="left")
    return df


def return_stationinfo(source: DataSource) -> pl.DataFrame:
    """
    A wrapper function to make the data source switch between json and parquet easier
    """
    if source == DataSource.JSON:
        df: pl.DataFrame = return_stationinfo_dataframe_from_json()

    if source == DataSource.PARQUET:
        df: pl.DataFrame = return_stationinfo_dataframe_from_parquet()

    # remove stations where the timestamp is None

    df = df.filter(pl.col("timestamp").is_not_null())
    return df


@router_station.get("/")
def get_stations_dict() -> JSONResponse:
    """Return a JSON response containing info for all stations
    on query to http://127.0.0.1:8000/stations

    Returns:
            Dict[str, Any]: The schema and sample response is

            {
                "parking_slots": [
                    {
                        "station_id": "486",
                        "short_name": "Ashfield",
                        "full_name": "AshfieldCarPark",
                        "coordinates": (-33.888104, 151.126577),
                        "total": 205,
                        "available": 205,
                        "occupied": 0,
                        "timestamp": "2024-09-04T20:09:02"
                    },
                    {
                        "station_id": "487",
                        "short_name": "Kogarah",
                        "full_name": "SYD319 Kogarah Park and Ride",
                        "coordinates": (-33.96369941, 151.1319494),
                        "total": 236,
                        "available": 235,
                        "occupied": 1,
                        "timestamp": "2024-09-04T20:09:02"
                    }
                ]
            }
        """
    df: pl.DataFrame = return_stationinfo(source=DataSource.JSON)

    stations: List[StationInfo] = []

    for row in df.iter_rows():
        station: StationInfo = create_stationinfo_from_polars_row(row)
        stations.append(station)

    content: dict[str, list[dict[str, Any]]] = {
        "parking_slots": [station.to_dict() for station in stations]
    }
    return JSONResponse(content=content, status_code=200)


if __name__ == "__main__":
    df: pl.DataFrame = return_stationinfo(source=DataSource.JSON)
    print(df)
