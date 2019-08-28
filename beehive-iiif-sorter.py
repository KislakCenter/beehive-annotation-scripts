#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 10:35:28 2019

@author: davidnelson
"""

# sort IIIF images by y values (second number) for alphabetical
# for index, need first to sort in ranges by x value
# first column: 100-500
# second column: 700 - 1300
# third coolumn >= 1300

# these values are a test, so there should also be a print statement to 
# throw out any other stuff

import re
import pandas as pd

def find_x_value(item):
    loc = re.compile('/\d+,\d+,\d+,\d+/')
    loc_info = loc.search(item).group()
    end_value = re.compile(',\d+,\d+,\d+/')
    strip = end_value.search(loc_info).group()
    loc_info = loc_info.replace(strip, '')
    loc_info = loc_info.strip('/')
    return(loc_info)
    
def find_y_value(item):
    loc = re.compile('/\d+,\d+,\d+,\d+/')
    loc_info = loc.search(item).group()
    front_value = re.compile('/\d+,')
    back_value = re.compile(',\d+,\d+/')
    to_strip = front_value.search(loc_info).group()
    also_strip = back_value.search(loc_info).group()
    loc_info = loc_info.replace(to_strip, '')
    loc_info = loc_info.replace(also_strip, '')
    return(loc_info)

with open('beehive-data-raw.csv', 'r') as f:
    df = pd.read_csv(f)
    df.fillna('',inplace=True)
    df['x_value'] = ''
    df['y_value'] = ''
    for row in df.index:
        url = df.loc[row,'selection']
        new_x_value = find_x_value(url)
        df.loc[row,'x_value'] = new_x_value
        new_y_value = find_y_value(url)
        df.loc[row,'y_value'] = new_y_value
        
new_csv = df.to_csv('beehive-data-for-sorting.csv', index=False)
print('Done.')

