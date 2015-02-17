#!/usr/bin/env python
# encoding: utf-8
"""
text_cleaner.py
Created by Robert Dempsey on 2/17/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

import unicodedata

def unicode_weather_cleaner(text_to_clean):
    dash = u'\u2013'.encode('utf8')
    long_dash = '\xe2\x80\x93'

    text_to_clean = str(text_to_clean.encode('utf8'))

    if long_dash in text_to_clean:
        text_to_clean = text_to_clean.replace(long_dash, " to ")
        text_to_clean = text_to_clean.replace("in.", "inches")

    for ch in ['(', ')']:
        if ch in text_to_clean:
            text_to_clean = text_to_clean.replace(ch, "")

    text_to_clean = text_to_clean.replace("in.", "inch")

    return text_to_clean