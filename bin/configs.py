#!/usr/bin/env python
# encoding: utf-8
"""
configs.py
Created by Robert Dempsey on 1/20/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

import configparser


def get_app_config():
    """Get the application configuration"""
    config = configparser.ConfigParser(interpolation = configparser.ExtendedInterpolation())
    config.read('config/config.ini')
    return config


def get_users_greeting():
    """Get the user's greeting"""
    config = get_app_config()
    return config['Default']['greeting']


def get_project_path():
    """Get the project path"""
    config = get_app_config()
    return config['FileLocations']['project_path']