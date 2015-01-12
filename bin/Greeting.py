#!/usr/bin/env python
# encoding: utf-8
"""
Greeting.py
Created by Robert Dempsey on 1/9/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

from os import system
from peak.rules import abstract, when, around, before, after
from bin.Weather import *


class Greeting:
    def __init__(self, app_state, current_time, greeting):
        self.current_time = current_time
        self.greeting = greeting
        self.app_state = app_state

    ## RULES ##

    # @abstract()
    def greet_the_user(self, app_state):
        """ A generic function for greeting the user """

    # If it's between midnight and noon say good morning
    @when(greet_the_user, "0<self.current_time and self.current_time<12")
    def morning_greeting(self, app_state):
        system('say {} {}'.format("Good morning", self.greeting))
        self.app_state.user_greeted = True

    # If it's between noon and 5pm say good afternoon
    @when(greet_the_user, "12<=self.current_time and self.current_time<17")
    def afternoon_greeting(self, app_state):
        system('say {} {}'.format("Good afternoon", self.greeting))
        self.app_state.user_greeted = True

    # If it's between 5 and midnight say good evening
    @when(greet_the_user, "17<=self.current_time and self.current_time<=24")
    def evening_greeting(self, app_state):
        system('say {} {}'.format("Good evening", self.greeting))
        self.app_state.user_greeted = True

    # If it's in the morning, and the user hasn't yet heard the weather and forecast, tell them
    @after(greet_the_user, "0<self.current_time and self.current_time<12 and self.app_state.date_of_last_weather_notification<str(time.strftime('%Y-%m-%d'))")
    def weather_greeting(self, app_state):
        SayCurrentWeather().start()
        SayCurrentForecast().start()
        app_state.date_of_last_weather_notification = str(time.strftime("%Y-%m-%d"))

if __name__ == '__main__':
    pass