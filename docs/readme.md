# Banyan

## Major Goals

    1. Be able to interact with Banyan, using voice, without having to activate an application or window.
    2. Be able to update Banyan's codebase and reload it without having to call "python banyan.sh" to do so.
    3. Be able to perform multiple tasks simultaneously while continuously accepting user input
    4. Be able to run Banyan on a completely separate system (raspberry pi) to make it quite autonomous

## Current Functionality

    Note: Banyan currently takes the form of a multi-threaded console application. Some functions can run simultaneously
          while others require the current process to finish first.

    1. Say good {morning, afternoon, evening} at the appropriate time.
    2. If it's the morning and the first time Banyan has been run, you'll be told the current weather and the forecast for the day
    3. Restart Banyan with a command, saving application state before the restart.
    4. Provide the current weather report from Forecast.io
    5. Provide the current day's weather forecast from Forecast.io
    6. Checks every 30 minutes for the current weather forecast. If we already have it keep going; if not get it and save it


## Functionality On The Agenda

    1. Add alerting via SMS
    2. Send an SMS alert when an application error occurs
    3. Have Banyan run as a daemon that can be started, stopped and reloaded (once voice commands are possible)
    

## Daily Scheduled Tasks

    * coming soon


## Requirements

    * Python 2.7.x (2.7.9)
    * SQLite: http://www.sqlite.org/ (3.8.7.4)
    * PEAK-Rules: http://peak.telecommunity.com/DevCenter/PEAK-Rules (0.5a1.dev-r2713)
    # configparser: https://pypi.python.org/pypi/configparser (3.3.0r2)
    * python-forecastio: https://pypi.python.org/pypi/python-forecastio (1.3.1)
    * apscheduler: https://pypi.python.org/pypi/APScheduler (3.0.1)
    * sqlalchemy: http://www.sqlalchemy.org/ (0.9.7)
    

## How To Set Up Voice Recognition

    * Download PortAudio: http://www.portaudio.com/archives/pa_stable_v19_20140130.tgz
    * Download PyAudio: http://people.csail.mit.edu/hubert/pyaudio/packages/pyaudio-0.2.8.tar.gz
    * Unpack PyAudio. This will create a folder named PyAudio-0.2.8
    * Unpack PortAudio, rename the folder to portaudio-v19, and move it into the PyAudio-0.2.8 folder
    * CD into the portaudio-v19 folder and run the following to build and install PortAudio:
        * ./configure
        * make
        * sudo make install
    * CD up into the PyAudio-0.2.8 folder and run the following to install PyAudio:
        * python setup.py build --static-link
        * python setup.py install
    or ...
    
    * Use the built-in dictation features of Mac OS and use an external application to activate it