#!/usr/bin/env python
# encoding: utf-8
"""
BanyanParser.py
Created by Robert Dempsey on 1/23/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

from pyparsing import *
from bin.LocalApp import *
from bin.LocalFile import *
from bin.Mailer import *
from bin.Weather import *
from bin.WebSearch import *
from bin.LocalProject import *


class BanyanParser:
    def __init__(self, **kwargs):
        self.properties = kwargs

    # Input
    @property
    def input(self):
        return self.properties.get('input', 'None')

    @input.setter
    def input(self, s):
        self.properties['input'] = s

    @input.deleter
    def input(self):
        del self.properties['input']


    def parse(self):
        """
        Commands
        word            ::      group of alphabetic characters
        command         ::      the first word of the sentence
        command_object  ::      what the command needs to do

        Questions
        question        ::      the first word of the sentence begins with a contraction
        """

        # Put the input into a string
        input = self.input

        # Parse Actions
        join_tokens = lambda tokens : " ".join(tokens)

        # Define grammar
        comma = Literal(",").suppress()
        command = oneOf("check create open search get email tweet launch")
        act_on = oneOf("project file web locally")
        command_object = OneOrMore(Word(alphas+"'."))
        what_time = oneOf("current today's tomorrow's")
        subject = Literal("subject")

        # Assign parse actions
        command_object.setParseAction(join_tokens)

        # Commands
        create_open_search = command("command") + act_on("act_on") + command_object("name")
        get = command("command") + what_time("time") + command_object("object")
        email = command("command") + command_object("email_to") + comma + subject + command_object("email_subject")
        tweet = command("command") + command_object("tweet")
        launch_check = command("command") + command_object("app")

        try:
            w = command.parseString(input)
            if w[0] == "create":
                c = create_open_search.parseString(input)
                if c.act_on == "project":
                    os.system("say Shall I store the project in a private repo?")
                    save_in_github = raw_input("Save in Github > ")
                    p = LocalProject()
                    p.create_new_project(c.name, save_in_github)
                elif c.act_on == "file":
                    #TODO: add create file
                    pass
            elif w[0] == "check":
                chk = launch_check.parseString(input)
                if chk.app == "email":
                    SayGmailCount().start()
                    SayADSCount().start()
                    SayDC2Count().start()
            elif w[0] == "open":
                c = create_open_search.parseString(input)
                if c.act_on == "file":
                    f = LocalFile()
                    f.open_file(c.name)
                else:
                    #TODO: add open project
                    print("{}: {} - {}".format(c.command, c.act_on, c.name))
            elif w[0] == "search":
                s = create_open_search.parseString(input)
                if s.act_on == "web":
                    ws = WebSearch()
                    ws.perform_search(s.name)
                elif s.act_on == "locally":
                    #TODO: add local searching
                    pass
            elif w[0] == "get":
                g = get.parseString(input)
                if g.time == "current" and g.object == "weather":
                    SayCurrentWeather().start()
                elif g.time == "current" and g.object == "forecast":
                    SayCurrentForecast().start()
            elif w[0] == "email":
                e = email.parseString(input)
                print("email: {}, subject: {}".format(e.email_to, e.email_subject))
            elif w[0] == "tweet":
                t = tweet.parseString(input)
                #TODO: add tweeting
                print( "tweet: {}".format(t.tweet))
            elif w[0] == "launch":
                l = launch_check.parseString(input)
                la = LocalApp()
                la.launch_application(l.app)
            else:
                print("I don't know what you want me to do...")
        except:
            print("Please enter a valid command")



if __name__ == '__main__':
    pass