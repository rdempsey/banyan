#!/usr/bin/env python
# encoding: utf-8
"""
BanyanDB.py
Created by Robert Dempsey on 12/30/14.
Copyright (c) 2014 Robert Dempsey. All rights reserved.
"""

import psycopg2
from time import strftime
from os import system

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

    # Save a forecast in the database
    def save_todays_forecast(self, forecast, weather):
        today = strftime("%Y-%m-%d")

        try:
            conn = psycopg2.connect(database="robertdempsey", user="robertdempsey", password="", host="localhost")
        except:
            system("say I'm unable to connect to the Banyan database")

        try:
            cur = conn.cursor()
            cur.execute("SET search_path TO 'banyan';")
            cur.execute("SELECT * from daily_forecasts WHERE forecast_date = %s", (today,))
            chk = cur.fetchone()
            if chk is None:
                cur.execute("INSERT INTO daily_forecasts (forecast_date, forecast, latitude, longitude, timezone) VALUES (%s,%s,%s,%s,%s)", (today,forecast,weather.latitude,weather.longitude,weather.timezone,))
        except IOError:
            system("say I am unable to save the forecast to the Banyan database")
            print("I am unable to save the forecast to the Banyan database")
        finally:
            conn.close()
            return "Forecast saved"

    # Get the current day's weather forecast from the database; return none if none is found
    def get_todays_weather_forecast(self):
        today = strftime("%Y-%m-%d")

        try:
            conn = psycopg2.connect(database="robertdempsey", user="robertdempsey", password="", host="localhost")
        except:
            system("say I'm unable to connect to the Banyan database")

        try:
            cur = conn.cursor()
            cur.execute("SET search_path TO 'banyan';")
            cur.execute("SELECT forecast FROM daily_forecasts WHERE forecast_date = %s;", (today,))
            forecast = cur.fetchone()
            if forecast is None:
                return None
            else:
                return forecast[0]
        except IOError:
            system("say I am unable to get today's weather from the Banyan database")
        conn.close()

    # Given an app name it returns the path to the application
    def get_app_by_name(self, app_name):
        try:
            conn = psycopg2.connect(database="robertdempsey", user="robertdempsey", password="", host="localhost")
        except:
            system("say I'm unable to connect to the Banyan database")
        cur = conn.cursor()
        try:
            cur.execute("SET search_path TO 'banyan';")
            cur.execute("SELECT * FROM local_apps WHERE app_name = %s;", (app_name,))
            app = cur.fetchone()
            if app is None:
                return None
            else:
                return app[2]
        except IOError:
            system("say I am unable to get application information from the Banyan database")
        finally:
            conn.close()



    # Given a file name it returns the path to the file
    def get_file_by_name(self, file_name):
        try:
            conn = psycopg2.connect(database="robertdempsey", user="robertdempsey", password="", host="localhost")
        except:
            system("say I'm unable to connect to the Banyan database")
        cur = conn.cursor()
        try:
            cur.execute("SET search_path TO 'banyan';")
            cur.execute("SELECT file_path FROM local_files WHERE file_name = %s;", (file_name,))
            app = cur.fetchone()
            if app is None:
                return None
            else:
                return app[0]
        except IOError:
            system("say I am unable to get file information from the Banyan database")
        finally:
            conn.close()

if __name__ == '__main__':
    pass