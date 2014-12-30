#!/usr/bin/env python
# encoding: utf-8
"""
get_the_weather_report.py
Created by Robert Dempsey on 12/30/14.
Copyright (c) 2014 Robert Dempsey. All rights reserved.
"""

import configparser
from lib.Weather import *
from lib.BanyanDB import *


def main():
    config = configparser.ConfigParser(interpolation = configparser.ExtendedInterpolation())
    config.read('../config/config.ini')
    ak = config['ForecastIO']['api_key']
    lat = config['ForecastIO']['h_lat']
    lng = config['ForecastIO']['h_long']

    w = Weather()
    w.api_key = ak
    w.latitude = lat
    w.longitude = lng

    # Get the forecast for the day
    f = w.get_todays_forecast()
    print(f)

    d = BanyanDB()
    d.database = config['BanyanDatabase']['db']
    print("Database: {}".format(d.database))
    d.save_todays_forecast(f)


if __name__ == '__main__':
    main()