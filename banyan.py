#!/usr/bin/env python
# encoding: utf-8
"""
banyan.py
Created by Robert Dempsey on 12/30/14.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

from os import system
import os
import cmd
import time
from bin.Greeting import *
from bin.AppState import *
from bin.Weather import *
from apscheduler.schedulers.background import BackgroundScheduler

# Get the application configuration
def get_app_config():
    config = configparser.ConfigParser(interpolation = configparser.ExtendedInterpolation())
    config.read('config/config.ini')
    return config

# Get the user's greeting
def get_users_greeting():
    config = get_app_config()
    return config['Default']['greeting']


# Get the greeting for the user
def greet_the_user(app_state):
    current_time = int(time.strftime("%H"))
    greeting = get_users_greeting()
    g = Greeting(app_state, current_time, greeting)
    g.greet_the_user(app_state)

# Say goodbye to the user
def say_goodbye():
    greeting = get_users_greeting()
    system('say Good bye {}'.format(greeting))

def get_the_weather_forecast():
    GetDailyWeatherForecast().start()

class Banyan(cmd.Cmd):
    intro = 'Welcome to Banyan. Type help or ? to list commands.\n'
    prompt = 'Banyan > '
    app_state = AppState()
    scheduler = BackgroundScheduler()

    # When Banyan starts, greet the user
    def preloop(self):
        # Restore the application state
        self.app_state.restore_application_state()
        # Start the task scheduler to get the current forecast. Run it every 30 minutes
        self.scheduler.add_job(get_the_weather_forecast, 'interval', seconds=1800)
        self.scheduler.start()
        # Greet the user
        greet_the_user(self.app_state)

    # On exit, save the application state and say goodbye
    def postloop(self):
        self.app_state.save_application_state()
        say_goodbye()

    def do_good(self, arg):
        'Say hello to Banyan and Banyan will say hello to you: GOOD {morning|afternoon|evening}'
        greet_the_user(self.app_state)

    def do_current(self, arg):
        ' Get the current weather or the weather forecast for the day: CURRENT {weather|forecast}'
        if arg.lower() == "weather":
            CurrentWeather().start()
        elif arg.lower() == "forecast":
            CurrentForecast().start()

    def do_restart(self, arg):
        'Immediately saves the application state and restarts Banyan: RESTART'
        config = get_app_config()
        file = config['FileLocations']['scripts'] + "restart.sh"
        self.app_state.save_application_state()
        os.execl(file, '')

    def do_bye(self, arg):
        'Close Banyan and exit: GOODBYE'
        self.scheduler.shutdown()
        return True


def main():
    Banyan().cmdloop()


if __name__ == '__main__':
    main()