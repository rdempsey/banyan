#!/usr/bin/env python
# encoding: utf-8
"""
LocalApp.py
Created by Robert Dempsey on 1/20/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

from os import system
import threading
from bin.BanyanDB import BanyanDB
from bin.banyan_logger import *


# Launch an application
def launch_app(app_to_launch):
    system("open '{}'".format(app_to_launch))


class LocalApp:
    def __init__(self, **kwargs):
        self.properties = kwargs

    lower = str.lower


    def launch_application(self, app_name):
        a = BanyanDB()
        app_to_launch = a.get_app_by_name(LocalApp.lower(app_name))

        if app_to_launch is None:
            log_message("LocalApp/LaunchApplication", "Unable to launch {}".format(app_name))
            system("say I am unable to launch {}".format(app_name))
        else:
            log_message("LocalApp/LaunchApplication", "Launching application: {}".format(app_name))
            t = threading.Thread(target=launch_app, kwargs={"app_to_launch":app_to_launch})
            t.daemon = True
            t.start()

if __name__ == '__main__':
    pass