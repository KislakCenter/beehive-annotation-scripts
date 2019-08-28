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

a = re.compile('alpha_\d+')
with open('alpha-unlinked.csv', 'r') as unlinked:
    df = pd.read_csv(unlinked)
    df.fillna('',inplace=True)
    for row in df.index:
        xref = str(df.loc[row,'xref'])
        temp_list= []
        if '|' in xref:
            xrefs = xref.split('|')
            for i in xrefs: # for entries with multiple xrefs
                # control for case
                if df['topic'].str.lower().isin([i.lower()]).any():
                    m = a.search(str(df.loc[df['topic'].str.lower().isin([i.lower()])]['pid'])).group()
                    s = (df.loc[df['topic'].str.lower().isin([i.lower()])]['first_letter'])
                    result = str(s.values).strip("['").strip("']")
                    if result.startswith(('A', 'B', 'C', 'D')):
                        annotation = f"<a href='/New_Beehive/alpha1/{m}/'>{i}</a>"
                        temp_list.append(annotation)
                    elif result.startswith(('E', 'F', 'G', 'H')):
                        annotation = f"<a href='/New_Beehive/alpha2/{m}/'>{i}</a>"
                        temp_list.append(annotation)
                    elif result.startswith(('I', 'K', 'L', 'M', 'N')):
                        annotation = f"<a href='/New_Beehive/alpha3/{m}/'>{i}</a>"
                        temp_list.append(annotation)
                    elif result.startswith(('O', 'P', 'Q', 'R', 'S')):
                        annotation = f"<a href='/New_Beehive/alpha4/{m}/'>{i}</a>"
                        temp_list.append(annotation)
                    else:
                        annotation = f"<a href='/New_Beehive/alpha5/{m}/'>{i}</a>"
                        temp_list.append(annotation)
                else:
                    print(f"Can't find {i}.")
                    temp_list.append(i) # this takes care of stray entries
        elif df['topic'].str.lower().isin([xref.lower()]).any(): # for entries with one alpha xref
                    m = a.search(str(df.loc[df['topic'].str.lower().isin([xref.lower()])]['pid'])).group()
                    s = (df.loc[df['topic'].str.lower().isin([xref.lower()])]['first_letter'])
                    result = str(s.values).strip("['").strip("']")
                    if result.startswith(('A', 'B', 'C', 'D')):
                        annotation = f"<a href='/New_Beehive/alpha1/{m}/'>{xref}</a>"
                        temp_list.append(annotation)
                    elif result.startswith(('E', 'F', 'G', 'H')):
                        annotation = f"<a href='/New_Beehive/alpha2/{m}/'>{xref}</a>"
                        temp_list.append(annotation)
                    elif result.startswith(('I', 'K', 'L', 'M', 'N')):
                        annotation = f"<a href='/New_Beehive/alpha3/{m}/'>{xref}</a>"
                        temp_list.append(annotation)
                    elif result.startswith(('O', 'P', 'Q', 'R', 'S')):
                        annotation = f"<a href='/New_Beehive/alpha4/{m}/'>{xref}</a>"
                        temp_list.append(annotation)
                    else:
                        annotation = f"<a href='/New_Beehive/alpha5/{m}/'>{xref}</a>"
                        temp_list.append(annotation)
        else:
            print(f"Can't find {xref}.")
            temp_list.append(xref)
        new_xref = '|'.join(temp_list)
        df.loc[row,'xref'] = new_xref
print('Annotations created.')
linked_csv = df.to_csv('alpha-linked.csv', index=False) # This writes the new csv
                                                        # "False" removes info 
                                                        # added by pd.
print('Done.')


# df['topic'].lower().isin([i.lower()]).any() try this code for correcting for case
