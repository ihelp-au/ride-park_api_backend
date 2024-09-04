"""
Scrpae the parking lot availability info
from https://transportnsw.info/travel-info/ways-to-get-around/drive/parking/transport-parkride-car-parks
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd


URL: str = "https://transportnsw.info/travel-info/ways-to-get-around/drive/parking/transport-parkride-car-parks"


def scrape_parking_info(url: str) -> pd.DataFrame:
    """Use bs4 to scrape the data from url
    and return a dataframe

    Args:
        url (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    response: requsets.Response = requests.get(URL)

    soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

    print(response.text)


def extract_parking_info(info: str) -> pd.DataFrame:
    """_summary_

    Args:
        info (str): _description_

    Returns:
        pd.DataFrame: _description_
    """


if __name__ == "__main__":
    scrape_parking_info(URL)
