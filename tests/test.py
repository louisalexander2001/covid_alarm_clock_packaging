#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 06:35:22 2020

@author: louisalexander
This module tests the basic functionality of the external APIs and the
functionality fo the main_flask module.
"""
import json
import requests
import pyttsx3
from uk_covid19 import Cov19API

with open('../covid_alarm_clock/conf.json', 'r') as f:
    json_file = json.load(f)
covid_data = json_file["covid_data"]
API_keys = json_file["API_keys"]
speech_engine = pyttsx3.init()

def check_covid_API() -> bool:
    '''
    Returns
    -------
    bool
        Check if the covid API is online.
    '''
    api = Cov19API(filters=covid_data["nationally"], structure=covid_data["cases_and_deaths"])
    data = api.get_json()
    if data['totalPages'] == 1:
        return True
    return False

def check_weather_API() -> bool:
    '''
    Returns
    -------
    bool
        Check if the news API is online.
    '''
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + API_keys['weather'] + "&q=London"
    response = requests.get(complete_url)
    unpacked = response.json()
    if unpacked['cod'] == 200:
        return True
    return False

def check_news_API() -> bool:
    '''
    Returns
    -------
    bool
        Check if the news API is online.
    '''
    base_url = "https://newsapi.org/v2/top-headlines?"
    complete_url = base_url + "country=" + 'gb' + "&apiKey=" + API_keys['news']
    response = requests.get(complete_url).json()
    if response['status'] == 'ok':
        return True
    return False

def check_APIs() -> bool:
    if check_covid_API() and check_weather_API() and check_news_API():
        print("All API's are online")
        return True
    print(f"Covid is: {check_covid_API()}\n Weather is {check_weather_API()}\n News is: {check_news_API()}")
    return False

def check_speech_engine() -> bool:
    global speech_engine
    try:
        speech_engine.endLoop()
    except RuntimeError:
        pass
    speech_engine = pyttsx3.init()
    speech_engine.say('x')
    speech_engine.runAndWait()
    return True

if check_APIs() and check_speech_engine():
    print('The tests have been passed.')
    
    
    