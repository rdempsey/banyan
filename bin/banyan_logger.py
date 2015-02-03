#!/usr/bin/env python
# encoding: utf-8
"""
banyan_logger.py
Created by Robert Dempsey on 2/2/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

import socket
from time import strftime

host = "127.0.0.1"
port = 5000

def log_message(sending_object, message):
    banyan_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    banyan_server.connect((host, port))

    now = strftime("%b %d %H:%M:%S")
    message = now + " zephyr " + sending_object + " " + message
    banyan_server.sendall(message + "\n")



