#!/usr/bin/env python
# encoding: utf-8
"""
banyan.py
Created by Robert Dempsey on 12/30/14.
Copyright (c) 2014 Robert Dempsey. All rights reserved.
"""

from os import system
from time import strftime
from lib.Weather import *
from lib.BanyanDB import *

# Get the application configuration
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

    return w

# Get the greeting for the user
def get_the_users_greeting():
    config = get_app_config()
    g = config['Default']['Greeting']
    current_time = int(strftime("%H"))
    if 0 < current_time < 12:
        greeting = "Good morning {}.".format(g)
    elif 12 < current_time < 17:
        greeting = "Good afternoon {}.".format(g)
    else:
        greeting = "Good evening {}.".format(g)

    return greeting


# Get the current weather report
def get_the_current_weather():
    w = get_a_weather_object()
    return w.get_the_current_weather_report()

# Get the current weather report
def get_the_current_forecast():
    db = get_banyan_db()
    w = get_a_weather_object()
    return w.get_the_current_forecast(db)


def say_hello():
    db = get_banyan_db()
    w = get_a_weather_object()

    # Say hello to the user
    system('say {}'.format(get_the_users_greeting()))

    # Get the current weather report
    system('say {}'.format(w.get_the_current_weather_report()))

    # Get today's forecast
    system('say {}'.format(w.get_the_current_forecast(db)))


def main():
    say_hello()


if __name__ == '__main__':
    main()