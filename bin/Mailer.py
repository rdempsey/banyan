#!/usr/bin/env python
# encoding: utf-8
"""
Mailer.py
Created by Robert Dempsey on 11/07/14.
Copyright (c) 2014 Robert Dempsey. All rights reserved.
"""

import sys
from os import system
import smtplib
import imaplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
from bin.configs import *

COMMASPACE = ', '
single_lock = threading.Lock()


# Get the count of unread emails for the Gmail account
class SayGmailCount(threading.Thread):
    def run(self):
        single_lock.acquire()
        config = get_app_config()
        m = Mailer()
        m.account_name = config['Email']['robertonrails_account_name']
        m.username = config['Email']['robertonrails_email']
        m.password = config['Email']['robertonrails_password']
        system('say {}'.format(m.get_email_count()))
        single_lock.release()

# Get the count of unread emails for the ADS account
class SayADSCount(threading.Thread):
    def run(self):
        single_lock.acquire()
        config = get_app_config()
        m = Mailer()
        m.account_name = config['Email']['robertatads_account_name']
        m.username = config['Email']['robertatads_email']
        m.password = config['Email']['robertatads_password']
        system('say {}'.format(m.get_email_count()))
        single_lock.release()

# Get the count of unread emails for the Gmail account
class SayDC2Count(threading.Thread):
    def run(self):
        single_lock.acquire()
        config = get_app_config()
        m = Mailer()
        m.account_name = config['Email']['robertatdc2_account_name']
        m.username = config['Email']['robertatdc2_email']
        m.password = config['Email']['robertatdc2_password']
        system('say {}'.format(m.get_email_count()))
        single_lock.release()


class Mailer:
    def __init__(self, **kwargs):
        self.properties = kwargs

    # Subject
    @property
    def subject(self):
        return self.properties.get('subject', 'None')

    @subject.setter
    def subject(self, s):
        self.properties['subject'] = s

    @subject.deleter
    def subject(self):
        del self.properties['subject']

    # Recipients
    @property
    def recipients(self):
        return self.properties.get('recipients', 'None')

    @recipients.setter
    def recipients(self, r):
        self.properties['recipients'] = r

    @recipients.deleter
    def recipients(self):
        del self.properties['recipients']

    # Account Name
    @property
    def account_name(self):
        return self.properties.get('account_name', 'None')

    @account_name.setter
    def account_name(self, an):
        self.properties['account_name'] = an

    @account_name.deleter
    def account_name(self):
        del self.properties['account_name']

    # Username
    @property
    def username(self):
        return self.properties.get('username', 'None')

    @username.setter
    def username(self, s_from):
        self.properties['username'] = s_from

    @username.deleter
    def username(self):
        del self.properties['username']

    # Password
    @property
    def password(self):
        return self.properties.get('password', 'None')

    @password.setter
    def password(self, g_pass):
        self.properties['password'] = g_pass

    @password.deleter
    def password(self):
        del self.properties['password']

    # Message
    @property
    def message(self):
        return self.properties.get('message', 'None')

    @message.setter
    def message(self, m):
        self.properties['message'] = m

    @message.deleter
    def message(self):
        del self.properties['message']

    # Attachments
    @property
    def attachments(self):
        return self.properties.get('attachments', 'None')

    @attachments.setter
    def attachments(self, a):
        self.properties['attachments'] = a

    @attachments.deleter
    def attachments(self):
        del self.properties['attachments']

    # Get the count of email for a given account
    def get_email_count(self):
        obj = imaplib.IMAP4_SSL('imap.gmail.com','993')
        obj.login(self.username, self.password)
        obj.select()
        email_count = len(obj.search(None,'UnSeen')[1][0].split())
        return "You have {} new messages in the {} account.".format(email_count, self.account_name)

    # Send an email via Gmail
    def send_email(self):
        # Create the enclosing (outer) message
        outer = MIMEMultipart('alternative')
        outer['Subject'] = self.subject
        outer['To'] = COMMASPACE.join(self.recipients)
        outer['From'] = self.username

        msg = MIMEBase('application', "octet-stream")

        # Add the text of the email
        email_body = MIMEText(self.message, 'plain')
        outer.attach(email_body)

        # Add the attachments
        for file in self.attachments:
            try:
                with open(file, 'rb') as fp:
                    msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                outer.attach(msg)
            except:
                print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                raise

        composed = outer.as_string()

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(self.username, self.password)
                s.sendmail(self.username, self.recipients, composed)
                s.close()
            print("Email sent!")
        except:
            print("Unable to send the email. Error: ", sys.exc_info()[0])
            raise

def main():
    pass

if __name__ == '__main__': main()