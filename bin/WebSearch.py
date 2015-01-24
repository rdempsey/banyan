#!/usr/bin/env python
# encoding: utf-8
"""
WebSearch.py
Created by Robert Dempsey on 1/24/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

import webbrowser
from bin.google import search
import threading


class WebSearch:
    def __init__(self, **kwargs):
        self.properties = kwargs

    def perform_search(self, query):
        s = threading.Thread(target=self.__search_the_web, args=(query,))
        s.start()

    def __search_the_web(self, query):
        for url in search(query, stop=10):
            webbrowser.open_new_tab(url)



if __name__ == '__main__':
    pass