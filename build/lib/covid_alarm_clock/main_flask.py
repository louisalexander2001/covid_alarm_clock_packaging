#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:32:17 2020

@author: louisalexander

This module is the main module in a project covid_alarm_clock. It is the main
backend for the html template to be rendered with flask. This module centers
around the home function, from which all other functions are called excluding
the initiation of variables.
"""
import sched
import time
import logging
import json
from datetime import date
import ast
import datetime
import pyttsx3
from flask import Flask, request, render_template, Markup
from uk_covid19 import Cov19API
import time_conversions
from weather_update import get_weather
from news_filter import get_news

# Read config file and unpack it
with open('conf.json', 'r') as f:
    json_file = json.load(f)
API_keys = json_file["API_keys"]
file_paths = json_file["filepaths"]
location = json_file["location"]
covid_data = json_file["covid_data"]
reload_notifications = json_file["reload_notifications"]

# Setup scheduler, speech engine, logging and flask app
scheduler = sched.scheduler(time.time, time.sleep)
speech_engine = pyttsx3.init()
logging.basicConfig(filename=file_paths['logfile'], level=logging.DEBUG)
app = Flask(__name__)

# Define key global varials
global NOTIFICATIONS
global ALARMS
NOTIFICATIONS = []
ALARMS = []

logging.info('Import statements have loaded correctly.')
logging.info('The scheduler, speech engine, logging and flask app have been initiated.')
logging.info('Global variables have been assigned.')

def make_notifications() -> None:
    '''
    Returns
    -------
    None
        This function calls on the news_filter and weather_update modules to
        collect the data form the relevant API's. It then unpacks them an
        appends them to the NOTIFICATIONS list for rendering.'''
    global NOTIFICATIONS
    NOTIFICATIONS = []
    api = Cov19API(filters=covid_data["nationally"], structure=covid_data["cases_and_deaths"])
    data = api.get_json()['data'][0]
    NOTIFICATIONS.append({'title': 'Covid Data',\
                          'content': Markup(
        f'<p style="text-align:left;">The COVID data for the\
        {data["areaName"]} as of {data["Date"]} is:\
        <br />Cases:\
        <br />&emsp;Total Cases: {str(data["cases"]["cumCasesByPublishDate"])}\
        <br />&emsp;New Cases: {str(data["cases"]["newCasesByPublishDate"])}\
        <br />Deaths:\
        <br />&emsp;Total Deaths: {str(data["deaths"]["cumDeaths28DaysByPublishDate"])}\
        <br />&emsp;New Deaths: {str(data["deaths"]["newDeaths28DaysByPublishDate"])}</p>')})
    NOTIFICATIONS.append({'title':'Weather',\
                          'content':Markup(get_weather(location['city'], API_keys['weather']))})
    NOTIFICATIONS.append({'title':'Headlines',\
                          'content':Markup(get_news(location['country'], API_keys['news'], True))})
    for notification in get_news(location['country'], API_keys['news']):
        NOTIFICATIONS.append(notification)
    logging.info('Notifications have been reloaded.')

def regular_actions(hour: bool =False, day: bool =False, first_time: bool =False) -> None:
    '''
    Parameters
    ----------
    hour : bool, optional
        Triggers the make_notifications function and schedules it to be done
        again in an hour. The default is False.
    day : bool, optional
        Triggers the load_alarms_from_log function and schedules it to be done
        again in a day. The default is False.
    first_time : bool, optional
        Trigers both load_alarms_from_log and make_notifications to be run. It
        schedueles them to be run again at 00:02 and the begining of the hour
        respectively. The default is False.

    Returns
    -------
    None
        This module is for ensuring that the notifications are kept upto date
        regularly and that every day the relevant alarms are loaded from the
        log file. It also has a first time flag to complete both these methods
        on startup.'''
    if first_time:
        make_notifications()
        load_alarms_from_log()
        delay = time_conversions.hhmm_to_seconds(str(int(time.strftime('%H'))+1) + ':01') - \
            time_conversions.hhmm_to_seconds(time_conversions.current_time_hhmm()) - \
            int(time.strftime('%S'))
        scheduler.enter(float(delay), 1, regular_actions, (True,))
        delay = (time_conversions.hhmm_to_seconds('23:59') - \
            time_conversions.hhmm_to_seconds(time_conversions.current_time_hhmm()) - \
            int(time.strftime('%S'))) + 180
        scheduler.enter(float(delay), 1, regular_actions, (False, True,))
        logging.info(
    'make_notifications and load_alarms_from_log have been run for the first time and rescheduled.')
    elif hour:
        make_notifications()
        scheduler.enter(float(reload_notifications), 1, regular_actions, (True,))
        logging.info('make_notifications has been run and rescheduled')
    elif day:
        load_alarms_from_log()
        scheduler.enter(float(86400), 1, regular_actions, (False, True))
        logging.info('load_alarms_from_log has been run and rescheduled')

def load_alarms_from_log() -> None:
    '''
    Returns
    -------
    None
        This function loads alarms from the log and schedules them to be
        announced.

    '''
    global ALARMS
    with open(file_paths['logfile'], "r") as file:
        lines = file.readlines()
    with open(file_paths['logfile'], "w") as file:
        for line in lines:
            if line[:26 ] == f"CRITICAL:root:['{time.strftime('%Y-%m-%d')}":
                values = ast.literal_eval(line[14:])
                title = values[0][:10] + ' - ' + values[0][-5:] + ' - ' + values[1]
                ALARMS = remove_dict_from_list(ALARMS, title)
                set_an_alarm(values[0], values[1], values[2], values[3])
                file.write(line)
            else:
                file.write(line)
    logging.info('The alarms for today have been scheduled form the log file.')

def remove_dict_from_list(list_name: list, title_to_remove: str) -> list:
    '''
    Parameters
    ----------
    list_name : list
        A list of dictionaries.
    title_to_remove : str
        The contents of the title attribute in one of the dictionaries in the list.

    Returns
    -------
    list
        This functiion takes a list and title(str) and searches a list of
        dictionaries for the dictionary that had the title attribute equal to
        the title(str). It then removes this dictionary from the list.
    '''
    logging.info('%s has been removed from a list.', title_to_remove)
    return [i for i in list_name if i['title'] != title_to_remove]

def text_to_speech(announcement: str) -> None:
    '''
    Parameters
    ----------
    announcement : str
        A string to be announced.

    Returns
    -------
    None
        This function takes a sting and passes it on to the speach engine for
        announcing. There is some extra functionality to deal with a mac bassed
        error. It is expected to throw an exception but this is caught and logged.
    '''
    try:
        speech_engine.endLoop()
    except RuntimeError:
        logging.info('A mac bassed error with pyttsx3 has been caught. No further action required.')
    speech_engine.say(announcement)
    speech_engine.runAndWait()
    logging.info('An announcement has been successfully made.')

def say_and_remove(title: str, alarm_title: str) -> None:
    '''
    Parameters
    ----------
    title : str
        The user friendly title built by set_an_alarm.
    alarm_title : str
        The alarm passed through from the html form.

    Returns
    -------
    None
        This function builds the announcement to be said by the speach engine.
        The announcement order is alarm title, weather, headlines. Once the
        announcement has been built it then removes the alarm from the list of
        alarms.
    '''
    global NOTIFICATIONS
    global ALARMS
    alarm = [i for i in ALARMS if i['title'] == title]
    announcement = str(title)[13:] + ' - ' + [i for i in NOTIFICATIONS \
                         if i['title'] ==
                         'Covid Data'][0]['content'][28:-4].replace('-', ' ') + ' - '
    try:
        if alarm[0]['weather'] is not None:
            make_notifications()
            announcement += [i for i in NOTIFICATIONS \
                             if i['title'] == 'Weather'][0]['content']
        if alarm[0]['news'] is not None:
            make_notifications()
            announcement += [i for i in NOTIFICATIONS \
                             if i['title'] == 'Headlines'][0]['content']
    except IndexError:
        logging.error('An Index error was thrown by say_and_remove')
    with open(file_paths['logfile'], "r") as file:
        lines = file.readlines()
        with open(file_paths['logfile'], "w") as file:
            for line in lines:
                if line[:36 + len(alarm_title)] == \
                    f"CRITICAL:root:['{time.strftime('%Y-%m-%d')}T{title[13:18]}', '{alarm_title}":
                    file.write(f'INFO:root: The alarm {title} has run.\n')
                else:
                    file.write(line)
    ALARMS = remove_dict_from_list(ALARMS, title)
    text_to_speech(announcement.unescape().replace('<br />', ' - '))
    logging.info(
    'The alarm %s has been said, removed from ALARMS and CRITICAL log removed', title)

def set_an_alarm(alarm_time: str, alarm_title: str, read_news: str, read_weather: str) -> None:
    '''
    Parameters
    ----------
    alarm_time : str
        The time the alarm should go off. FORMAT: "HH:MM".
    alarm_title : str
        The title of the alarm passed through from the HTML form.
    read_news : str
        Is equal to 'news' if the news should be read with the alarm.
    read_weather : str
        Is equal to 'weather' if the weather should be read with the alarm.

    Returns
    -------
    None
        This function creates the user-friendly tile that is displayed in the
        browser and adds it to the ALARMS list. It checks if the alarm is
        in the past and if it is ignors the request. If the alarm is the same
        day in the future it schedules and logs it. If the alarm is in the
        future and not on the current day it only logs it so that it can be
        loaded in and scheduled after midnight on the relevant day.
    '''
    global ALARMS
    global NOTIFICATIONS
    content = 'This alarm will:<br />Make an announcement'
    title = alarm_time[:10] + ' - ' + alarm_time[-5:] + ' - ' + alarm_title
    # Check alarm is today and in the future
    if date(int(alarm_time[:4]), int(alarm_time[5:7]), int(alarm_time[8:10])) > date.today():
        logging.critical([alarm_time, alarm_title, read_news, read_weather])
        if read_news:
            content += '<br />Read the headlines'
        if read_weather:
            content += '<br />Read the weather'
        ALARMS.append({'title':title, \
                       'content':Markup(content), \
                       'news':read_news, \
                       'weather':read_weather, \
                       'event':None
                       })
        logging.info(
            'Alarm %s has been logged for the future and added to ALARMS.', title)
    elif datetime.datetime(int(alarm_time[:4]), int(alarm_time[5:7]), \
                           int(alarm_time[8:10]), int(alarm_time[11:13]), \
                           int(alarm_time[14:])) > datetime.datetime.now():
        # Convert alarm_time to a delay
        alarm_hhmm = alarm_time[-5:-3] + ':' + alarm_time[-2:]
        delay = time_conversions.hhmm_to_seconds(alarm_hhmm) - \
            time_conversions.hhmm_to_seconds(time_conversions.current_time_hhmm()) - \
            int(time.strftime('%S'))
        if read_news:
            content += '<br />Read the headlines'
        if read_weather:
            content += '<br />Read the weather'
        logging.critical([alarm_time, alarm_title, read_news, read_weather])
        ALARMS.append({'title':title, \
                       'content':Markup(content), \
                       'news':read_news, \
                       'weather':read_weather, \
                       'event':scheduler.enter(float(delay), 1, \
                                               say_and_remove, \
                                               (title, alarm_title)) })
        logging.info(
            'Alarm %s has been logged, scheduled and added to ALARMS.', title)
    else:
        NOTIFICATIONS.insert(0, {'title':'ALARM TIME NOT POSSIBLE', \
                       'content': 'The date and time you choese must be in the future.'})
        logging.debug('The user tried to set an alarm in the future %s', title)

@app.route('/')
@app.route('/index')
def home() -> render_template:
    '''
    Returns
    -------
    render_template
        This is the main function of the module. It is executed every time the
        webpage is reloaded which is every 30s. It runs the scheduler and
        gathers  perameters from the restful URL. Bassed on the perameters it
        adds alarms, removes alarms or removes notifications.
    '''
    global NOTIFICATIONS
    global ALARMS
    scheduler.run(blocking=False)
    alarm_time = request.args.get("alarm")
    alarm_title = request.args.get("two")
    read_news = request.args.get("news")
    read_weather = request.args.get("weather")
    remove_notification = request.args.get("notif")
    remove_alarm = request.args.get("alarm_item")
    if alarm_time:
        set_an_alarm(alarm_time, alarm_title, read_news, read_weather)
    if remove_notification:
        NOTIFICATIONS = remove_dict_from_list(NOTIFICATIONS, \
                                              remove_notification)
        logging.info('Notification %s has been removed from NOTIFICATIOS', remove_notification)
    if remove_alarm:
        try:
            scheduler.cancel([i for i in ALARMS \
                              if i['title'] == remove_alarm][0]['event'])
        except AttributeError:
            logging.debug(
        'An AttributeError was thrown by home() after line if remove_alarm:. This is expected.')
        except IndexError:
            logging.debug(
            'An IndexError was thrown by home() after line if remove_alarm:. This is expected.')
        with open(file_paths['logfile'], "r") as file:
            lines = file.readlines()
        with open(file_paths['logfile'], "w") as file:
            for line in lines:
                if line[:36 + len(remove_alarm[21:])] != \
                f"CRITICAL:root:['{remove_alarm[:10]}T{remove_alarm[13:18]}', '{remove_alarm[21:]}":
                    file.write(line)
        logging.info("Following alarm was removed from %s: %r", file_paths['logfile'], remove_alarm)
        ALARMS = remove_dict_from_list(ALARMS, remove_alarm)
    logging.info('The HTML template has been rerendered.')
    return render_template('index.html', \
                           title=Markup('<a href="/index">Covid Smart Alarm</a>'), \
                           notifications=NOTIFICATIONS, \
                           alarms=ALARMS, \
                           image=Markup(file_paths['image_file'] + \
                                        '" <img src="' + file_paths['image_URL']))

# Gets relevant alarms from the log and gets the notifications. Schedules both
# events to rung again in the future.
regular_actions(False, False, True)


if __name__ == '__main__':
    app.run()
