#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 18:04:06 2020

@author: louisalexander
"""
import requests

def get_weather(city_name: str, api_key: str) ->str:
    '''
    Parameters
    ----------
    city_name : str
        The name of a city.
    api_key : str
        An API key for www.api.openweathermap.org.

    Returns
    -------
    str
        Returns markup formatted user friendly data for the area concerned.
    '''
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    unpacked = response.json()
    main = unpacked["main"]
    current_temperature = round(main["temp"]- 273.15, 2)
    current_feels_like = round(main["feels_like"]- 273.15, 2)
    weather_description = unpacked["weather"][0]["description"]
    # print following values
    return "The weather for " + str(unpacked['name'] + ' is as follows.<br />\
            The temperature is ' + str(current_temperature) + " celcius.<br />\
            It feels like " + str(current_feels_like) + " celcius.<br />\
            Today there will be " + str(weather_description))
