"""
This module contains tests for the root and stations endpoints of the API.
"""

from typing import Any, Dict
import json
import requests


def test_root() -> None:
    """
    Test http://127.0.0.1:8000/
    """
    response: requests.Response = requests.get("http://127.0.0.1:8000/", timeout=20)
    assert response.status_code == 200, "Root endpoint did not return status code 200"


def test_stations() -> None:
    """
    Test http://127.0.0.1:8000/stations
    """

    response: requests.Response = requests.get(
        "http://127.0.0.1:8000/stations", timeout=20
    )

    # expect 200 status code
    assert (
        response.status_code == 200
    ), "Stations endpoint did not return status code 200"

    # test returned JSON
    stations: Dict[str, Any] = json.loads(response.text)
    assert "parking_slots" in stations, "'parking_slots' not in response"

    stations_info = stations["parking_slots"]
    assert len(stations_info) == 38, "Expected 38 parking slots"

    # sample test data content
    assert stations_info[0]["station_id"] == "486", "Station ID mismatch at index 0"
    assert (
        stations_info[0]["short_name"] == "Ashfield"
    ), "Short name mismatch at index 0"
    assert (
        stations_info[0]["available"] >= 0
    ), "Available slots should be non-negative at index 0"
    assert stations_info[0]["address"] == "Brown Street", "Address mismatch at index 0"

    assert stations_info[18]["station_id"] == "16", "Station ID mismatch at index 18"
    assert (
        stations_info[18]["short_name"] == "Leppington"
    ), "Short name mismatch at index 18"
    assert (
        stations_info[18]["available"] >= 0
    ), "Available slots should be non-negative at index 18"
    assert (
        stations_info[18]["address"] == "199A Rickard Road"
    ), "Address mismatch at index 18"

    assert stations_info[36]["station_id"] == "31", "Station ID mismatch at index 36"
    assert (
        stations_info[36]["short_name"] == "Bella Vista"
    ), "Short name mismatch at index 36"
    assert (
        stations_info[36]["available"] >= 0
    ), "Available slots should be non-negative at index 36"
    assert stations_info[36]["address"] == "Byles Place", "Address mismatch at index 36"
