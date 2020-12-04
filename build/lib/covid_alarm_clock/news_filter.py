#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 17:36:46 2020

@author: louisalexander
"""
from typing import Union
import requests
from flask import Markup

def get_news(country: str, api_key: str, headlines: bool =False) -> Union[str, dict]:
    '''
    Parameters
    ----------
    country : str
        A country code.
    api_key : str
        An API key for www.newsapi.org.
    headlines : bool, optional
        Modifies return value of the function. The default is False.

    Returns
    -------
    Union[str, dict]
        This function takes in some values and returns a list of dictionaries
        of news articles that pass the filter if headlines is False. If
        headlines is True it retuns a string containing a markup formatted
        version of just the headlines of the articles that passed the filter.
        The filter is for BBC or coronavirus articles.
    '''
    base_url = "https://newsapi.org/v2/top-headlines?"
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    # print response object
    response = requests.get(complete_url).json()
    articles = response["articles"]
    return_str = ''
    news_dict = []
    for article in articles:
        try:
            if article['source']['name'] == 'BBC News':
                return_str += article['title'] + '<br /><br />'
                news_dict.append({'title': article['title'], \
                                  'content': Markup(article['description']+'<br />\
                                                    <a href="'+article['url']+\
                                                    '">Read more here</a>')})
            elif (('covid' or 'covid-19' or 'coronavirus') in \
                  article['title'].lower()) or (('covid' or 'covid-19' or \
                  'coronavirus') in article['content'].lower()) or (('covid' \
                  or 'covid-19' or 'coronavirus') in article['description'].lower()):
                return_str +=  article['title'] + '<br /><br />'
                news_dict.append({'title': article['title'], \
                                  'content': Markup(article['description']+\
                                  '<br /><a href="'+article['url']+\
                                  '">Read more here</a>')})
        except:
            pass
    if headlines:
        return return_str
    return news_dict
