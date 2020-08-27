import streamlit as st

import numpy as np
import pandas as pd

DATA_URL = (
    "/Desktop/Vehicle-Collisions-NYC/Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("Motor Vehicle Collisions in NYC")
st.markdown("This dashboard analyzes motor vehicle collisions in NYC")

# @st.cache doesn't re-run the app everytime a
# computation needs to be completed.
# It will re-run the app if the input or code has changed
@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows,parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_data_crash_time': 'date/time'}, inplace = True)
    return data

data = load_data(50000)

st.header("Where are most people injured in NYC?")
injured_people = st.slider("Number of persons injured in vehicle collisions",0,19)

#plot data
st.map(data.query("injured_persons >= @injured_people")[["latitude","longitude"]].dropna(how="any"))

st.header("How many collisions occured during a given time of day?")
hour = st.selectbox("Hour to look at", range(0,24),1)
data = data[data['date/time'].dt.hour == hour]


if st.checkbox("Show Raw Data", False):
    st.subheader("Raw Data")
    st.write(data)
