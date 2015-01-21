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


# Launch an application
def launch_app(app_to_launch):
    os.system("open '{}'".format(app_to_launch))


class LocalApp:
    def __init__(self, **kwargs):
        self.properties = kwargs

    def launch_application(self, app_name):
        app = str(app_name).lower()
        app_to_launch = get_app_by_name(app)

        if app_to_launch == None:
            print("Unable to launch {}".format(app_name))
        else:
            t = threading.Thread(target=launch_app, kwargs={"app_to_launch":app_to_launch})
            t.daemon = True
            t.start()

if __name__ == '__main__':
    pass