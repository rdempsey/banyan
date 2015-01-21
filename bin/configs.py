#!/usr/bin/env python
# encoding: utf-8
"""
configs.py
Created by Robert Dempsey on 1/20/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

import configparser


# Get the application configuration
def get_app_config():
    config = configparser.ConfigParser(interpolation = configparser.ExtendedInterpolation())
    config.read('config/config.ini')
    return config


# Get the path to the BanyanDB file
def get_banyan_db():
    config = get_app_config()
    return config['BanyanDatabase']['db']


# Get the user's greeting
def get_users_greeting():
    config = get_app_config()
    return config['Default']['greeting']