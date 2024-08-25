from bs4 import BeautifulSoup
import requests


URL = "https://transportnsw.info/travel-info/ways-to-get-around/drive/parking/transport-parkride-car-parks"


response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")

with open("sample_html.txt", encoding="utf-8", mode="w") as f:
    f.write(response.text)
