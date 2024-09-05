"""
Provide API functions under /stations
"""

from cachetools import cached, TTLCache
from enum import Enum
from typing import Any, List, Dict
import os
from fastapi.responses import JSONResponse
from fastapi import APIRouter
import polars as pl
from app.stationinfo import StationInfo, create_stationinfo_from_polars_row


router_station = APIRouter(prefix="/stations", tags=["station"])


class DataSource(Enum):
    """
    Data source enum for station info function - JSON or PARQUET
    """

    JSON = "json"
    PARQUET = "parquet"


def return_stationinfo_dataframe_from_json(
    station_geo_filename: str = "../data/station_geo.parquet",
    station_filename: str = "../data/station.parquet",
    parking_lots_dir: str = "../data/",
) -> pl.DataFrame:
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
            df: pl.DataFrame = pl.read_json(
                os.path.join(parking_lots_dir, json_file))
            parking_lots_dfs.append(df)
    df_parking: pl.DataFrame = pl.concat(parking_lots_dfs)

    df: pl.DataFrame = df_station.join(other=df_geo, on="facility_id", how="left").join(
        other=df_parking, on="facility_id", how="left"
    )
    return df


def return_stationinfo_dataframe_from_parquet(
    station_geo_filename: str = "../data/station_geo.parquet",
    station_filename: str = "../data/station.parquet",
    parking_lots_filename: str = "../data/parking_lots.parquet",
) -> pl.DataFrame:
    """Load station info from parquet files and parking lot info from JSON files in a directory

    Args:
        station_geo_filename (str): parquet file storing station geo coordinates
        station_filename (str): parquet file storing station name
        parking_lots_dir (str): directory containing JSON files with parking information

    Returns:
        pl.DataFrame: The merged dataframe

    TODO: call the data_backend refresh function here?
    """
    df_geo: pl.DataFrame = pl.read_parquet(station_geo_filename)
    df_station: pl.DataFrame = pl.read_parquet(station_filename)
    df_parking: pl.DataFrame = pl.read_parquet(parking_lots_filename)

    df: pl.DataFrame = df_station.join(other=df_geo, on="facility_id", how="left").join(
        other=df_parking, on="facility_id", how="left"
    )
    return df


# set cache time to live as 120 seconds
@cached(cache=TTLCache(maxsize=8192, ttl=120))
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
                "parking_slots": {
                    "486" : {
                        "station_id": "486",
                        "short_name": "Ashfield",
                        "full_name": "AshfieldCarPark",
                        "coordinates": (-33.888104, 151.126577),
                        "total": 205,
                        "available": 205,
                        "occupied": 0,
                        "timestamp": "2024-09-04T20:09:02"
                    },
                    "487" : {
                        "station_id": "487",
                        "short_name": "Kogarah",
                        "full_name": "SYD319 Kogarah Park and Ride",
                        "coordinates": (-33.96369941, 151.1319494),
                        "total": 236,
                        "available": 235,
                        "occupied": 1,
                        "timestamp": "2024-09-04T20:09:02"
                    }
                }
            }
    """
    df: pl.DataFrame = return_stationinfo(source=DataSource.JSON)

    stations: List[StationInfo] = []

    for row in df.iter_rows():
        station: StationInfo = create_stationinfo_from_polars_row(row)
        stations.append(station)

    content: Dict[str, Dict[str, Any]] = {
        "parking_lost": generate_parking_slots_dict(stations)
    }

    return JSONResponse(content=content, status_code=200)


def generate_parking_slots_dict(stations: List[StationInfo]) -> Dict[str, Any]:
    """Generate a dictionary containing station info for each station.

    The dictionary will have the following structure:
    {
        station_id_1: {station_info_1},
        station_id_2: {station_info_2},
        ...
    }
    where each station_info is a dictionary containing the details for that station.

    Args:
        stations (List[StationInfo]): A list of stationinfo container

    Returns:
        Dict[str, Any]: Dictionary contains station info with station ids as keys
    """
    station_dict: Dict[str, Any] = {}
    for station in stations:
        station_dict.update(station.to_dict())

    return station_dict
