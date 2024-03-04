# helpers.py

from ipyleaflet import Map, GeoData
from geopandas import GeoDataFrame, points_from_xy
import pandas as pd
import plotly.express as px
from numpy import vectorize


def get_city(stations):
    # Check if 'city' column exists in 'stations' DataFrame
    if 'city' not in stations.columns:
        return "Error: 'city' column not found in DataFrame 'stations'."

    # Get unique values in the 'city' column
    unique_cities = stations['city'].unique()

    # Check if there is only one unique value in 'city' column
    if len(unique_cities) == 1:
        return unique_cities[0]
    else:
        return "Error: More than one unique value in the 'city' column of DataFrame 'stations'."

@vectorize
def city_tz_convert(datetime, city):
    """Converts the datetime to the city local timezone.
    City should be one of "dc", "austin", or "chicago"
    Assumes the datetime is passed in as a pandas.Timestamp object,
    not as a datetime pandas Series object
    """
    if city not in ["dc", "austin", "chicago"]:
        raise ValueError(f"Unknown city value: {city}")

    if city == "dc":
        new_dt_tz = datetime.tz_convert("EST")
    elif city in ["austin", "chicago"]:
        new_dt_tz = datetime.tz_convert("CST6CDT")

    return new_dt_tz


def show_city(stations):
    """
    city should be one of: "dc", "austin", or "chicago"
    """

    # Check if 'stations' DataFrame is empty
    if stations.empty:
        return "Error: DataFrame 'stations' is empty."

    gdf = GeoDataFrame(
        stations,
        geometry = points_from_xy(
            stations.lon,
            stations.lat
        )
    )

    geo_data = GeoData(
        geo_dataframe=gdf,
        style={
            "color": "black",
            "radius": 4,
            "fillColor": "#517664",
            "opacity": 0.5,
            "weight": 1.9,
            "dashArray": "2",
            "fillOpacity": 0.6,
        },
        hover_style={"fillColor": "red", "fillOpacity": 0.2},
        point_style={
            "radius": 1,
            "color": "red",
            "fillOpacity": 0.8,
            "fillColor": "blue",
            "weight": 3,
        },
        name="Release",
    )

    city = get_city(stations)

    if city == "dc":
        center = (38.9072, -77.0369)
        zoom = 10
    elif city == "austin":
        center = (30.2672, -97.7431)
        zoom = 13
    elif city == "chicago":
        center = (41.8781, -87.6298)
        zoom = 10

    m = Map(center=center, zoom=zoom)
    m.add(geo_data)
    return m

def show_trend(bikes):

    bikes_sub = bikes[['time', 'num_bikes_available']]

    plot_data = (
        bikes_sub
        .groupby(['time'])
        .agg({'num_bikes_available': 'mean'})
        .reset_index()
    )

    custom_template = {
        "layout": {
            "plot_bgcolor": "#D6E5E3",  # Background color
            "paper_bgcolor": "#f8f9fa",  # Paper color (where the plot is drawn)
        }
    }

    return px.line(
        plot_data,
        x="time",
        y="num_bikes_available",
        title="Average Number of Bikes Available Over Time",
        color_discrete_sequence=["#517664"],
        template=custom_template,
        labels={
            "num_bikes_available": "Average Number of Bikes Available",
            "time": "Date and Time"
            }
        )
