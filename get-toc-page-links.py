#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 10:08:44 2019

@author: davidnelson

This code will create links for entries in the Beehive data export
to their corresponding page generated from the Table of Contents csv.
You will need a cleaned-up version of the data export (run the sorting script
first) and a copy of the master csv.
"""

import csv
import pandas as pd

def get_pids(data):
    reader = csv.DictReader(data)
    pages = {}
    for row in reader:
        vol = row['volume']
        img = str(row['image']).zfill(3)
        loc = f'{vol}.{img}'
        pages.update({loc: row['pid']})
    return pages

with open('master_toc.csv', 'r') as f1:
    toc = get_pids(f1)

with open('beehive-data-label.csv', 'r') as f:
    df = pd.read_csv(f)
    df.fillna('',inplace=True)
    df['location'] = ''
    for row in df.index:
        volume = str(df.loc[row,'volume'])
        volume = volume.strip('Volume ')
        image = str(df.loc[row,'image_number']).zfill(3)
        loc = f'{volume}.{image}'
        try:
            pid = toc[loc]
            pid_link = f"<a href='/digital-beehive/toc/{pid}/'>Full Page</a>"
            df.loc[row,'location'] = pid_link
        except:
            print(f"Data bad for {df.loc[row,'pid']}.")
        
new_csv = df.to_csv('beehive-data-toc-link.csv', index=False)
print('Done.')
