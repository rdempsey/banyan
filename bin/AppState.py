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
            self.create_initial_state_file()

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

    # Whether or not the user has been greeted. Default: false
    # On restart, we don't need to greet the user again.
    @property
    def user_greeted(self):
        return self.properties.get('user_greeted', False)

    @user_greeted.setter
    def user_greeted(self, s):
        self.properties['user_greeted'] = s

    @user_greeted.deleter
    def user_greeted(self):
        del self.properties['user_greeted']


    # Create an initial state file and set defaults
    def create_initial_state_file(self):
        shelf_file = shelve.open('config/app_state')
        shelf_file['date_of_last_weather_notification'] = '1900-01-01'
        shelf_file['user_greeted'] = False
        shelf_file.close()

    # Save the application state using shelve
    def save_application_state(self):
        shelf_file = shelve.open('config/app_state')
        shelf_file['date_of_last_weather_notification'] = self.date_of_last_weather_notification
        shelf_file['user_greeted'] = self.user_greeted
        shelf_file.close()

    # Restore the application state using shelve
    def restore_application_state(self):
        shelf_file = shelve.open('config/app_state')
        self.date_of_last_weather_notification = shelf_file['date_of_last_weather_notification']
        self.user_greeted = shelf_file['user_greeted']
        shelf_file.close()