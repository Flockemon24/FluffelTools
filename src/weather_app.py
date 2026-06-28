import openmeteo_requests
import streamlit as st
import plotly.express as px
import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

def run_weather_app():
    st.title("Weather App")
    st.write("This app fetches weather data from the Open-Meteo API and displays it.")
    location = st.text_input("Enter a location (latitude, longitude):", "51.401055, 7.184833")
    latitude, longitude = map(float, location.split(","))
    timezone = st.selectbox("Select a timezone:", ["Europe/Berlin", "America/New_York", "Asia/Tokyo"])

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "uv_index_max", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_sum", "precipitation_hours", "precipitation_probability_max"],
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "precipitation_probability", "rain", "showers", "snowfall", "snow_depth"],
        "current": ["temperature_2m", "relative_humidity_2m", "is_day", "apparent_temperature", "precipitation", "rain", "showers", "snowfall"],
        "timezone": timezone,
        "past_days": 0,
        "forecast_days": 14,
    }
    responses = openmeteo.weather_api(url, params = params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    st.write(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    st.write(f"Elevation: {response.Elevation()} m asl")
    st.write(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
    st.write(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()/3600}h")

    # Process current data. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_is_day = current.Variables(2).Value()
    current_apparent_temperature = current.Variables(3).Value()
    current_precipitation = current.Variables(4).Value()
    current_rain = current.Variables(5).Value()
    current_showers = current.Variables(6).Value()
    current_snowfall = current.Variables(7).Value()

    st.write(f"\nCurrent time: {current.Time()}")
    st.write(f"Current temperature_2m: {current_temperature_2m}")
    st.write(f"Current relative_humidity_2m: {current_relative_humidity_2m}")
    st.write(f"Current is_day: {current_is_day}")
    st.write(f"Current apparent_temperature: {current_apparent_temperature}")
    st.write(f"Current precipitation: {current_precipitation}")
    st.write(f"Current rain: {current_rain}")
    st.write(f"Current showers: {current_showers}")
    st.write(f"Current snowfall: {current_snowfall}")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(3).ValuesAsNumpy()
    hourly_rain = hourly.Variables(4).ValuesAsNumpy()
    hourly_showers = hourly.Variables(5).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(6).ValuesAsNumpy()
    hourly_snow_depth = hourly.Variables(7).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        ).tz_convert(response.Timezone().decode())
    }

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["rain"] = hourly_rain
    hourly_data["showers"] = hourly_showers
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["snow_depth"] = hourly_snow_depth

    hourly_df = pd.DataFrame(data = hourly_data)
    st.write("\nHourly data\n", hourly_df)

    # Hourly temperature graph
    temp_graph = px.line(
        hourly_df, 
        x='date', 
        y='temperature_2m', 
        title='Hourly Temperature',
        markers=True,
        hover_data=['temperature_2m']
    )

    temp_graph.update_traces(
        hovertemplate="<br>".join([
            "<b>Date:</b> %{x}",
            "<b>Temperature:</b> %{y} °C"
        ])
    )

    st.plotly_chart(temp_graph, width='stretch')

    # Hourly precipitation graph
    prec_graph = px.line(
        hourly_df, 
        x='date', 
        y='precipitation', 
        title='Hourly Precipitation',
        markers=True,
        hover_data=['precipitation_probability']
    )

    prec_graph.update_traces(
        hovertemplate="<br>".join([
            "<b>Date:</b> %{x}",
            "<b>Precipitation:</b> %{y} mm",
            "<b>Probability:</b> %{customdata[0]}%"
        ])
    )

    st.plotly_chart(prec_graph, width='stretch')

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
    daily_apparent_temperature_max = daily.Variables(2).ValuesAsNumpy()
    daily_apparent_temperature_min = daily.Variables(3).ValuesAsNumpy()
    daily_sunrise = daily.Variables(4).ValuesInt64AsNumpy()
    daily_sunset = daily.Variables(5).ValuesInt64AsNumpy()
    daily_daylight_duration = daily.Variables(6).ValuesAsNumpy()
    daily_sunshine_duration = daily.Variables(7).ValuesAsNumpy()
    daily_uv_index_max = daily.Variables(8).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(9).ValuesAsNumpy()
    daily_showers_sum = daily.Variables(10).ValuesAsNumpy()
    daily_snowfall_sum = daily.Variables(11).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(12).ValuesAsNumpy()
    daily_precipitation_hours = daily.Variables(13).ValuesAsNumpy()
    daily_precipitation_probability_max = daily.Variables(14).ValuesAsNumpy()

    daily_data = {
        "date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        ).tz_convert(response.Timezone().decode())
    }

    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
    daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
    daily_data["sunrise"] = daily_sunrise
    daily_data["sunset"] = daily_sunset
    daily_data["daylight_duration"] = daily_daylight_duration
    daily_data["sunshine_duration"] = daily_sunshine_duration
    daily_data["uv_index_max"] = daily_uv_index_max
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["showers_sum"] = daily_showers_sum
    daily_data["snowfall_sum"] = daily_snowfall_sum
    daily_data["precipitation_sum"] = daily_precipitation_sum
    daily_data["precipitation_hours"] = daily_precipitation_hours
    daily_data["precipitation_probability_max"] = daily_precipitation_probability_max

    daily_df = pd.DataFrame(data = daily_data)
    st.write("\nDaily data\n", daily_df)
