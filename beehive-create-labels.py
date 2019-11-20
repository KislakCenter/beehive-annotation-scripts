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
        entry = str(df.loc[row,'entry'])
        if pid.startswith('alpha'):
            df.loc[row,'label'] = entry
        elif pid.startswith('num'):
            topic = str(df.loc[row,'topic'])
            df.loc[row,'label'] = f'{entry}. {topic}'
        elif pid.startswith('index'):
            head = str(df.loc[row,'head'])
            df.loc[row,'label'] = head

new_csv = df.to_csv('beehive-data-label.csv',index=False)
print('Done')
        