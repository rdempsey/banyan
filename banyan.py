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


def say_hello():
    config = configparser.ConfigParser(interpolation = configparser.ExtendedInterpolation())
    config.read('config/config.ini')
    g = config['Default']['Greeting']

    current_time = int(strftime("%H"))
    if 0 < current_time < 12:
        greeting = "Good morning {}.".format(g)
    elif 12 < current_time < 17:
        greeting = "Good afternoon {}.".format(g)
    else:
        greeting = "Good evening {}.".format(g)

    system('say {}'.format(greeting))



def get_the_current_weather():
    config = configparser.ConfigParser(interpolation = configparser.ExtendedInterpolation())
    config.read('config/config.ini')
    ak = config['ForecastIO']['api_key']
    lat = config['ForecastIO']['h_lat']
    lng = config['ForecastIO']['h_long']

    w = Weather()
    w.api_key = ak
    w.latitude = lat
    w.longitude = lng

    # Get the current weather report
    c = w.get_current_weather()
    system('say {}'.format(c))


def main():
    say_hello()


if __name__ == '__main__':
    main()