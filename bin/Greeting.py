#!/usr/bin/env python
# encoding: utf-8
"""
Greeting.py
Created by Robert Dempsey on 1/9/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

from os import system
from peak.rules import abstract, when, around, before, after
from bin.Weather import *
import threading
import time
from tzlocal import get_localzone

single_lock = threading.Lock()

# Get the application config file
def get_app_config():
    config = configparser.ConfigParser(interpolation = configparser.ExtendedInterpolation())
    config.read('config/config.ini')
    return config

# Get the path to the BanyanDB file
def get_banyan_db():
    config = get_app_config()
    return config['BanyanDatabase']['db']

# Get a weather object to work with
def get_a_weather_object():
    config = get_app_config()
    ak = config['ForecastIO']['api_key']
    lat = config['ForecastIO']['h_lat']
    lng = config['ForecastIO']['h_long']

    w = Weather()
    w.api_key = ak
    w.latitude = lat
    w.longitude = lng
    w.timezone = str(get_localzone())

    return w

# Say the current weather report
class CurrentWeather(threading.Thread):
    # Get the current weather report
    def run(self):
        single_lock.acquire()
        config = get_app_config()
        w = get_a_weather_object()
        system('say {}'.format(w.get_the_current_weather_report()))
        single_lock.release()

# Say the current weather forecast
class CurrentForecast(threading.Thread):
    # Get the current weather report
    def run(self):
        single_lock.acquire()
        db = get_banyan_db()
        w = get_a_weather_object()
        system('say {}'.format(w.get_the_current_forecast(db)))
        single_lock.release()


class Greeting:
    def __init__(self, app_state, current_time, greeting):
        self.current_time = current_time
        self.greeting = greeting
        self.app_state = app_state

    ## RULES ##

    # @abstract()
    def greet_the_user(self, app_state):
        """ A generic function for greeting the user """

    # Between midnight and noon is morning
    @when(greet_the_user, "0<self.current_time and self.current_time<12")
    def morning_greeting(self, app_state):
        system('say {} {}'.format("Good morning", self.greeting))

    # Between noon and 5 is afternoon
    @when(greet_the_user, "12<=self.current_time and self.current_time<17")
    def afternoon_greeting(self, app_state):
        system('say {} {}'.format("Good afternoon", self.greeting))

    # Between 5 and midnight is evening
    @when(greet_the_user, "17<=self.current_time and self.current_time<=24")
    def evening_greeting(self, app_state):
        system('say {} {}'.format("Good evening", self.greeting))

    # If it's in the morning, and the user hasn't yet heard the weather and forecast, tell them
    @after(greet_the_user, "0<self.current_time and self.current_time<12 and self.app_state.date_of_last_weather_notification<str(time.strftime('%Y-%m-%d'))")
    def weather_greeting(self, app_state):
        CurrentWeather().start()
        CurrentForecast().start()
        app_state.date_of_last_weather_notification = str(time.strftime("%Y-%m-%d"))

if __name__ == '__main__':
    pass