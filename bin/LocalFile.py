#!/usr/bin/env python
# encoding: utf-8
"""
LocalFile.py
Created by Robert Dempsey on 1/20/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

from os import system, path
import threading
from bin.configs import *
from bin.BanyanDB import BanyanDB


class LocalFile:
    def __init__(self, **kwargs):
        self.properties = kwargs

    lower = str.lower

    def open_file(self, file_name):
        """Open a file listed in the database"""
        f = BanyanDB()
        f.database = get_banyan_db()
        file_to_open = f.get_file_by_name(LocalFile.lower(file_name))

        if file_to_open is None:
            print("Unable to open {}".format(file_name))
        else:
            t = threading.Thread(target=self.__open_local_file, kwargs={"file_name":file_to_open})
            t.daemon = True
            t.start()

    def __open_local_file(file_name):
        system("open '{}'".format(file_name))

    def __create_local_file(file_name):
        pass


if __name__ == '__main__':
    pass