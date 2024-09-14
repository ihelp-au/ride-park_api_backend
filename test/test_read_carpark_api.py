"""
This module contains unit tests for the carpark API and station information functions.

Functions:
- test_read_stationinfo_json: Tests the return_stationinfo_dataframe_from_json function to ensure it returns a DataFrame with more than 10 rows.
- test_extract_carpark_info_individualstation: Tests the extract_carpark_info function by passing a facility ID and verifying the response and its contents.
- test_extract_carpark_info_invalid_station: Tests the extract_carpark_info function with an invalid facility ID to ensure it returns a 404 status code.
- test_extract_carpark_info_missing_fields: Tests the extract_carpark_info function to check for missing fields in the response.
"""

from typing import Dict, Any
import json
import polars as pl
from requests import Response
from app.routers.stations import (
    return_stationinfo_dataframe_from_json,
)
from data_backend.read_carpark_api import extract_carpark_info


def test_read_stationinfo_json() -> None:
    """Test the return_stationinfo_dataframe_from_json function"""

    df: pl.DataFrame = return_stationinfo_dataframe_from_json(
        station_geo_filename="data/station_geo.parquet",
        station_filename="data/station.parquet",
        parking_lots_dir="data/",
    )
    assert df.shape[0] > 10
    # station.parquet
    assert df['facility_id'].dtype == pl.Utf8
    assert df['station_name'].dtype == pl.Utf8
    # station_geo.parquet
    assert df['full_name'].dtype == pl.Utf8
    assert df['short_name'].dtype == pl.Utf8
    assert df['address'].dtype == pl.Utf8
    assert df['latitude'].dtype == pl.Float64
    assert df['longitude'].dtype == pl.Float64
    # parking_lots.parquet
    assert df['total'].dtype == pl.Int64
    assert df['occupied'].dtype == pl.Int64
    assert df['available'].dtype == pl.Int64
    assert df['timestamp'].dtype == pl.Utf8
    assert df['zones'].dtype == pl.Utf8


def test_extract_carpark_info_individualstation() -> None:
    """
    Test function extract_carpark_info from
    data_backend//read_carpark_api.py and passing
    facility id of an individual station
    """
    fid: str = "488"
    response = extract_carpark_info(facility_id=fid)

    assert (
        response.status_code == 200
    ), f"facility id {fid} does not return expected 200 status code"

    station_info: Dict[str, Any] = json.loads(response.text)
    assert "tsn" in station_info
    assert "time" in station_info
    assert "zones" in station_info
    assert "occupancy" in station_info
    assert station_info["facility_id"] == fid


def test_extract_carpark_info_invalid_station() -> None:
    """
    Test function extract_carpark_info from data_backend//read_carpark_api.py with an invalid facility id
    """
    invalid_fid: str = "999999"  # Assuming this is an invalid facility id
    response: Response = extract_carpark_info(facility_id=invalid_fid)

    assert response.status_code == 404, f"Invalid facility id {invalid_fid} should return 404 status code"


def test_extract_carpark_info_missing_fields() -> None:
    """
    Test function extract_carpark_info from data_backend//read_carpark_api.py to check for missing fields in the response
    """
    fid: str = "488"
    response = extract_carpark_info(facility_id=fid)
    station_info: Dict[str, Any] = json.loads(response.text)

    missing_fields = []
    for field in ["tsn", "time", "zones", "occupancy", "facility_id"]:
        if field not in station_info:
            missing_fields.append(field)

    assert len(
        missing_fields) == 0, f"Missing fields in the response: {', '.join(missing_fields)}"
