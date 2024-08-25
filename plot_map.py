import folium
import pandas as pd


def generate_station_data() -> pd.DataFrame:
    df_station_geo = pd.read_parquet("data//station_geo.parquet")
    df_station = pd.read_parquet("data//station.parquet")
    df_parking = pd.read_parquet("data//parking_lots.parquet")

    df = df_station.merge(df_station_geo, how="left", on="facility_id").merge(
        df_parking, how="left", on="facility_id"
    )

    df: pd.DataFrame = df.loc[~pd.isnull(df["timestamp"]), :]

    return df


def generate_map(df: pd.DataFrame):
    # Sydney Opera (-33.89, 151.03)
    m = folium.Map(location=(-33.89, 151.03))

    for row in df.iterrows():
        row = row[1]
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            tooltip=f"{row['station_name']}\n total: {row['total']:.0f}\n available:{row['available']:.0f}",
            icon=folium.Icon(icon='train', prefix='fa'),
        ).add_to(m)

    m.save("map//station_map.html")
    return m


if __name__ == "__main__":
    df = generate_station_data()

    generate_map(df)
