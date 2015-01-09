#!/usr/bin/env python
# encoding: utf-8
"""
Greeting.py
Created by robertdempsey on 1/9/15.
Copyright (c) 2015 robertdempsey. All rights reserved.
"""

from os import system
from peak.rules import abstract, when, around, before, after
from bin.Weather import *
import threading
from tzlocal import get_localzone

single_lock = threading.Lock()

class CurrentWeather(threading.Thread):
    # Get the current weather report
    def run(self):
        single_lock.acquire()
        config = configparser.ConfigParser(interpolation = configparser.ExtendedInterpolation())
        config.read('config/config.ini')

        ak = config['ForecastIO']['api_key']
        lat = config['ForecastIO']['h_lat']
        lng = config['ForecastIO']['h_long']

        w = Weather()
        w.api_key = ak
        w.latitude = lat
        w.longitude = lng
        w.timezone = str(get_localzone())

        system('say {}'.format(w.get_the_current_weather_report()))
        single_lock.release()

class Greeting:
    def __init__(self, current_time, greeting, notified_of_the_weather):
        self.current_time = current_time
        self.greeting = greeting
        self.notified_of_the_weather = notified_of_the_weather

    ## RULES ##

    # @abstract()
    def greet_the_user(self):
        """ A generic function for greeting the user """

    # Between midnight and noon is morning
    @when(greet_the_user, "0<self.current_time and self.current_time<12")
    def morning_greeting(self):
        system('say {} {}'.format("Good morning", self.greeting))

    # Between noon and 5 is afternoon
    @when(greet_the_user, "12<=self.current_time and self.current_time<17")
    def afternoon_greeting(self):
        system('say {} {}'.format("Good afternoon", self.greeting))

    # Between 5 and midnight is evening
    @when(greet_the_user, "17>=self.current_time and self.current_time<=24")
    def evening_greeting(self):
        system('say {} {}'.format("Good evening", self.greeting))

    # When the user hasn't been notified of the current weather
    @after(greet_the_user, "self.notified_of_the_weather==0")
    def weather_greeting(self):
        CurrentWeather().start()

if __name__ == '__main__':
    pass