#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 11:17:36 2019

@author: davidnelson

This script will take a csv of the data pull of the alphabetical section and a 
separate csv of the index of the Beehive and turn the xrefs for page numbers 
into links to the corresponding page in the table of contents. 

In order to use this script, you will need both a copy of the table of contents
of volume two as a csv as well as the cleaned up version of the data pull.

Run the script to create alphabetical cross references first before running
this script. 
"""

import csv
import pandas as pd
import re

def find_numbers(entry):
    return any(char.isdigit() for char in entry)

with open('toc_vol2.csv', 'r') as f:
    toc = csv.DictReader(f, delimiter=',')
    pages = {}
    for row in toc:
        if find_numbers(row['first_entry']) == True:
            page_range = list(range(int(row['first_entry']), int(row['last_entry']) + 1))
            pages.update({row['pid']: page_range})

with open('alpha-linked.csv', 'r') as file:
    df = pd.read_csv(file)
    df.fillna('', inplace=True)
    for row in df.index:
        xref = str(df.loc[row,'xref'])
        xref_list = []
        if '|' in xref:
            xrefs = xref.split('|')
            for i in xrefs:
                if find_numbers(i) == False: # take care of stray entries
                    xref_list.append(i)
                elif i.startswith('<a href'): # get rid of alpha links
                        xref_list.append(i)
                elif i.endswith('[PAGE_MISSING]'): # preserve missing pages
                        xref_list.append(i)
                else:
                    num = int(re.search(r'\d+', i).group())
                    for pid, contents in pages.items():
                        if num in contents:
                            annotation = f"<a href='/New_Beehive/toc_vol2/{pid}/'>{i}</a>"
                            xref_list.append(annotation)
        else:
            if find_numbers(xref) == False:
                xref_list.append(xref)
            elif xref.startswith('<a href'):
                xref_list.append(xref)
            elif xref.endswith('[PAGE_MISSING]'):
                xref_list.append(xref)
            else:
                num = int(re.search(r'\d+', xref).group())
                for pid, contents in pages.items():
                    if num in contents:
                        annotation = f"<a href='/New_Beehive/toc_vol2/{pid}/'>{xref}</a>"
                        xref_list.append(annotation)
        new_xref = '|'.join(xref_list)
        df.loc[row,'xref'] = new_xref
        
linked_csv = df.to_csv('alpha-num-linked.csv', index=False)
print('Alphabetical section done.')

with open('index-linked.csv', 'r') as eff:
    idx = pd.read_csv(eff)
    idx.fillna('',inplace=True)
    for row in idx.index:
        entry = str(idx.loc[row,'entry'])
        entry_list = []
        if '|' in entry:
            entries = entry.split('|')
            for i in entries:
                if find_numbers(i) == False:
                    entry_list.append(i)
                elif i.startswith('<a href'):
                    entry_list.append(i)
                elif '[PAGE_MISSING' in i:
                    entry_list.append(i)
                else:
                    num = int(re.search(r'\d+', i).group())
                    for pid, contents, in pages.items():
                        if num in contents:
                            annotation = f"<a href='/New_Beehive/toc_vol2/{pid}/'>{i}</a>"
                            entry_list.append(annotation)
        else:
            if find_numbers(entry) == False:
                entry_list.append(entry)
            elif entry.startswith('<a href'):
                entry_list.append(entry)
            elif '[PAGE_MISSING' in entry:
                entry_list.append(entry)
            else:
                num = int(re.search(r'\d+', entry).group())
                for pid, contents in pages.items():
                    if num in contents:
                        annotation = f"<a href='/New_Beehive/toc_vol2/{pid}/'>{entry}</a>"
                        entry_list.append(annotation)
        new_entry = '|'.join(entry_list)
        idx.loc[row,'entry'] = new_entry

linked_index = idx.to_csv('index-num-linked.csv', index=False)
print('Index done.')