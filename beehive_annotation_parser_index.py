#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:19:13 2019

@author: davidnelson

This script will link up the index to the alphabetical section of Pastorius'
Beehive. You will need a cleaned-up copy of the most recent data export. The 
end of the script will break the index and alphabetical section into two 
separate files for further manipulation.
"""

import pandas as pd
import re
import csv

a = re.compile('alpha_\d+')
idx = re.compile('index_\d+')
num = re.compile('\d+')
with open('beehive-data.csv', 'r') as unlinked:
    df = pd.read_csv(unlinked)
    df.fillna('',inplace=True)
    for row in df.index:
        head = str(df.loc[row,'head'])
        if head != '':
            entry = str(df.loc[row,'entry'])
            entry_list = []
            if '|' in entry:
                entries = entry.split('|')
                for i in entries:
                    if i == 'a':
                        # Since the index is added manually to each alphabetical
                        # entry, we don't need to control for case.
                        if df['index'].isin([head]).any():
                            m = a.search(str(df.loc[df['index'].isin([head])]['pid'])).group()
                            n = num.search(str(df.loc[df['index'].isin([head])]['topic'])).group()
                            topic = str(df.loc[df['index'].isin([head])]['topic']).strip(n).strip('Name: topic, dtype: object').rstrip()
                            s = (df.loc[df['index'].isin([head])]['first_letter'])
                            result = str(s.values).strip("['").strip("']")
                            if result.startswith(('A', 'B', 'C', 'D')):
                                annotation = f"<a href='/New_Beehive/alpha1/{m}/'>a</a>"
                                entry_list.append(annotation)
                            elif result.startswith(('E', 'F', 'G', 'H')):
                                annotation = f"<a href='/New_Beehive/alpha2/{m}/'>a</a>"
                                entry_list.append(annotation)
                            elif result.startswith(('I', 'K', 'L', 'M', 'N')):
                                annotation = f"<a href='/New_Beehive/alpha3/{m}/'>a</a>"
                                entry_list.append(annotation)
                            elif result.startswith(('O', 'P', 'Q', 'R', 'S')):
                                annotation = f"<a href='/New_Beehive/alpha4/{m}/'>a</a>"
                                entry_list.append(annotation)
                            else:
                                annotation = f"<a href='/New_Beehive/alpha5/{m}/'>a</a>"
                                entry_list.append(annotation)
                    else:
                        entry_list.append(i)
            elif 'a' == entry:
                if df['index'].isin([head]).any():
                    m = a.search(str(df.loc[df['index'].isin([head])]['pid'])).group()
                    n = num.search(str(df.loc[df['index'].isin([head])]['topic'])).group()
                    topic = str(df.loc[df['index'].isin([head])]['topic']).strip(n).strip('Name: topic, dtype: object').rstrip()
                    s = (df.loc[df['index'].isin([head])]['first_letter'])
                    result = str(s.values).strip("['").strip("']")
                    if result.startswith(('A', 'B', 'C', 'D')):
                        annotation = f"<a href='/New_Beehive/alpha1/{m}/'>a</a>"
                        entry_list.append(annotation)
                    elif result.startswith(('E', 'F', 'G', 'H')):
                        annotation = f"<a href='/New_Beehive/alpha2/{m}/'>a</a>"
                        entry_list.append(annotation)
                    elif result.startswith(('I', 'K', 'L', 'M', 'N')):
                        annotation = f"<a href='/New_Beehive/alpha3/{m}/'>a</a>"
                        entry_list.append(annotation)
                    elif result.startswith(('O', 'P', 'Q', 'R', 'S')):
                        annotation = f"<a href='/New_Beehive/alpha4/{m}/'>a</a>"
                        entry_list.append(annotation)
                    else:
                        annotation = f"<a href='/New_Beehive/alpha5/{m}/'>a</a>"
                        entry_list.append(annotation)
                else:
                    entry_list.append(entry)
            else:
                entry_list.append(entry)
            new_entry = '|'.join(entry_list)
            df.loc[row,'entry'] = new_entry
temp_csv = df.to_csv('beehive-temp.csv', index=False)
print('Index linked.')
with open('beehive-temp.csv', 'r') as temp:
    df2 = pd.read_csv(temp)
    df2.fillna('',inplace=True)
    for row in df2.index:
        index = str(df2.loc[row,'index'])
        if index != '':
            if df2['head'].isin([index]).any():
                ind = idx.search(str(df.loc[df2['head'].isin([index])]['pid'])).group()
                s = (df.loc[df2['head'].isin([index])]['first_letter'])
                result = str(s.values).strip("['").strip("']")
                if result.startswith(('A', 'B', 'C', 'D')):
                    annotation = f"<a href='/New_Beehive/index1/{ind}/'>{index}</a>"
                elif result.startswith(('E', 'F', 'G', 'H')):
                    annotation = f"<a href='/New_Beehive/index2/{ind}/'>{index}</a>"
                elif result.startswith(('I', 'K', 'L', 'M', 'N')):
                    annotation = f"<a href='/New_Beehive/index3/{ind}/'>{index}</a>"
                elif result.startswith(('O', 'P', 'Q', 'R', 'S')):
                    annotation = f"<a href='/New_Beehive/index4/{ind}/'>{index}</a>"
                else:
                    annotation = f"<a href='/New_Beehive/index5/{ind}/'>{index}</a>"
            else:
                annotation = index
            df2.loc[row,'index'] = annotation       
            
linked_csv = df2.to_csv('beehive-data-linked.csv', index=False)
print('Alphabetical section linked.')

with open('beehive-data-linked.csv', 'r') as infile, open('alpha-linked.csv', 'w') as outfile:
    reader = csv.DictReader(infile, delimiter=',')
    fields = reader.fieldnames
    writer = csv.DictWriter(outfile, delimiter=',', fieldnames=fields)
    writer.writeheader()
    for row in reader:
        if row['pid'].startswith('alpha'):
            writer.writerow(row)
    print('Alphabetical section separated.')

with open('beehive-data-linked.csv', 'r') as infile, open('index-linked.csv') as outfile:
    reader = csv.DictReader(infile, delimiter=',')
    writer = csv.DictWriter(outfile, delimiter=',', fieldnames=fields)
    writer.writeheader()
    for row in reader:
        if row['pid'].startswith('index'):
            writer.writerow(row)
    print('Index separated.')
    