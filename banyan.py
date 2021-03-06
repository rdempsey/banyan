#!/usr/bin/env python
# encoding: utf-8
"""
banyan.py
Created by Robert Dempsey on 12/30/14.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

import rlcompleter, readline
readline.parse_and_bind('tab:complete')
from os import system
import cmd
from time import strftime
from bin.configs import *
from bin.banyan_logger import log_message
from bin.Greeting import *
from bin.AppState import *
from bin.BanyanParser import *
from apscheduler.schedulers.background import BackgroundScheduler


# Get the greeting for the user
def greet_the_user(app_state):
    current_time = int(time.strftime("%H"))
    current_date = str(strftime('%Y-%m-%d'))
    greeting = get_users_greeting()
    g = Greeting(app_state, current_time, current_date, greeting)
    g.greet_the_user(app_state)


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
        log_message("Banyan/ResetUserGreeted", "Resetting user greeted")
        app_state.user_greeted = False


##
# Banyan
##

class Banyan(cmd.Cmd):
    prompt = 'Banyan > '
    app_state = AppState()
    scheduler = BackgroundScheduler()

    lower = str.lower


    # Do these when Banyan starts
    def preloop(self):
        """Actions to take when Banyan starts"""
        self.app_state.restore_application_state()

        log_message("Banyan/PreLoop", "Adding background jobs to the scheduler")
        self.scheduler.add_job(get_the_weather_forecast, 'interval', seconds=1800)
        self.scheduler.add_job(save_the_application_state, trigger='interval', kwargs={"app_state":self.app_state}, seconds=60)
        self.scheduler.add_job(reset_user_greeted, trigger='interval', kwargs={"app_state":self.app_state}, seconds=600)

        log_message("Banyan/PreLoop", "Starting the background scheduler")
        self.scheduler.start()

        log_message("Banyan/PreLoop", "Welcoming the user")
        greet_the_user(self.app_state)


    def postloop(self):
        """Actions to take when Banyan closes"""
        self.app_state.save_application_state()
        greeting = get_users_greeting()
        log_message("Banyan/PostLoop", "Saying goodbye")
        system('say Goodbye {}'.format(greeting))


    def do_good(self, arg):
        """Say hello to Banyan and Banyan will say hello to you: GOOD {morning|afternoon|evening}"""
        log_message("Banyan/Good", "Greeting the user")
        greet_the_user(self.app_state)


    def do_restart(self, arg):
        """Immediately saves the application state and restarts Banyan.: RESTART"""
        log_message("Banyan/Restart", "Preparing to restart Banyan")
        config = get_app_config()
        file = config['FileLocations']['scripts'] + "restart.sh"
        self.app_state.save_application_state()
        log_message("Banyan/Restart", "Restarting Banyan")
        os.execl(file, '')

    def do_clear(self, arg):
        """Clear the console: CLEAR"""
        log_message("Banyan/Clear", "Clearing the console")
        clear = lambda: system('clear')
        clear()

    def do_bye(self, arg):
        """Close Banyan and exit: GOODBYE"""
        log_message("Banyan/Bye", "Preparing for shutdown")

        log_message("Banyan/Bye", "Shutting down the scheduler")
        self.scheduler.shutdown()

        log_message("Banyan/Bye", "Shutting down Banyan")
        return True

    def default(self, arg):
        p = BanyanParser()
        p.input = arg
        p.parse()


def main():
    Banyan().cmdloop()


if __name__ == '__main__':
    main()