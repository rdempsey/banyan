#!/usr/bin/env python
# encoding: utf-8
"""
LocalFile.py
Created by Robert Dempsey on 1/20/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

import os
import threading
from bin.configs import *
from bin.BanyanDB import BanyanDB


# Open a file
def open_file(file_name):
    os.system("open '{}'".format(file_name))


class LocalFile:
    def __init__(self, **kwargs):
        self.properties = kwargs

    def open_file(self, file_name):
        f = BanyanDB()
        f.database = get_banyan_db()
        file_to_open = f.get_file_by_name(str(file_name).lower())

        if file_to_open is None:
            print("Unable to open {}".format(file_name))
        else:
            t = threading.Thread(target=open_file, kwargs={"file_name":file_to_open})
            t.daemon = True
            t.start()


if __name__ == '__main__':
    pass