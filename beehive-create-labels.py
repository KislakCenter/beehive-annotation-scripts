#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 11:26:43 2019

@author: davidnelson
"""

import pandas as pd

with open('beehive-data.csv', 'r') as f:
    df = pd.read_csv(f)
    df.fillna('',inplace=True)
    df['label'] = ''
    for row in df.index:
        pid = str(df.loc[row, 'pid'])
        if pid.startswith('alpha'):
            entry = str(df.loc[row,'entry'])
            df.loc[row,'label'] = entry
        if pid.startswith('index'):
            head = str(df.loc[row,'head'])
            df.loc[row,'label'] = head

new_csv = df.to_csv('beehive-data-label.csv',index=False)
print('Done')
        