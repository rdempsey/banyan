#!/usr/bin/env python
# encoding: utf-8
"""
BanyanDB.py
Created by Robert Dempsey on 12/30/14.
Copyright (c) 2014 Robert Dempsey. All rights reserved.
"""

import os
import sqlite3
import configparser
from datetime import datetime
from time import strftime

class BanyanDB:
    def __init__(self, **kwargs):
        self.properties = kwargs

    # Database
    @property
    def database(self):
        return self.properties.get('database', 'None')

    @database.setter
    def database(self, db):
        self.properties['database'] = db

    @database.deleter
    def database(self):
        del self.properties['database']

    def save_todays_forecast(self, forecast, weather):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        today = strftime("%Y-%m-%d")

        now = str(datetime.now())
        try:
            cursor.execute('SELECT * FROM daily_forecasts WHERE date=?', (today,))
            chk = cursor.fetchone()
            if chk is None:
                cursor.execute("INSERT INTO daily_forecasts (date, forecast, latitude, longitude, timezone, created_at, updated_at) VALUES (?,?,?,?,?,?,?)", (today,forecast,weather.latitude,weather.longitude,weather.timezone,now,now))
                conn.commit()
        except IOError:
            return "Unable to insert the forecast into the database."
        finally:
            conn.close()
            return "Forecast saved"

    def get_todays_weather_forecast(self):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        today = strftime("%Y-%m-%d")

        try:
            cursor.execute('SELECT forecast FROM daily_forecasts WHERE date=?', (today,))
            forecast = cursor.fetchone()
            if forecast is None:
                return None
            else:
                return forecast[0]
        except IOError:
            return "Unable to connect to the Banyan database. Please check the settings and try again."
        finally:
            conn.close()

if __name__ == '__main__':
    pass