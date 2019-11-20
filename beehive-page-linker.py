#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 14:58:56 2019

@author: davidnelson
"""

import csv
import re
import pandas

def annotation_maker(fl, pid, ref):
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

with open('pastorius_pages.csv', 'r') as f:
    toc = csv.DictReader(f, delimiter=',')
    pages = {}
    for row in toc:
        pages.update({row['pastorius_page_numbers']: row['pid']})
            
with open('index-num-linked.csv', 'r') as file:
    df = pandas.read_csv(file)
    df.fillna('',inplace=True)
    for row in df.index:
        if df.loc[row,'page'] != '':
            page = str(df.loc[row,'page'])
            p_list = []
            if '|' in page:
                pnumbers = page.split('|')
                for i in pnumbers:
                    pnumber = re.search(r'p.\d+', i).group().strip('p.')
                    if pnumber in pages:
                        n = pages[pnumber]
                        annotation = f"<a href='/digital-beehive/toc/{n}/'>{i}</a>"
                        p_list.append(annotation)
                    else:
                        print(f"{pnumber} for {row} missing.")
                        p_list.append(i)
            else:
                pnumber = re.search(r'p.\d+', page).group().strip('p.')
                if pnumber in pages:
                    n = pages[pnumber]
                    annotation = f"<a href='/digital-beehive/toc/{n}/'>{page}</a>"
                    p_list.append(annotation)
                else:
                    print(f"{pnumber} for {row} missing.")
                    p_list.append(page)
            new_page = '|'.join(p_list)
            df.loc[row,'page'] = new_page
    print('Page annotations created.')
    for row in df.index:
        if df.loc[row,'see'] != '':
            see = str(df.loc[row,'see'])
            see_list = []
            if '|' in see:
                vide = see.split('|')
                for i in vide:
                    if df['head'].str.lower().isin([i.lower()]).any():
                        a = re.search(r'index_\d+',str((df.loc[df['head'].str.lower().isin([i.lower()])]['pid']))).group()
                        s = df.loc[df['head'].str.lower().isin([i.lower()])]['first_letter']
                        result = str(s.values).strip("['").strip("']")
                        annotation = annotation_maker(result, a, i)
                        see_list.append(annotation)
                    else: 
                        print(f'{i} for {row} missing.')
                        see_list.append(i)
            else:
                if df['head'].str.lower().isin([see.lower()]).any():
                    a = re.search(r'index_\d+',str((df.loc[df['head'].str.lower().isin([see.lower()])]['pid']))).group()
                    s = df.loc[df['head'].str.lower().isin([see.lower()])]['first_letter']
                    result = str(s.values).strip("['").strip("']")
                    annotation = annotation_maker(result, a, see)
                    see_list.append(annotation)
                else:
                    see_list.append(see)
            new_see = '|'.join(see_list)
            df.loc[row,'see'] = new_see
    print('See annotations created.')
                         
new_csv = df.to_csv('index-p-and-see.csv',index=False)
print('File complete.')
