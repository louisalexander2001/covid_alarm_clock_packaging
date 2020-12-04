#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 04:29:09 2020

@author: louisalexander
"""

import json

print("This setup script initialises variables in the config file for this package.\n")
print("The following API keys are required!\n")
with open('./covid_alarm_clock/conf.json', 'r') as f:
    json_file = json.load(f)
weather, news = '', ''
while weather == '':
    weather = str(input("Please enter your API key for www.api.openweathermap.org: "))
while news == '':
    news = str(input("Please enter your API key for www.api.openweathermap.org: "))
print("If you would like to use the default value just press enter.\n")
log_file = str(input("Enter the directorhy for the log file: "))
image_URL = str(input("Enter the URL for the image you would like to use: "))
image_file = str(input("Enter the image file name in the static folder: "))
country = str(input("Enter the country code: ")).lower()
city = str(input("Enter the city: "))
json_file["API_keys"]['news'] = news
json_file["API_keys"]['weather'] = weather
if log_file != '':
    json_file["filepaths"]["logfile"] = log_file
if image_URL != '':
    json_file["filepaths"]["image_URL"] = image_URL
if image_file != '':
    json_file["filepaths"]["image_file"] = image_file
if country != '':
    json_file["location"]["country"] = country
if city != '':
    json_file["location"]["city"] = city

with open('./covid_alarm_clock/conf.json', 'w') as f:
    json.dump(json_file, f)