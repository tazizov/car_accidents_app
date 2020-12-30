import plotly.express as px
import pickle5
import json
from collections import namedtuple
import geopandas as gpd
from datetime import datetime
import pandas as pd

DEFAULT_POINTS_UNIQUE_FILEPATH = './data/preprocessed/points_dropped.pkl'
DEFAULT_POINTS_WEATHER_FILEPATH = './data/preprocessed/points_weather.pkl'
DEFAULT_POLYS_LIST_FILEPATH = './data/preprocessed/polys_list.pkl'
DEFAULT_BOROUGHS_FILEPATH = './data/london_boroughs.json'
DEFALUT_ISOFOREST_FILEPATH = './data/forest.pkl'
MAPBOX_TOKEN = 'pk.eyJ1IjoidGF6aXpvdiIsImEiOiJja2o1aTkyaXYweGt2MnZrM3pycW85bjFuIn0.o5E1GoUzcaw88zQuqae-AA'
DAY_HOURS_COUNT = 5
CENTER = {'lat': 51.50052370921687, 'lon': -0.10938133210902337}
FIGURE_HEIGHT = 800
FIGURE_WIDTH = 1000


px.set_mapbox_access_token(MAPBOX_TOKEN)

with open(DEFALUT_ISOFOREST_FILEPATH, 'rb') as pfio:
    forest = pickle5.load(pfio)

with open(DEFAULT_BOROUGHS_FILEPATH, 'r') as jfio:
    london_boroughs = gpd.read_file(json.load(jfio))

with open(DEFAULT_POINTS_UNIQUE_FILEPATH, 'rb') as pfio:
    points_unique = pickle5.load(pfio)

with open(DEFAULT_POINTS_WEATHER_FILEPATH, 'rb') as pfio:
    points_weather = pickle5.load(pfio)

with open(DEFAULT_POLYS_LIST_FILEPATH, 'rb') as pfio:
    polys_list = pickle5.load(pfio)

template = namedtuple('template',
                      [
                          'Day_of_Week',
                          'Weather_Conditions',
                          'Road_Surface_Conditions',
                          'month',
                          'hour'
                      ]
                      )


def fill_template(some_date, df):
    if df[df['datetime'] == some_date].shape[0] > 0:
        filled_template = template(
            Road_Surface_Conditions=df[df['datetime'] == some_date]['Road_Surface_Conditions'].median(),
            Weather_Conditions=df[df['datetime'] == some_date]['Weather_Conditions'].median(),
            Day_of_Week=some_date.weekday(),
            month=some_date.month,
            hour=some_date.hour
        )
    else:
        filled_template = template(
            Road_Surface_Conditions=df['Road_Surface_Conditions'].median(),
            Weather_Conditions=df['Weather_Conditions'].median(),
            Day_of_Week=some_date.weekday(),
            month=some_date.month,
            hour=some_date.hour
        )
    return filled_template


def add_conditions_to_points(df, tuple_data):
    df['Day_of_Week'] = tuple_data.Day_of_Week
    df['Weather_Conditions'] = tuple_data.Weather_Conditions
    df['Road_Surface_Conditions'] = tuple_data.Road_Surface_Conditions
    df['month'] = tuple_data.month
    df['hour'] = tuple_data.hour
    return df


def scale_scores(scores):
    scores_scaled = scores - scores.min()
    return scores_scaled


def generate_scores_for_day(some_day):
    scores_grouped = pd.DataFrame()
    scores_grouped['boroughs_id'] = polys_list
    test_df = add_conditions_to_points(points_unique, fill_template(some_day, points_weather))
    scores = forest.decision_function(test_df)
    scores_grouped['scores'] = scores
    borough_scores = scores_grouped.groupby('boroughs_id')['scores'].mean().sort_index().values
    borough_scores = scale_scores(borough_scores)
    return borough_scores


def get_plotly_animated_figure(some_day):
    day_scores = generate_scores_for_day(some_day)
    day_boroughs_data = london_boroughs.copy()
    day_boroughs_data['proba'] = day_scores
    fig = px.choropleth_mapbox(
        day_boroughs_data,
        geojson=day_boroughs_data.geometry,
        locations='id',
        color='proba',
        hover_name='NAME',
        hover_data={'proba': ":.3f", 'id': False},
        center=CENTER,
        zoom=8,
        color_continuous_scale=["lightgrey", "red"],
        width=FIGURE_WIDTH,
        height=FIGURE_HEIGHT,
    )
    return fig

if __name__ == '__main__':
    fig = get_plotly_animated_figure(datetime(2006, 3, 3))
    fig.show()