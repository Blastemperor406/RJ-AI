import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
def weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 12.9719,
        "longitude": 77.5937,
        "hourly": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation_probability", "rain", "showers", "weather_code", "cloud_cover", "wind_speed_10m", "wind_gusts_10m","precipitation"],
        "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "rain_sum", "showers_sum", "precipitation_hours", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max"],
        "timezone": "auto",
        'forecast_hours':12,
        "forecast_days":1
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    print(hourly)
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(3).ValuesAsNumpy()
    hourly_rain = hourly.Variables(4).ValuesAsNumpy()
    hourly_showers = hourly.Variables(5).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(6).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(7).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(8).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(9).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(10).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time()+response.UtcOffsetSeconds(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd()+response.UtcOffsetSeconds(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}
    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["rain"] = hourly_rain
    hourly_data["showers"] = hourly_showers
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    #print(hourly_dataframe)

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(3).ValuesAsNumpy()
    daily_showers_sum = daily.Variables(4).ValuesAsNumpy()
    daily_precipitation_hours = daily.Variables(5).ValuesAsNumpy()
    daily_precipitation_probability_max = daily.Variables(6).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(7).ValuesAsNumpy()
    daily_wind_gusts_10m_max = daily.Variables(8).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time()+response.UtcOffsetSeconds(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd()+response.UtcOffsetSeconds(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["showers_sum"] = daily_showers_sum
    daily_data["precipitation_hours"] = daily_precipitation_hours
    daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max

    daily_dataframe = pd.DataFrame(data = daily_data)
    #print(daily_dataframe)
    current_weather=(hourly_dataframe.iloc[0:1])
    current_weather=current_weather.drop(columns=['precipitation_probability'])
    forecast_hourly=hourly_dataframe.iloc[1:]

    current_weather=current_weather.to_json(orient='records',date_format='iso')
    forecast_hourly=forecast_hourly.to_json(orient='records',date_format='iso')
    daily_dataframe=daily_dataframe.to_json(orient='records',date_format='iso')

    return [current_weather,forecast_hourly]


#print(weather())
