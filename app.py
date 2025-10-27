import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(layout="wide")
st.title('Uber pickups in NYC')

# Convertir l’image locale en base64
def get_base64_of_image(image_path):
    img = Image.open(image_path)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

img_base64 = get_base64_of_image("images/image.jpg")

# Injecter l’image en HTML pleine largeur
st.markdown(
    f"""
    <style>
    .full-width-img {{
        width: 100vw;
        height: auto;
        margin: 0;
        padding: 0;
        display: block;
    }}
    </style>
    <img class="full-width-img" src="data:image/jpeg;base64,{img_base64}">
    """,
    unsafe_allow_html=True
)


DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)