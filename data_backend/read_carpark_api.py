"""
Fetch car park occupancy data;

API: https://api.transport.nsw.gov.au/v1/carpark
"""

from rich import print_json
import requests

API = "https://api.transport.nsw.gov.au/v1/carpark"
NSW_TRANSPORT_OPEN_DATA_TOKEN: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI4WlZsMm5ENTdYYXVGLXJZSXRzUWYzNnhJdGdUUURSOHVzOHZWWGJYRUFRIiwiaWF0IjoxNzI0NDU3ODQ0fQ.MeUI_yOnPI3Tj5izgGGDP2DEvZmEoXb7eF56Ee_Bm7Y"


def extract_carpark_info(
    facility_id: str, token: str = NSW_TRANSPORT_OPEN_DATA_TOKEN
) -> requests.Response:
    """Read station parking information data from NSW Transport Open
    API. Return the response returned.

    Args:
        facility_id (str): The ID of the individual facility to retrieve information for.

        token (str): the token retrieved from https://opendata.transport.nsw.gov.au/user-guide

    Returns:
        requests.Response: The response object
    """

    assert len(facility_id) > 0
    assert facility_id.isnumeric()

    # pass token in header
    head: dict[str, str] = {"Authorization": f"apikey {token}"}

    api: str = f"{API}?facility={facility_id}"

    # timeout in 20 seconds
    station_response: requests.Response = requests.get(
        api, headers=head, timeout=20)

    return station_response


def extract_station_list(token: str = NSW_TRANSPORT_OPEN_DATA_TOKEN) -> requests.Response:
    """
    Retrieve a list of all station facilities from the NSW Transport Open API.

    Args:
        token (str): The token retrieved from https://opendata.transport.nsw.gov.au/user-guide

    Returns:
        requests.Response: The response object containing the list of station facilities
    """
    head: dict[str, str] = {"Authorization": f"apikey {token}"}

    api: str = f"{API}"

    station_list: requests.Response = requests.get(
        api, headers=head, timeout=20)

    return station_list


if __name__ == "__main__":
    while True:
        carpark: str = input("key in carpark facility ID, e.g. 6\n")
        response: requests.Response = extract_carpark_info(carpark)
        print_json(response.text)
