from fastapi import FastAPI
from folium import Map
from pandas import DataFrame
from plot_map import generate_map, generate_station_data
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/map")
async def plot_map(response_class=HTMLResponse) -> HTMLResponse:
    """
    Embed a foliumn map in the HTML response
    """

    # TODO: direct query mode; No cache now.
    df: DataFrame = generate_station_data()
    m: Map = generate_map(df)
    iframe: str = m.get_root()._repr_html_()

    html_content = f"""
    <html>
        <head>
        <title>
            Ride & Park Map
        </title>
        </head>

        <body>
        <h1> Car Park Map </h1>

        {iframe}

        </body>

    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)
