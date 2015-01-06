#!/usr/bin/env python
# encoding: utf-8
"""
banyan.py
Created by Robert Dempsey on 12/30/14.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

from os import system
import cmd
import threading
import time
from tzlocal import get_localzone
from lib.Weather import *
from lib.BanyanDB import *
import readline

single_lock = threading.Lock()

# Get the application configuration
def get_app_config():
    config = configparser.ConfigParser(interpolation = configparser.ExtendedInterpolation())
    config.read('config/config.ini')
    return config

# Get the path to the BanyanDB file
def get_banyan_db():
    config = get_app_config()
    return config['BanyanDatabase']['db']


# Get the local timezone
def get_local_timezone():
    return str(get_localzone())


# Get the greeting for the user
def say_hello():
    config = get_app_config()
    g = config['Default']['greeting']
    current_time = int(time.strftime("%H"))
    if 0 < current_time < 12:
        greeting = "Good morning {}.".format(g)
    elif 12 <= current_time < 17:
        greeting = "Good afternoon {}.".format(g)
    else:
        greeting = "Good evening {}.".format(g)

    system('say {}'.format(greeting))

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
    w.timezone = get_local_timezone()

    return w


class CurrentWeather(threading.Thread):
    # Get the current weather report
    def run(self):
        single_lock.acquire()
        w = get_a_weather_object()
        system('say {}'.format(w.get_the_current_weather_report()))
        single_lock.release()


class CurrentForecast(threading.Thread):
    # Get the current weather report
    def run(self):
        single_lock.acquire()
        db = get_banyan_db()
        w = get_a_weather_object()
        system('say {}'.format(w.get_the_current_forecast(db)))
        single_lock.release()


class Banyan(cmd.Cmd):
    intro = 'Welcome to Banyan. Type help or ? to list commands.\n'
    prompt = 'Banyan > '

    def do_goodbye(self, arg):
        'Close Banyan and exit: GOODBYE'
        print('Thank you for using Banyan')
        return True

    def do_good(self, arg):
        'Say hello: GOOD {morning, afternoon, evening}'
        say_hello()

    def do_current(self, arg):
        ' Get the current weather or weather forecast: CURRENT {weather, forecast}'
        if arg.lower() == "weather":
            CurrentWeather().start()
        elif arg.lower() == "forecast":
            CurrentForecast().start()

def main():
    Banyan().cmdloop()


if __name__ == '__main__':
    main()