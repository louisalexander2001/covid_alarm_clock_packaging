
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 18:21:42 2020

@author: louisalexander

Credit for this code must go to Matt Collison
"""
import time
def minutes_to_seconds( minutes: str ) -> int:
    '''
    Parameters
    ----------
    minutes : str
        A number (usually two digit).

    Returns
    -------
    int
        Converts minutes to seconds.
    '''
    return int(minutes)*60

def hours_to_minutes( hours: str ) -> int:
    '''
    Parameters
    ----------
    hours : str
        A number (usually two digit).

    Returns
    -------
    int
        Converts hours to minutes.

    '''
    return int(hours)*60

def hhmm_to_seconds( hhmm: str ) -> int:
    '''
    Parameters
    ----------
    hhmm : str
        A clock time  in the format: HH:MM.

    Returns
    -------
    int
        Converts a timne into the number of seconds since midnight.

    '''
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
        minutes_to_seconds(hhmm.split(':')[1])

def hhmmss_to_seconds( hhmmss: str ) -> int:
    '''
    Parameters
    ----------
    hhmmss : str
        A clock time  in the format: HH:MM:SS.

    Returns
    -------
    int
        Converts a timne into the number of seconds since midnight.

    '''
    if len(hhmmss.split(':')) != 3:
        print('Incorrect format. Argument must be formatted as HH:MM:SS')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmmss.split(':')[0])) + \
        minutes_to_seconds(hhmmss.split(':')[1]) + int(hhmmss.split(':')[2])

def current_time_hhmm() -> None:
    '''
    Returns
    -------
    None
        Returns a string of the current time in the format HH:MM.

    '''
    return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)
