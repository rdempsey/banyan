#!/usr/bin/env python
# encoding: utf-8
"""
AppState.py
Created by Robert Dempsey on 1/9/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

import shelve
import os.path

class AppState:
    def __init__(self, **kwargs):
        self.properties = kwargs
        if not os.path.exists('config/app_state.db'):
            print("Creating a new state file")
            self.create_initial_state_file()

    # Whether or not the user was notified of the weather
    @property
    def notified_of_the_weather(self):
        return self.properties.get('notified_of_the_weather', 'None')

    @notified_of_the_weather.setter
    def notified_of_the_weather(self, s):
        self.properties['notified_of_the_weather'] = s

    @notified_of_the_weather.deleter
    def notified_of_the_weather(self):
        del self.properties['notified_of_the_weather']

    # Whether or not the user was notified of the forecast
    @property
    def notified_of_the_forecast(self):
        return self.properties.get('notified_of_the_forecast', 'None')

    @notified_of_the_forecast.setter
    def notified_of_the_forecast(self, s):
        self.properties['notified_of_the_forecast'] = s

    @notified_of_the_forecast.deleter
    def notified_of_the_forecast(self):
        del self.properties['notified_of_the_forecast']

    # The date on which the user was last notified about the weather
    @property
    def date_of_last_weather_notification(self):
        return self.properties.get('date_of_last_weather_notification', 'None')

    @date_of_last_weather_notification.setter
    def date_of_last_weather_notification(self, s):
        self.properties['date_of_last_weather_notification'] = s

    @date_of_last_weather_notification.deleter
    def date_of_last_weather_notification(self):
        del self.properties['date_of_last_weather_notification']

    # The date on which the user was last notified of the forecast
    @property
    def date_of_last_forecast_notification(self):
        return self.properties.get('date_of_last_forecast_notification', 'None')

    @date_of_last_forecast_notification.setter
    def date_of_last_forecast_notification(self, s):
        self.properties['date_of_last_forecast_notification'] = s

    @date_of_last_forecast_notification.deleter
    def date_of_last_forecast_notification(self):
        del self.properties['date_of_last_forecast_notification']

    def create_initial_state_file(self):
        shelf_file = shelve.open('config/app_state')
        shelf_file['notified_of_the_weather'] = 0
        shelf_file['notified_of_the_forecast'] = 0
        shelf_file['date_of_last_weather_notification'] = 'Never'
        shelf_file['date_of_last_forecast_notification'] = 'Never'
        shelf_file.close()

    # Save the application state using shelve
    def save_application_state(self):
        shelf_file = shelve.open('config/app_state')
        shelf_file['notified_of_the_weather'] = self.notified_of_the_weather
        shelf_file['notified_of_the_forecast'] = self.notified_of_the_forecast
        shelf_file['date_of_last_weather_notification'] = self.date_of_last_weather_notification
        shelf_file['date_of_last_forecast_notification'] = self.date_of_last_forecast_notification
        shelf_file.close()

    # Restore the application state using shelve
    def restore_application_state(self):
        shelf_file = shelve.open('config/app_state')
        self.notified_of_the_weather = shelf_file['notified_of_the_weather']
        self.notified_of_the_forecast = shelf_file['notified_of_the_forecast']
        self.date_of_last_weather_notification = shelf_file['date_of_last_weather_notification']
        self.date_of_last_forecast_notification = shelf_file['date_of_last_forecast_notification']
        shelf_file.close()