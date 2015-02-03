#!/usr/bin/env python
# encoding: utf-8
"""
LocalProject.py
Created by Robert Dempsey on 1/24/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

from os import system, makedirs, path
from threading import Thread
from bin.configs import *
from github import Github
from github.GithubException import *
from bin.banyan_logger import log_message

class LocalProject:
    def __init__(self, **kwargs):
        self.properties = kwargs

    lower = str.lower

    def create_new_project(self, project_name, save_in_github):
        """Create a new project"""
        log_message("LocalProject/CreateNewProject", "Creating project: ".format(project_name))
        project_path = get_project_path() + project_name
        t = Thread(target=self.__create_project_folder, args=(project_name, project_path, save_in_github,))
        t.daemon = True
        t.start()


    def __create_project_folder(self, project_name, project_path, save_in_github):
        if LocalProject.lower(save_in_github) == "yes":
            log_message("LocalProject/CreateProjectFolder", "Creating a private Github repo for project {}".format(project_name))
            config = get_app_config()
            un = config['Github']['username']
            pw = config['Github']['password']
            token = config['Github']['token']

            try:
                g = Github(un, pw)
                new_repo = g.get_user().create_repo(name="{}".format(project_name),
                                                    private=True,
                                                    has_issues=False,
                                                    has_wiki=False,
                                                    has_downloads=False,
                                                    auto_init=True)
            except GithubException:
                log_message("LocalProject/CreateProjectFolder", "Unable to create a new repo in Github")
                system("say I was unable to create the new repo.")

            # Make the directory
            if not path.exists(project_path):
                log_message("LocalProject/CreateProjectFolder", "Creating the project folder")
                makedirs(project_path)
            try:
                # Initialize a git repo in the new directory
                log_message("LocalProject/CreateProjectFolder", "Initializing the git repo")
                system("cd {} && git init".format(project_path))

                # Pull the repo into the new folder
                log_message("LocalProject/CreateProjectFolder", "Pulling the new project from the git repo")
                git_pull_url = "https://{}@github.com/rdempsey/{}.git".format(token, project_name)
                system("cd {} && git pull {}".format(project_path, git_pull_url))
            except:
                log_message("LocalProject/CreateProjectFolder", "Unable to pull the new repo")
                system("say I was unable to pull the new repo")
        else:
            # Simply create the project
            if not path.exists(project_path):
                log_message("LocalProject/CreateProjectFolder", "Creating the project folder")
                makedirs(project_path)

        log_message("LocalProject/CreateProjectFolder", "Project creation complete")
        system("say Project creation complete")


if __name__ == '__main__':
    pass