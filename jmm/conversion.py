#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""

import json

import pandas


def json2csv(path_or_content, destination=None, shuffle=False):
    """
    """
    df = pandas.read_json(path_or_content)
    if shuffle:
        df = df.sample(frac=1)
    
    if destination:
        return df.to_csv(destination, index=False)
    else:
        return df.to_csv(index=False)
