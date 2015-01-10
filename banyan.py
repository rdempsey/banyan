#!/usr/bin/env python
# encoding: utf-8
"""
banyan.py
Created by Robert Dempsey on 12/30/14.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

from os import system
import cmd
import time
from bin.Greeting import *
from bin.AppState import *

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
def say_hello(app_state):
    current_time = int(time.strftime("%H"))
    greeting = get_users_greeting()
    g = Greeting(app_state, current_time, greeting)
    g.greet_the_user(app_state)

# Say goodbye to the user
def say_goodbye():
    greeting = get_users_greeting()
    system('say Good bye {}'.format(greeting))


class Banyan(cmd.Cmd):
    intro = 'Welcome to Banyan. Type help or ? to list commands.\n'
    prompt = 'Banyan > '
    app_state = AppState()

    def show_app_state(self):
        print("date_of_last_weather_notification: {}".format(self.app_state.date_of_last_weather_notification))

    def preloop(self):
        # When the user logs on, say hello
        self.app_state.restore_application_state()
        say_hello(self.app_state)

    def postloop(self):
        self.app_state.save_application_state()
        self.show_app_state()
        say_goodbye()

    def do_good(self, arg):
        say_hello(self.app_state)

    def do_bye(self, arg):
        'Close Banyan and exit: GOODBYE'
        return True

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