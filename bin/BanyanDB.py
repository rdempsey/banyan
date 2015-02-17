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
from bin.banyan_logger import log_message

class BanyanDB:
    def __init__(self, **kwargs):
        self.properties = kwargs
        self.connect_message = "Connecting to the Banyan database"
        self.connection_error_message = "Unable to connect to the Banyan database"
        self.closing_message = "Closing the connection to the Banyan database"

    # Save a forecast in the database
    def save_todays_forecast(self, forecast, weather):
        today = strftime("%Y-%m-%d")

        try:
            log_message("BanyanDB/SaveTodaysForecast", self.connect_message)
            conn = psycopg2.connect(database="robertdempsey", user="robertdempsey", password="", host="localhost")
        except:
            log_message("BanyanDB/SaveTodaysForecast", self.connection_error_message)
            system("say I am unable to connect to the Banyan database")

        try:
            cur = conn.cursor()
            cur.execute("SET search_path TO 'banyan';")
            cur.execute("SELECT * from daily_forecasts WHERE forecast_date = %s", (today,))
            chk = cur.fetchone()
            if chk is None:
                log_message("BanyanDB/SaveTodaysForecast", "Saving the forecast to the Banyan database")
                cur.execute("INSERT INTO daily_forecasts (forecast_date, forecast, latitude, longitude, timezone) VALUES (%s,%s,%s,%s,%s)", (today,forecast,weather.latitude,weather.longitude,weather.timezone,))
                conn.commit()
        except IOError:
            log_message("BanyanDB/SaveTodaysForecast", "Unable to save the forecast to the Banyan database")
            system("say I am unable to save the forecast to the Banyan database")
        finally:
            log_message("BanyanDB/SaveTodaysForecast", self.closing_message)
            conn.close()

    # Get the current day's weather forecast from the database; return none if none is found
    def get_todays_weather_forecast(self):
        today = strftime("%Y-%m-%d")

        try:
            log_message("BanyanDB/GetTodaysWeatherForecast", self.connect_message)
            conn = psycopg2.connect(database="robertdempsey", user="robertdempsey", password="", host="localhost")
        except:
            log_message("BanyanDB/GetTodaysWeatherForecast", self.connection_error_message)
            system("say I'm unable to connect to the Banyan database")

        try:
            log_message("BanyanDB/GetTodaysWeatherForecast", "Retrieving the current weather forecast from the Banyan database")
            cur = conn.cursor()
            cur.execute("SET search_path TO 'banyan';")
            cur.execute("SELECT forecast FROM daily_forecasts WHERE forecast_date = %s;", (today,))
            forecast = cur.fetchone()
            if forecast is None:
                return None
            else:
                return forecast[0]
        except IOError:
            log_message("BanyanDB/GetTodaysWeatherForecast", "Unable to retrieve the current weather forecast from the Banyan database")
            system("say I am unable to get today's weather forecast from the Banyan database")
        finally:
            log_message("BanyanDB/GetTodaysWeatherForecast", self.closing_message)
            conn.close()

    # Given an app name it returns the path to the application
    def get_app_by_name(self, app_name):
        try:
            log_message("BanyanDB/GetAppByName", self.connect_message)
            conn = psycopg2.connect(database="robertdempsey", user="robertdempsey", password="", host="localhost")
        except:
            log_message("BanyanDB/GetAppByName", self.connection_error_message)
            system("say I'm unable to connect to the Banyan database")

        cur = conn.cursor()

        try:
            log_message("BanyanDB/GetAppByName", "Retrieving the path to application {} from the database".format(app_name))
            cur.execute("SET search_path TO 'banyan';")
            cur.execute("SELECT * FROM local_apps WHERE app_name = %s;", (app_name,))
            app = cur.fetchone()
            if app is None:
                return None
            else:
                return app[2]
        except IOError:
            log_message("BanyanDB/GetAppByName", "Unable to retrieve the path to application {} from the Banyan database".format(app_name))
            system("say I am unable to retrieve the application path from the Banyan database")
        finally:
            log_message("BanyanDB/GetAppByName", self.closing_message)
            conn.close()



    # Given a file name it returns the path to the file
    def get_file_by_name(self, file_name):
        try:
            log_message("BanyanDB/GetFileByName", self.connect_message)
            conn = psycopg2.connect(database="robertdempsey", user="robertdempsey", password="", host="localhost")
        except:
            log_message("BanyanDB/GetFileByName", self.connection_error_message)
            system("say I'm unable to connect to the Banyan database")

        cur = conn.cursor()

        try:
            log_message("BanyanDB/GetFileByName", "Retrieving the path to file {} from the Banyan database".format(file_name))
            cur.execute("SET search_path TO 'banyan';")
            cur.execute("SELECT file_path FROM local_files WHERE file_name = %s;", (file_name,))
            app = cur.fetchone()
            if app is None:
                return None
            else:
                return app[0]
        except IOError:
            log_message("BanyanDB/GetFileByName", "Unable to retrieve the path for {} from the Banyan database".format(file_name))
            system("say I am unable to retrieve the file path from the Banyan database")
        finally:
            log_message("BanyanDB/GetFileByName", self.closing_message)
            conn.close()

if __name__ == '__main__':
    pass