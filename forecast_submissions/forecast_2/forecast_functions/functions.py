import json
import urllib.request
import urllib.parse
import re
from datetime import datetime, timedelta
from io import StringIO
import csv

import pandas as pd
import numpy as np
import xarray as xr
import geopandas as gpd


def get_weather_forecast(latitude, longitude):
    """
    Get weather forecast focusing on rain and temperature extremes
    
    Parameters:
    latitude (float): Latitude of the location
    longitude (float): Longitude of the location
    
    Returns:
    str: CSV formatted string with date, rain_prob, min_temp, and max_temp
    """
    
    def make_request(url):
        """Helper function to make HTTP requests"""
        headers = {'User-Agent': '(Weather Forecast Script, contact@example.com)'}
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode('utf-8'))
    
    def extract_precipitation_chance(forecast):
        """Extract probability of precipitation"""
        # Check if probabilityOfPrecipitation is directly available
        if 'probabilityOfPrecipitation' in forecast:
            prob = forecast['probabilityOfPrecipitation'].get('value', 0)
            return prob if prob is not None else 0
            
        # Otherwise try to extract from detailed forecast
        text = forecast['detailedForecast'].lower()
        
        # Look for percentage patterns
        chance_pattern = r"(\d+)\s*%\s*chance"
        match = re.search(chance_pattern, text)
        if match:
            return int(match.group(1))
            
        # Check for keyword indicators
        if "likely" in text or "probable" in text:
            return 70
        elif "chance" in text:
            return 50
        elif "slight chance" in text:
            return 30
        elif "possible" in text:
            return 20
        
        return 0

    def extract_qpf(forecast):
        """Extract Quantitative Precipitation Forecast from text"""
        text = forecast['detailedForecast'].lower()
        
        # Common patterns for precipitation amounts
        patterns = [
            r"(rainfall|precipitation) amounts? between (\d+\.\d+) and (\d+\.\d+) inch",
            r"(rainfall|precipitation) amounts? around (\d+\.\d+) inch",
            r"(rainfall|precipitation) of (\d+\.\d+) inch",
            r"new rainfall of (\d+\.\d+) to (\d+\.\d+) inch",
            r"precipitation amounts? less than (\d+\.\d+) inch"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                if len(groups) == 3:  # Range format
                    return (float(groups[1]) + float(groups[2])) / 2
                elif len(groups) == 2:  # Single value format
                    if "less than" in text:
                        return float(groups[1]) / 2
                    return float(groups[1])
        
        # If we have a probability but no amount specified, use typical amounts
        prob = extract_precipitation_chance(forecast)
        if prob > 0:
            if "heavy" in text or "substantial" in text:
                return 0.5 * (prob/100)
            elif "light" in text or "scattered" in text:
                return 0.1 * (prob/100)
            else:
                return 0.25 * (prob/100)  # moderate rain assumption
                
        return 0.0

    # Round to 4 decimal places 
    latitude = np.around(latitude, 4)
    longitude = np.around(longitude, 4)

    # Get the forecast data
    points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    grid_data = make_request(points_url)
    
    # Get both regular and hourly forecasts
    forecast_url = grid_data['properties']['forecast']
    forecast_data = make_request(forecast_url)
    
    # Create CSV string for DataFrame
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['date', 'rain_prob', 'rain_amount', 'min_temp', 'max_temp'])
    
    # Process forecast periods into daily data
    daily_data = {}
    
    for period in forecast_data['properties']['periods']:
        date = period['startTime'].split('T')[0]
        
        if date not in daily_data:
            daily_data[date] = {
                'rain_prob': [],
                'rain_amount': 0.0,
                'temps': []
            }
        
        # Update precipitation data
        prob = extract_precipitation_chance(period)
        amount = extract_qpf(period)
        
        daily_data[date]['rain_prob'].append(prob / 100)
        daily_data[date]['rain_amount'] += amount  # Accumulate through day
        daily_data[date]['temps'].append(period['temperature'])
    
    # Write daily data to CSV
    for date, data in sorted(daily_data.items()):
        writer.writerow([
            date,
            max(data['rain_prob']),  # Use maximum probability for the day
            round(data['rain_amount'], 2),
            min(data['temps']),
            max(data['temps'])
        ])
    
    return pd.read_csv(StringIO(output.getvalue()), index_col='date')


def create_usgs_url(site_no, begin_date, end_date):
    """
    Create a USGS URL for streamflow data

    Parameters:
    site_no (str): USGS site number
    begin_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format

    Returns:
    str: URL for USGS streamflow data
    """
    return (f'https://waterdata.usgs.gov/nwis/dv?'
        f'cb_00060=on&format=rdb&referred_module=sw&'
        f'site_no={site_no}&'
        f'begin_date={begin_date}&'
        f'end_date={end_date}')


def open_usgs_data(site, begin_date, end_date):
    """
    Open USGS streamflow data for a given site and date range

    Parameters:
    site (str): USGS site number
    begin_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format

    Returns:
    xarray.Dataset: Streamflow data
    """
    url = create_usgs_url((site), begin_date, end_date)
    response = urllib.request.urlopen(url)
    df = pd.read_table(
        response, comment='#', skipfooter=1, sep='\s+',
        names=['agency', 'site', 'date', 'streamflow', 'quality_flag'],
        index_col=2, parse_dates=True, engine='python', ).iloc[2:]
    df['streamflow'] = df['streamflow'].astype(np.float64)
    df.index = pd.DatetimeIndex(df.index)
    ds = df[['streamflow']].to_xarray().rename({'date': 'time'})
    return ds


def open_gfs_data(
    lat, lon,
    begin_date, end_date,
    url="https://data.dynamical.org/noaa/gfs/analysis-hourly/latest.zarr"
):
    """
    Open GFS data for a given latitude, longitude, and date range

    Parameters:
    lat (float): Latitude of the location
    lon (float): Longitude of the location
    begin_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD'
    url (str): URL to GFS data

    Returns:
    xarray.Dataset: GFS data
    """
    ds = xr.open_zarr(url).sel( latitude=lat, longitude=lon, method='nearest')
    ds = ds.resample(time='1D').mean().sel(time=slice(begin_date, end_date))
    ds = ds.chunk({'time': -1})
    return ds


def open_gage_data(
    gage_id,
    url='https://github.com/HAS-Tools-Fall-2024/homework_arbennett/raw/refs/heads/main/data/gagesii_shapefile/gagesII_9322_sept30_2011.shp',
):
    """
    Open gage data for a given gage ID

    Parameters:
    gage_id (str): Gage ID
    url (str): URL to Gage data

    Returns:
    geopandas.GeoDataFrame: Gage data
    """
    gages = gpd.read_file(url)
    gages.index = gages['STAID'].astype(str)
    gage_data = gages.loc[gage_id]
    return gage_data


def print_forecast_and_statistics(
    site_id,
    site_name,
    date_today,
    latest_streamflow,
    current_streamflow_quantile,
    forecast_streamflow_quantile,
    probable_accum_precip,
    current_precipitation_quantile,
    probable_avg_temp,
    current_temperature_quantile,
):
    message = f"""
    Site name: {site_name}
    Site ID: {site_id}
    Date: {date_today}

    Current Streamflow: {latest_streamflow.values[()]: .2f}
    Current Streamflow Quantile: {current_streamflow_quantile['quantile'].values[()]: .2f}
    Forecast Streamflow based on Current Quantile: {forecast_streamflow_quantile.values[()]}

    Probable Accumulated Precipitation: {probable_accum_precip}
    Current Precipitation Quantile: {current_precipitation_quantile['quantile'].values[()]: .2f}

    Probable Average Temperature: {probable_avg_temp: .2f}
    Current Temperature Quantile: {current_temperature_quantile['quantile'].values[()]: .2f}
    """
    print(message)

