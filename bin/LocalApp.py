#!/usr/bin/env python
# encoding: utf-8
"""
LocalApp.py
Created by Robert Dempsey on 1/20/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

import os
import threading
from bin.configs import *
from bin.BanyanDB import BanyanDB


# Launch an application
def launch_app(app_to_launch):
    os.system("open '{}'".format(app_to_launch))


class LocalApp:
    def __init__(self, **kwargs):
        self.properties = kwargs

    def launch_application(self, app_name):
        a = BanyanDB()
        a.database = get_banyan_db()
        app_to_launch = a.get_app_by_name(str(app_name).lower())

        if app_to_launch is None:
            print("Unable to launch {}".format(app_name))
        else:
            t = threading.Thread(target=launch_app, kwargs={"app_to_launch":app_to_launch})
            t.daemon = True
            t.start()

if __name__ == '__main__':
    pass