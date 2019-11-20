#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:19:13 2019

@author: davidnelson

This script will link up the index to the Alvearium of Pastorius's
"Bee-Hive" manuscript. You will need a cleaned-up copy of the most recent data 
export. The end of the script will break the index and Alvearium into two 
separate files for further manipulation.
"""

import pandas as pd
import re
import csv

def alpha_annotation_maker(fl, pid, ref):
    if fl.startswith(('A','B','C','D')):
        return f"<a href='/digital-beehive/alpha1/{pid}/'>{ref}</a>"
    elif fl.startswith(('E', 'F', 'G', 'H')):
        return f"<a href='/digital-beehive/alpha2/{pid}/'>{ref}</a>"
    elif fl.startswith(('I', 'K', 'L', 'M', 'N')):
        return f"<a href='/digital-beehive/alpha3/{pid}/'>{ref}</a>"
    elif fl.startswith(('O', 'P', 'Q', 'R', 'S')):
        return f"<a href='/digital-beehive/alpha4/{pid}/'>{ref}</a>"
    else:
        return f"<a href='/digital-beehive/alpha5/{pid}/'>{ref}</a>"

def num_annotation_maker(entry, pid, ref):
    if int(entry) <= 250:
        return f"<a href='/digital-beehive/num1/{pid}/'>{ref}</a>"
    elif int(entry) > 250:
        return f"<a href='/digital-beehive/num2/{pid}/'>{ref}</a>"
    
def index_annotation_maker(fl, pid, ref):
    if fl.startswith(('A','B','C','D')):
        return f"<a href='/digital-beehive/index1/{pid}/'>{ref}</a>"
    elif fl.startswith(('E', 'F', 'G', 'H')):
        return f"<a href='/digital-beehive/index2/{pid}/'>{ref}</a>"
    elif fl.startswith(('I', 'K', 'L', 'M', 'N')):
        return f"<a href='/digital-beehive/index3/{pid}/'>{ref}</a>"
    elif fl.startswith(('O', 'P', 'Q', 'R', 'S')):
        return f"<a href='/digital-beehive/index4/{pid}/'>{ref}</a>"
    else:
        return f"<a href='/digital-beehive/index5/{pid}/'>{ref}</a>"
    
def find_numbers(entry):
    return any(char.isdigit() for char in entry)

a = re.compile('alpha_\d+')
idx = re.compile('index_\d+')
num = re.compile('\d+')
with open('beehive-data-toc-link.csv', 'r') as unlinked:
    df = pd.read_csv(unlinked)
    df.fillna('',inplace=True)
    
    #create dummy column for numerical entry matching
df['num_match'] = ''
for row in df.index:
    if df.loc[row,'pid'].startswith('num'):
        entry = str(df.loc[row,'entry'])
        topic = df.loc[row,'topic']
        num_match = f'{entry} [{topic}]'
        df.loc[row,'num_match'] = num_match

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
                        try: 
                            m = a.search(str(df.loc[df['index'].isin([head])]['pid'])).group()
                            n = num.search(str(df.loc[df['index'].isin([head])]['topic'])).group()
                            topic = str(df.loc[df['index'].isin([head])]['topic']).strip(n).strip('Name: topic, dtype: object').rstrip()
                            s = (df.loc[df['index'].isin([head])]['first_letter'])
                            result = str(s.values).strip("['").strip("']")
                            annotation = alpha_annotation_maker(result, m, 'a')
                            entry_list.append(annotation)
                        except AttributeError:
                            print(f'"{head}" has problematic data.')
                            entry_list.append(i)
                # numerical section annotated up until 400 for now, so we 
                # can try to link these
                elif find_numbers(i) == True:
                    num_entry = int(re.search('\d+', i).group())
                    if num_entry <= 496:
                        match = df[df['num_match'] == i]
                        pid = match['pid'].tolist()
                        pid = ''.join(pid)
                        if pid == '':
                            entry_list.append(i)
                        else:
                            annotation = num_annotation_maker(num_entry, pid, i)
                            entry_list.append(annotation)
                    else:
                        entry_list.append(i)
                else:
                    entry_list.append(i)
        elif 'a' == entry:
            if df['index'].isin([head]).any():
                m = a.search(str(df.loc[df['index'].isin([head])]['pid'])).group()
                n = num.search(str(df.loc[df['index'].isin([head])]['topic'])).group()
                topic = str(df.loc[df['index'].isin([head])]['topic']).strip(n).strip('Name: topic, dtype: object').rstrip()
                s = (df.loc[df['index'].isin([head])]['first_letter'])
                result = str(s.values).strip("['").strip("']")
                annotation = alpha_annotation_maker(result, m, 'a')
                entry_list.append(annotation)
            else:
                entry_list.append(entry)
        elif find_numbers(entry) == True:
            num_entry = int(re.search('\d+', entry).group())
            if num_entry <=496:
                match = df[df['num_match'] == entry]
                pid = str(match['pid'].values).strip("['").strip("']")
                if pid == '':
                    entry_list.append(entry)
                else:
                    annotation = num_annotation_maker(num_entry, pid, entry)
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
    df = pd.read_csv(temp)
    df.fillna('',inplace=True)
for row in df.index:
    index = str(df.loc[row,'index'])
    if index != '':
        index_list = []
        if '|' in index:
            indices = index.split('|')
            for i in indices:
                if df['head'].isin([i]).any():
                    ind = idx.search(str(df.loc[df['head'].isin([i])]['pid'])).group()
                    s = (df.loc[df['head'].isin([i])]['first_letter'])
                    result = str(s.values).strip("['").strip("']")
                    annotation = index_annotation_maker(result, ind, i)
                    index_list.append(annotation)         
        elif df['head'].isin([index]).any():
            ind = idx.search(str(df.loc[df['head'].isin([index])]['pid'])).group()
            s = (df.loc[df['head'].isin([index])]['first_letter'])
            result = str(s.values).strip("['").strip("']")
            annotation = index_annotation_maker(result, ind, index)
            index_list.append(annotation)
        else:
            index_list.append(index)
        new_index = '|'.join(index_list)
        df.loc[row,'index'] = new_index      
            
df = df.drop(['num_match'], axis=1)
linked_csv = df.to_csv('beehive-data-linked.csv', index=False)
print('Alphabetical section linked.')

with open('beehive-data-linked.csv', 'r') as infile, open('alpha-unlinked.csv', 'w') as outfile:
    reader = csv.DictReader(infile, delimiter=',')
    fields = reader.fieldnames
    writer = csv.DictWriter(outfile, delimiter=',', fieldnames=fields)
    writer.writeheader()
    for row in reader:
        if row['pid'].startswith('alpha'):
            writer.writerow(row)
        elif row['pid'].startswith('num'):
            writer.writerow(row)
    print('Alphabetical section separated.')

with open('beehive-data-linked.csv', 'r') as infile, open('index-linked.csv', 'w') as outfile:
    reader = csv.DictReader(infile, delimiter=',')
    writer = csv.DictWriter(outfile, delimiter=',', fieldnames=fields)
    writer.writeheader()
    for row in reader:
        if row['pid'].startswith('index'):
            writer.writerow(row)
    print('Index separated.')
