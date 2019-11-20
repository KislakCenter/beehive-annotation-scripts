#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 11:09:34 2019

@author: davidnelson

This script will automatically link cross references for the Beehive in the 
alphabetical section. It creates a csv that contains linked cross-references
that will work with wax.

The script will correct for incorrect capitalization, but is not yet able to 
deal with Pastorius's variant spellings and abbreviations.

The script will only work for alphabetical entries. Copy all index entries 
to a separate csv first.
"""

import pandas as pd
import re

# 'alpha_unlinked.csv' is the path to the source file
# 'alpha_linked.csv' is the new file you write to

def annotation_maker(fl, pid, ref):
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
    

def find_numbers(entry):
    return any(char.isdigit() for char in entry)
        
a = re.compile('alpha_\d+')
with open('alpha-unlinked.csv', 'r') as unlinked:
    df = pd.read_csv(unlinked)
    df.fillna('',inplace=True)
    
df['num_match'] = ''
for row in df.index:
    if df.loc[row,'pid'].startswith('num'):
        entry = str(df.loc[row,'entry'])
        topic = df.loc[row,'topic']
        num_match = f'{entry} [{topic}]'
        df.loc[row,'num_match'] = num_match
    
for row in df.index:
    xref = str(df.loc[row,'xref'])
    temp_list= []
    if '|' in xref:
        xrefs = xref.split('|')
        for i in xrefs: # for entries with multiple xrefs
            # control for case
            if find_numbers(i) == True:
                xref_num = int(re.search('\d+', i).group())
                if xref_num <= 496:
                        match = df[df['num_match'] == i]
                        pid = str(match['pid'].values).strip("['").strip("']")
                        if pid == '':
                            temp_list.append(i)
                        else:
                            annotation = num_annotation_maker(xref_num, pid, i)
                            temp_list.append(annotation)
                else:
                    temp_list.append(i)
            elif df['topic'].str.lower().isin([i.lower()]).any():
                try:
                    m = a.search(str(df.loc[df['topic'].str.lower().isin([i.lower()])]['pid'])).group()
                    s = (df.loc[df['topic'].str.lower().isin([i.lower()])]['first_letter'])
                    result = str(s.values).strip("['").strip("']")
                    if result.startswith(('A', 'B', 'C', 'D')):
                        annotation = f"<a href='/digital-beehive/alpha1/{m}/'>{i}</a>"
                        temp_list.append(annotation)
                    elif result.startswith(('E', 'F', 'G', 'H')):
                        annotation = f"<a href='/digital-beehive/alpha2/{m}/'>{i}</a>"
                        temp_list.append(annotation)
                    elif result.startswith(('I', 'K', 'L', 'M', 'N')):
                        annotation = f"<a href='/digital-beehive/alpha3/{m}/'>{i}</a>"
                        temp_list.append(annotation)
                    elif result.startswith(('O', 'P', 'Q', 'R', 'S')):
                        annotation = f"<a href='/digital-beehive/alpha4/{m}/'>{i}</a>"
                        temp_list.append(annotation)
                    else:
                        annotation = f"<a href='/digital-beehive/alpha5/{m}/'>{i}</a>"
                        temp_list.append(annotation)
                except AttributeError:
                    print(f'{xref} has a data issue.')
                    temp_list.append(i)
            else:
                temp_list.append(i) # this takes care of stray entries
    elif find_numbers(xref) == True:
        xref_num = int(re.search('\d+', xref).group())
        if xref_num <= 496:
            match = df[df['num_match'] == xref]
            pid = str(match['pid'].values).strip("['").strip("']")
            if pid == '':
                temp_list.append(xref)
            else: 
                annotation = num_annotation_maker(xref_num, pid, xref)
                temp_list.append(annotation)
        else:
            temp_list.append(xref)
    elif df['topic'].str.lower().isin([xref.lower()]).any(): # for entries with one alpha xref
        try:
            m = a.search(str(df.loc[df['topic'].str.lower().isin([xref.lower()])]['pid'])).group()
            s = (df.loc[df['topic'].str.lower().isin([xref.lower()])]['first_letter'])
            result = str(s.values).strip("['").strip("']")
            if result.startswith(('A', 'B', 'C', 'D')):
                annotation = f"<a href='/digital-beehive/alpha1/{m}/'>{xref}</a>"
                temp_list.append(annotation)
            elif result.startswith(('E', 'F', 'G', 'H')):
                annotation = f"<a href='/digital-beehive/alpha2/{m}/'>{xref}</a>"
                temp_list.append(annotation)
            elif result.startswith(('I', 'K', 'L', 'M', 'N')):
                annotation = f"<a href='/digital-beehive/alpha3/{m}/'>{xref}</a>"
                temp_list.append(annotation)
            elif result.startswith(('O', 'P', 'Q', 'R', 'S')):
                annotation = f"<a href='/digital-beehive/alpha4/{m}/'>{xref}</a>"
                temp_list.append(annotation)
            else:
                annotation = f"<a href='/digital-beehive/alpha5/{m}/'>{xref}</a>"
                temp_list.append(annotation)
        except AttributeError:
            print(f'{xref} has a data problem')
            temp_list.append(xref)
    else:
        temp_list.append(xref)

    new_xref = '|'.join(temp_list)
    df.loc[row,'xref'] = new_xref
print('Annotations created.')

linked_csv = df.to_csv('alpha-linked.csv', index=False) # This writes the new csv
                                                        # "False" removes info 
                                                        # added by pd.
print('Done.')


# df['topic'].lower().isin([i.lower()]).any() try this code for correcting for case
