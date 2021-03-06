#!/usr/bin/env python
# encoding: utf-8
"""
Weather.py
Created by Robert Dempsey on 12/30/14.
Copyright (c) 2014 Robert Dempsey. All rights reserved.
"""

from os import system
import forecastio
import threading
import time
from tzlocal import get_localzone
from bin.BanyanDB import *
from bin.configs import *
from bin.banyan_logger import log_message
from bin.text_cleaner import *

single_lock = threading.Lock()

# Return a weather object
def get_a_weather_object():
    config = get_app_config()
    w = Weather()
    w.api_key = config['ForecastIO']['api_key']
    w.latitude = config['ForecastIO']['h_lat']
    w.longitude = config['ForecastIO']['h_long']
    w.timezone = str(get_localzone())
    return w


# Say the current weather report
class SayCurrentWeather(threading.Thread):
    # Get the current weather report
    def run(self):
        log_message("Weather/SayCurrentWeather", "Saying the current weather report")
        single_lock.acquire()
        w = get_a_weather_object()
        system('say {}'.format(w.get_the_current_weather_report()))
        single_lock.release()


# Say the current weather forecast
class SayCurrentForecast(threading.Thread):
    # Get the current weather report
    def run(self):
        log_message("Weather/SayCurrentForecast", "Saying the current weather forecast")
        single_lock.acquire()
        w = get_a_weather_object()
        system('say {}'.format(w.get_the_current_forecast()))
        single_lock.release()


# Get the current weather forecast; used by a scheduled task for retrieving the latest forecast
class GetCurrentForecast(threading.Thread):
    # Get the current weather report
    def run(self):
        w = get_a_weather_object()
        w.get_the_current_forecast()


# Weather class
class Weather:
    def __init__(self, **kwargs):
        self.properties = kwargs

    # Forecast.io API Key
    @property
    def api_key(self):
        return self.properties.get('api_key', 'None')

    @api_key.setter
    def api_key(self, s):
        self.properties['api_key'] = s

    @api_key.deleter
    def api_key(self):
        del self.properties['api_key']

    # Latitude
    @property
    def latitude(self):
        return self.properties.get('latitude', 'None')

    @latitude.setter
    def latitude(self, lat):
        self.properties['latitude'] = lat

    @latitude.deleter
    def lat(self):
        del self.properties['latitude']

    # Longitude
    @property
    def longitude(self):
        return self.properties.get('longitude', 'None')

    @longitude.setter
    def longitude(self, lng):
        self.properties['longitude'] = lng

    @longitude.deleter
    def longitude(self):
        del self.properties['longitude']

    # Timezone
    @property
    def timezone(self):
        return self.properties.get('timezone', 'None')

    @timezone.setter
    def timezone(self, lng):
        self.properties['timezone'] = lng

    @timezone.deleter
    def timezone(self):
        del self.properties['timezone']

    lower = str.lower

    # Get the current weather report from Forecast.io
    def get_the_current_weather_report(self):
        try:
            log_message("Weather/GetCurrentWeatherReport", "Retrieving the current weather report")
            forecast = forecastio.load_forecast(self.api_key, self.latitude, self.longitude)
            c = forecast.currently()
            c_temp = int(round(c.temperature))
            c_summary = c.summary.lower()
            c_precip = int(round(c.precipProbability * 100))
            return "It is currently {} degrees and {} with a {} percent chance of precipitation.".format(c_temp, c_summary, c_precip)
        except:
            # TODO: handle the can't get to Forecast.io error
            log_message("Weather/GetCurrentWeatherReport", "Unable to retrieve the current weather report")
            system('say I am unable to retrieve the current weather report')
            pass

    # Get the current forecast; if it's in the database use that, otherwise go to Forecast.io and get the latest
    def get_the_current_forecast(self):
        log_message("Weather/GetCurrentForecast", "Getting the current weather forecast")
        # Check the database to see if we already have the current forecast
        d = BanyanDB()
        current_forecast = d.get_todays_weather_forecast()
        # If not, fetch it from Forecast.io, save it and return it
        if current_forecast is None:
            try:
                log_message("Weather", "Retrieving the current weather forecast")
                f = forecastio.load_forecast(self.api_key, self.latitude, self.longitude)
                forecast = f.daily()
                f_summary = forecast.data[0].summary[:-1].lower()
                # Update the string they gave us
                f_summary = unicode_weather_cleaner(f_summary)
                # Get the rest of the temps for the day
                f_min_temp = int(round(forecast.data[0].temperatureMin))
                f_max_temp = int(round(forecast.data[0].temperatureMax))
                # Create the forecast
                t_forecast = "It is going to be {} with temperatures between {} and {} degrees".format(f_summary, f_min_temp, f_max_temp)
                # Save the forecast
                d.save_todays_forecast(t_forecast, self)
                # Return it
                return t_forecast
            except:
                # TODO: handle can't get to Forecast.io error
                log_message("Weather/GetCurrentForecast", "Unable to retrieve the current weather forecast")
                system('say I am unable to retrieve the current weather forecast')
                pass
        else:
            return current_forecast


if __name__ == '__main__':
    pass