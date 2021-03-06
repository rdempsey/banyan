#!/usr/bin/env python
# encoding: utf-8
"""
LocalFile.py
Created by Robert Dempsey on 1/20/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

from os import system
import threading
from bin.BanyanDB import BanyanDB
from bin.banyan_logger import log_message

def open_local_file(file_name):
    system("open '{}'".format(file_name))

class LocalFile:
    def __init__(self, **kwargs):
        self.properties = kwargs

    lower = str.lower

    def open_file(self, file_name):
        """Open a file listed in the database"""
        f = BanyanDB()
        file_to_open = f.get_file_by_name(LocalFile.lower(file_name))

        if file_to_open is None:
            log_message("LocalFile/OpenFile", "unable to open file {}".format(file_name))
            system("say I am unable to open file {}".format(file_name))
        else:
            log_message("LocalApp/OpenFile", "Opening file: {}".format(file_name))
            t = threading.Thread(target=open_local_file, kwargs={"file_name":file_to_open})
            t.daemon = True
            t.start()


if __name__ == '__main__':
    pass