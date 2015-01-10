# Banyan

## Major Goals

    1. Be able to interact with Banyan, using voice, without having to activate an application or window.

## Desired Functionality

    1. Have Banyan remind me of events on my calendar.
    
## Current Functionality

    Note: Banyan currently takes the form of a multi-threaded console application. Some functions can run simultaneously
          while others require the current process to finish first.

    1. Say good {morning, afternoon, evening} at the appropriate time
    2. Provide the current weather report from Forecast.io
    3. Provide the current day's weather forecast from Forecast.io

## Daily Automated Tasks

    * Get the weather report for the day


## Requirements

    * Python 2.7.x
    * PEAK-Rules: http://peak.telecommunity.com/DevCenter/PEAK-Rules
    * sqlite3
    # configparser
    * forecastio

    * Allow osascript to use accessibility features: sudo sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db "INSERT or REPLACE INTO access VALUES('kTCCServiceAccessibility','com.apple.RemoteDesktopAgent',1,1,1,NULL)"
    

## Setting Up Voice Recognition

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