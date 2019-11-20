#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 16:06:38 2019

@author: davidnelson
"""

import pandas as pd
import re

def add_or_append(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)

a = re.compile(r'\[:\d+.\]')
    
with open('index-add.csv', 'r') as f:
    df = pd.read_csv(f)
    df.fillna('',inplace=True)
    
crochets = {} # get pids from insertions
for row in df.index:
    if df.loc[row,'insertion'] != '':
        insertion = df.loc[row,'insertion']
        pid = df.loc[row,'pid']
        add_or_append(crochets, insertion, pid)

for row in df.index:
    match = a.match(str(df.loc[row,'head']))
    key_list = []
    xref_list = []
    if match is not None:
        head = df.loc[row,'head']
        if head == '[:70.]': # we don't yet have a way to annotate insertion 70
            print('Oops')
        else:
            key_list = crochets.get(head)
            for i in key_list:
                xref = str(df.loc[df['pid'] == i]['head'].values)
                xref = xref.strip("['").strip("']")
                link = f"<a href='/digital-beehive/index5/{i}/'>{xref}</a>"
                xref_list.append(link)
        annotation = '|'.join(xref_list)        
        df.loc[row,'insertion_xref'] = annotation
        
new_csv = df.to_csv('index-crochets.csv', index=False)
print('Done')
