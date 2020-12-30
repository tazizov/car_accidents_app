import streamlit as st
from datetime import datetime, timedelta
from creating_plotly_fig import get_plotly_animated_figure
import pathlib

STREAMLIT_STATIC_PATH = pathlib.Path(st.__path__[0]) / 'static'
ABOUT_MD_PATH = './about.md'

st.title("Predicting probability of car accident for London boroughs")

with open(ABOUT_MD_PATH, 'r') as aboutfio:
    aboutmd = aboutfio.read()

st.markdown(aboutmd)

st.sidebar.title("Choose the date here")

date = st.sidebar.slider(label='',
                         min_value=datetime(2015, 1, 1, 0),
                         max_value=datetime(2015, 12, 31, 23),
                         step=timedelta(hours=1),
                         format="DD/MM/YYYY - hh:mm")

st.sidebar.write("Chosen datetime:")
st.sidebar.write(date)


@st.cache()
def _get_fig(date_):
    fig = get_plotly_animated_figure(date_)
    return fig


fig_ = _get_fig(date)
st.plotly_chart(fig_)
