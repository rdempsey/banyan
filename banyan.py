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
import webbrowser
from bin.Greeting import *
from bin.AppState import *
from bin.Weather import *
from bin.Mailer import *
from bin.google import search
from apscheduler.schedulers.background import BackgroundScheduler
from birdy.twitter import UserClient

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
    current_date = str(strftime('%Y-%m-%d'))
    greeting = get_users_greeting()
    g = Greeting(app_state, current_time, current_date, greeting)
    g.greet_the_user(app_state)


# Say goodbye to the user
def say_goodbye():
    greeting = get_users_greeting()
    system('say Good bye {}'.format(greeting))

##
# Scheduled Tasks
##

# Get the current weather forecast; happens every 30 minutes
def get_the_weather_forecast():
    GetCurrentForecast().start()


# Save the application state; happens every 30 seconds
def save_the_application_state(app_state):
    app_state.save_application_state()


# Reset the user greeting; checks every 10 minutes but resets once per day
def reset_user_greeted(app_state):
    if str(strftime('%Y-%m-%d')) > app_state.date_of_last_weather_notification and app_state.user_greeted is True:
        app_state.user_greeted = False


##
# Banyan
##

class Banyan(cmd.Cmd):
    intro = 'Welcome to Banyan. Type help or ? to list commands.\n'
    prompt = 'Banyan > '
    app_state = AppState()
    scheduler = BackgroundScheduler()

    def preloop(self):
        self.app_state.restore_application_state()
        self.scheduler.add_job(get_the_weather_forecast, 'interval', seconds=1800)
        self.scheduler.add_job(save_the_application_state, trigger='interval', kwargs={"app_state":self.app_state}, seconds=60)
        self.scheduler.add_job(reset_user_greeted, trigger='interval', kwargs={"app_state":self.app_state}, seconds=600)
        self.scheduler.start()
        greet_the_user(self.app_state)

    def postloop(self):
        self.app_state.save_application_state()
        say_goodbye()

    def do_good(self, arg):
        """Say hello to Banyan and Banyan will say hello to you: GOOD {morning|afternoon|evening}"""
        greet_the_user(self.app_state)

    def do_current(self, arg):
        """Get the current weather or the weather forecast for the day: CURRENT {weather|forecast}"""
        if arg.lower() == "weather":
            SayCurrentWeather().start()
        elif arg.lower() == "forecast":
            SayCurrentForecast().start()

    def do_check(self, arg):
        """Check email: CHECK {email}"""
        if arg.lower() == "email":
            SayGmailCount().start()
            SayADSCount().start()
            SayDC2Count().start()

    def do_search(self, arg):
        """Search Google for the given query and open the first 10 results in Chrome: SEARCH {query}"""
        s_query = arg.lower()
        for url in search(s_query, stop=10):
            webbrowser.open_new_tab(url)

    def do_restart(self, arg):
        """Immediately saves the application state and restarts Banyan: RESTART"""
        config = get_app_config()
        file = config['FileLocations']['scripts'] + "restart.sh"
        self.app_state.save_application_state()
        os.execl(file, '')

    def do_bye(self, arg):
        """Close Banyan and exit: GOODBYE"""
        self.scheduler.shutdown()
        return True


def main():
    Banyan().cmdloop()


if __name__ == '__main__':
    main()