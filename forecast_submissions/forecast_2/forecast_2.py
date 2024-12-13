#%%
import numpy as np
import pandas as pd
import xarray as xr

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')


import argparse  # TODO: Import argparse from the ArgumentParser module
pass 

# TODO: Import the following functions from forecast_functions.functions
from forecast_functions.functions import (
    open_usgs_data,
    open_gage_data,
    open_gfs_data,
    get_weather_forecast,
    print_forecast_and_statistics,
)
# - open_usgs_data
# - open_gage_data
# - open_gfs_data
# - get_weather_forecast
# - print_forecast_and_statistics
pass


# TODO: These functions will need to be implemented later, you can 
#      leave them as is for now, but you will need to come back to
#      them as you progress through the assignment.
# TODO: The following functions need to be implemented in this script
#      - process_climatology
#      - determine_historic_value
#      - convert_f_to_c

def download_gage_data(save_location='./data'):
    import os
    import requests
 
    # Create the data directory if it doesn't exist
    if not os.path.exists(save_location):
        os.makedirs(save_location)
   
    url = ('https://github.com/HAS-Tools-Fall-2024/homework_arbennett/'
           'raw/refs/heads/main/data/gagesii_shapefile/gagesII_9322_sept30_2011')
    extensions_to_download = ['.shp', '.dbf', '.prj', '.sbn', '.sbx', '.shx']
 
    for extension in extensions_to_download:
        r = requests.get(url + extension)
        with open(f'{save_location}/gagesII_9322_sept30_2011{extension}', 'wb') as f:
            f.write(r.content)
        print(f'Downloaded: {url}{extension}')
gage_id = '09506000'
        
def process_climatology(ds, quantiles=[0.05, 0.33, 0.5 ,0.66, 0.95]):
    return (
        ds.groupby("time.week")
        .quantile(quantiles, dim="time")
        )
    """
    Process climatology data to calculate quantiles for each week.

    This function takes in a dataset and calculates specified quantiles for each week of the year.
    It groups the data by week and computes the quantiles along the time dimension.

    Parameters:
    ds (xarray.Dataset): An xarray Dataset containing the climatology data.
    quantiles (list of float, optional): A list of quantiles to compute. Default is [0.05, 0.33, 0.5, 0.66, 0.95].

    Returns:
    xarray.Dataset: A Dataset with the calculated quantiles for each week.

    Implementation Steps:
    1. Group the dataset by the 'time.week' dimension.
    2. Calculate the specified quantiles along the 'time' dimension for each group.
    3. Return the resulting dataset with the quantiles.
    """
    pass


def determine_historic_value(historic_quantiles, current_value):
    differences = abs(historic_quantiles - current_value)
    closest_idx = differences.argmin(dim="quantile")
    return historic_quantiles.isel(quantile=closest_idx)
    """
    Determine the closest historic quantile value to the current value.

    This function takes in a dataset of historic quantiles and a current value,
    and returns the quantile value from the historic data that is closest to the current value.

    Parameters:
    historic_quantiles (xarray.DataArray): An xarray DataArray containing the historic quantiles.
                                           The DataArray should have a 'quantile' dimension.
    current_value (float): The current value for which we want to find the closest historic quantile.

    Returns:
    xarray.DataArray: The quantile value from the historic data that is closest to the current value.

    Implementation Steps:
    1. Calculate the absolute difference between each quantile value in `historic_quantiles` and `current_value`.
    2. Find the index of the minimum difference, which corresponds to the closest quantile.
    3. Use this index to select and return the closest quantile value from `historic_quantiles`.

    """

    pass


def convert_f_to_c(temp):
    return (temp - 32) * 5 / 9
    
    """
    Convert temperature from Fahrenheit to Celsius.

    This function takes a temperature value in Fahrenheit and converts it to Celsius using the formula:
    Celsius = (Fahrenheit - 32) * 5/9

    Parameters:
    temp (float): The temperature in Fahrenheit.

    Returns:
    float: The temperature converted to Celsius.
    """
    pass


# TODO: The main function is where you will tie everything together
#       and create the forecast for a USGS site. You will need to 
#       fill in the missing parts to complete the forecast.
def main():
    # TODO: Create an ArgumentParser object, with name `parser`
    #sites = ["09503000", "09504500"]
    parser = argparse.ArgumentParser(description="Streamflow Forecast Tool") # replace me
    # TODO:  add an argument for the USGS site number - default to '09506000'
    parser.add_argument(
        "--sites", type=str, 
        nargs="+",  # Accept one or more site numbers as a list
        default=["09506000"],  # Default to a single site if none are provided
        help="USGS site numbers (space-separated for multiple)"
    )
    #parser.add_argument("--site", type=str, default="09506000", help="USGS site number")
    # TODO:  Now make the parser parse the arguments
    args = parser.parse_args()
    # TODO:  Now pull the site number from the arguments
    sites = args.sites # replace me
    for site in sites:
        print(f"\nProcessing forecast for site: {site}")

    # Set some dates for the forecast, notably (nothing to do here):
    # - The data begin date
    # - The date today

    # - The forecast date
    data_begin_date = '2015-01-15'
    date_today = pd.to_datetime('today').floor('D').strftime('%Y-%m-%d')
    forecast_date = pd.to_datetime(date_today) + pd.Timedelta('7D')

    # TODO: Get the current week of the year as an integer
    current_week = pd.to_datetime(date_today).week # replace me

    # TODO: Get the forecast week of the year as an integer
    forecast_week = pd.to_datetime(forecast_date).week # replace me

    # Open the gage data (nothing to do here)
    
    #gage_data = open_gage_data(site)

    # TODO: Pull the site name from the gage data
    download_gage_data()
    gage_data = open_gage_data(site, './data/gagesII_9322_sept30_2011.shp')
    site_name = gage_data["STANAME"] # replace me

    # TODO: Pull the latitude from the gage data
    gage_lat = gage_data['LAT_GAGE'] # replace me

    # TODO: Pull the longitude from the gage data
    gage_lon = gage_data['LNG_GAGE'] # replace me

    # Use the provided functions to open the USGS and GFS data
    # NOTE: Nothing here needs doing, but it won't work unless
    #       the prior steps are completed to pull the dates/locations
    usgs_data = open_usgs_data(site, data_begin_date, date_today)
    print(usgs_data)
    gfs_data = open_gfs_data(gage_lat, gage_lon, data_begin_date, date_today)
    print(gfs_data)

    # Calculate climatology for streamflow, temperature, and precipitation
    # TODO: You need to implement the `process_climatology` function for this step
    gfs_climatology = process_climatology(gfs_data)
    usgs_climatology = process_climatology(usgs_data)

    # Now pull out the values for your forecast
    # NOTE: Nothing here needs doing, provided the prior steps are completed
    streamflow_climatology = usgs_climatology['streamflow'].compute()
    temperature_climatology = gfs_climatology['temperature_2m'].compute()
    precipitation_climatology = gfs_climatology['precipitation_surface'].compute()

    # Get the weather forecast for the gage location
    # NOTE: Nothing to do here, provided the function is imported correctly
    weather_forecast = get_weather_forecast(gage_lat, gage_lon)

    # TODO: Convert the temperature values in the weather forecast to Celsius
    # NOTE: You need to implement the `convert_f_to_c` function for this step
    weather_forecast['min_temp'] = convert_f_to_c(weather_forecast['min_temp'])
    weather_forecast['max_temp'] = convert_f_to_c(weather_forecast['max_temp'])

    # TODO: Calculate the probable accumulated precipitation and average temperature for the forecast
    # NOTE: You need to calculate the mean of the product of 'rain_amount' and 'rain_prob' for precipitation
    probable_accum_precip = np.mean(
        weather_forecast["rain_amount"] * weather_forecast["rain_prob"]
    )

    # TODO: Calculate the probable average temperature for the forecast
    # NOTE: You need to calculate the mean of the average temperature for the forecast
    probable_avg_temp = np.mean(
        (weather_forecast["min_temp"] + weather_forecast["max_temp"]) / 2
    )

    # TODO: Get the latest streamflow value from the USGS data
    # NOTE: You need to calculate the mean of the last 7 days of streamflow data
    latest_streamflow = usgs_data["streamflow"].isel(time=slice(-7, None)).mean()


    # TODO: You need to implement the `determine_historic_value` function for these steps
    # In order to do this you will need to first find the current timestamp in the climatology data
    # which encompasses the streamflow, temperature, and precipitation data. Basically you need to 
    # select the current or forecast week from the climatology data, as appropriate. 
    historic_streamflow_quantiles = streamflow_climatology.isel(week=current_week)
    forecast_streamflow_quantiles = streamflow_climatology.isel(week=forecast_week)
    forecast_temperature_quantiles = temperature_climatology.isel(week=current_week)
    forecast_precipitation_quantiles = precipitation_climatology.isel(week=forecast_week)


    # TODO: Now implement the `determine_historic_value` function to find the closest historic quantile.
    # The `determine_historic_value` function takes in the historic quantiles and the current value
    # and returns the quantile value from the historic data that is closest to the current value.
    current_streamflow_quantile = determine_historic_value(historic_streamflow_quantiles, latest_streamflow)
    forecast_streamflow_quantile = determine_historic_value(forecast_streamflow_quantiles, latest_streamflow)
    current_temperature_quantile = determine_historic_value(forecast_temperature_quantiles, probable_avg_temp)
    current_precipitation_quantile = determine_historic_value(forecast_precipitation_quantiles, probable_accum_precip)

    # Finally, print the forecast and statistics - nothing to do here
    # NOTE: You should use this function and its output to write your report
    # Make sure to consider all of the factors in your writeup, including:
    # - The current streamflow and its quantile
    # - The forecast streamflow and its quantile
    # - The probable accumulated precipitation and its quantile
    # - The probable average temperature and its quantile
    # - How these factors might affect the streamflow at the site
    print_forecast_and_statistics(
        site, 
        site_name, 
        date_today, 
        latest_streamflow,
        current_streamflow_quantile, 
        forecast_streamflow_quantile,
        probable_accum_precip, 
        current_precipitation_quantile,
        probable_avg_temp, 
        current_temperature_quantile
    )


# Do not modify the code below, I will use this to make 
# sure your code is working correctly. If you want more
# information about how this works, please see :
# https://realpython.com/python-main-function/
if __name__ == '__main__':
    main()
# %%
