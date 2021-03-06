# Banyan

## Caveat Emptor

Banyan is not 100% ready for primetime. There are no tests, and it's a somewhat non-trivial set up. I am working on updating this readme with more instructions, adding tests, and generally making Banyan more user friendly. Having said that...

I'm a huge fan of the Iron Man trilogy, and anything with Iron Man in it (Avengers). I love the idea of having my own personal JARVIS to help with my day-to-day work. That is what Banyan is all about - automating certain parts of my life.

In the development of Banyan I have found that voice recognition is hard. In order to get around this I decided to use the built-in voice dictation functionality of my Mac. I combined that with an iTerm activation hotkey in order to:

1. Activate the iTerm (running Banyan) window
2. Start voice dictation
3. Stop voice dictation
4. Run the command in Banyan

Once I have all of the hardware integrated on a glove I will post a video for that.


## Major Project Goals

1. Be able to interact with Banyan, using voice, without having to activate an application or window.
2. Be able to update Banyan's codebase and reload it without having to call "python banyan.sh" to do so.
3. Be able to perform multiple tasks simultaneously while continuously accepting user input
4. Be able to run Banyan on a completely separate system (raspberry pi) to make it quite autonomous


## Current Functionality

Note: Banyan currently takes the form of a multi-threaded console application. Some functions can run simultaneously
      while others require the current process to finish first.

1. Say good {morning, afternoon, evening} at the appropriate time.
2. If it's the morning and Banyan hasn't said hello yet, you'll be told good morning along with the current weather 
   and the forecast for the day.
3. Restart Banyan with the restart command, saving application state before the restart. This is for instant code updates.
4. Provide the current weather report from Forecast.io.
5. Provide the current day's weather forecast from Forecast.io.
6. Check every 30 minutes for the current weather forecast. If we already have it don't worry about it; if not get it and save it in the database.
7. Save app state every 30 seconds and on program exit.
8. Search Google and open the first 10 results in separate tabs in Chrome.
9. Open a file listed in the database.
10. Create a new project, and optionally create a private Github repo for it.
11. Log everything to a central logging server controlled by Banyan (using logstash and elasticsearch).


## Functionality On The Agenda

1. Add alerting via SMS
2. Send an SMS alert when an application error occurs
3. Have Banyan run as a daemon that can be started, stopped and reloaded (once voice commands are possible)
    

## Daily Scheduled Tasks

1. Get the current weather forecast; every 30 minutes
2. Save the application state; every 30 seconds
3. Reset the user greeted boolean; every 10 minutes


## Requirements

* Python 2.7.x (2.7.9)
* Postgres: http://www.postgresql.org/ (>=9.4)
* Elasticsearch: http://www.elasticsearch.org/ (1.4.2)
* Logstash: http://logstash.net/ (1.4.2)
* PEAK-Rules: http://peak.telecommunity.com/DevCenter/PEAK-Rules (0.5a1.dev-r2713)
* A host of other eggs


## Optional
 
* Kibana: http://www.elasticsearch.org/guide/en/kibana/current/index.html (3.1.2)


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

* Use the built-in dictation features of Mac OS and use an external application to activate it, which is what I do.