#!/usr/bin/env python
# encoding: utf-8
"""
LocalProject.py
Created by Robert Dempsey on 1/24/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

import os
from threading import Thread
from bin.configs import *


class LocalProject:
    def __init__(self, **kwargs):
        self.properties = kwargs

    def create_new_project(self, project_name):
        """Create a new project"""
        project_path = get_project_path() + project_name
        t = Thread(target=self.__create_project_folder, args=(project_path,))
        t.daemon = True
        t.start()


    def __create_project_folder(self, project_name):
        if not os.path.exists(project_name):
            os.makedirs(project_name)
            os.system("say Project created")

if __name__ == '__main__':
    pass