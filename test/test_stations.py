from polars import DataFrame
from app.routers.stations import (
    return_stationinfo_dataframe_from_json,
)


# def test_read_stationinfo_json() -> None:
#     """
#     Test the return_stationinfo function with JSON data source
#     """
#     df: DataFrame = return_stationinfo(source=DataSource.JSON)
#     assert df.shape[0] > 10


def test_read_stationinfo_json() -> None:
    """Test the return_stationinfo_dataframe_from_json function"""

    df: DataFrame = return_stationinfo_dataframe_from_json(
        station_geo_filename="data/station_geo.parquet",
        station_filename="data/station.parquet",
        parking_lots_dir="data/",
    )
    print(df.columns)
    assert df.shape[0] > 10
