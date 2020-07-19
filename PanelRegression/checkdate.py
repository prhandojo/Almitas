#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 17:16:52 2020

@author: kanp
"""

def Checkdate(start_datetime, end_datetime):

    # Need to refactor to switch case python see througth in python lib
    if not isinstance(start_datetime, datetime.date):
        raise TypeError(
            "Your start_datetime ({}) must be datetime object ,datetime(Y,m,d,H,M,S)".format(
                str(start_datetime)
            )
        )
    if not isinstance(end_datetime, datetime.date):
        raise TypeError(
            "Your end_datetime ({}) must be datetime object ,datetime(Y,m,d,H,M,S)".format(
                str(end_datetime)
            )
        )

    if start_datetime > datetime.datetime.now():
        raise ValueError(
            "Input start_datetime more than current time stock current time is {}".format(
                datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            )
        )
    if end_datetime > datetime.datetime.now():
        raise ValueError(
            "Input end_datetime more than current time stock current time is {}".format(
                datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            )
        )
    if start_datetime > end_datetime:
        raise ValueError(
            "Input start_datetime more than end_datetime select time should between {} and {}".format(
                start_datetime.strftime("%Y-%m-%d %H-%M-%S"),
                end_datetime.strftime("%Y-%m-%d %H-%M-%S"),
            )
        )
    if start_datetime.year < 2005:
        raise ValueError(
            "Your input year is "
            + str(start_datetime.year)
            + ". start_datetime must be after 2005"
        )
