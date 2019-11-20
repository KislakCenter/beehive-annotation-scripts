#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 13:19:44 2019

@author: davidnelson
"""

import pandas as pd
import re

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
    
pid = re.compile('index_\d+')

with open('index-p-and-see.csv', 'r') as f:
    df = pd.read_csv(f)
    df.fillna('',inplace=True)

for row in df.index:
    if df.loc[row,'add'] != '':
        add = df.loc[row,'add']
        add_list = []
        if '|' in add:
            adde = add.split('|')
            for i in adde:
                if i == 'Arab':
                    num = pid.search(str(df.loc[df['head'] == 'arabia'])).group()
                    annotation = annotation_maker('A', num, i)
                    add_list.append(annotation)
                elif i == 'Eccles.':
                    num = pid.search(str(df.loc[df['head'] == 'ecclesiastical discipline'])).group()
                    annotation = annotation_maker('E', num, i)
                    add_list.append(annotation)
                elif i == 'martial':
                    num = pid.search(str(df.loc[df['head'] == 'martial discipline'])).group()
                    annotation = annotation_maker('M', num, i)
                    add_list.append(annotation)
                elif i == 'Concup':
                    num = pid.search(str(df.loc[df['head'] == 'concupiscence'])).group()
                    annotation = annotation_maker('C', num, i)
                    add_list.append(annotation)
                elif i == 'lasciv':
                    num = pid.search(str(df.loc[df['head'] == 'lascivious'])).group()
                    annotation = annotation_maker('L', num, i)
                    add_list.append(annotation)
                elif i == 'eye':
                    num = pid.search(str(df.loc[df['head'] == 'eye lust'])).group()
                    annotation = annotation_maker('E', num, i)
                    add_list.append(annotation)
                else:
                    num = pid.search(str(df.loc[df['head'].str.lower().isin([i.lower()])])).group()
                    s = df.loc[df['head'].str.lower().isin([i.lower()])]['first_letter']
                    result = str(s.values).strip("['").strip("']")
                    annotation = annotation_maker(result, num, i)
                    add_list.append(annotation)
        else:
            if df['head'].str.lower().isin([add.lower() + ' ' + df.loc[row,'head'].lower()]).any():
                num = pid.search(str(df.loc[df['head'].str.lower().isin([add.lower() + ' ' + df.loc[row,'head'].lower()])])).group()
                s = df.loc[df['head'].str.lower().isin([add.lower() + ' ' + df.loc[row,'head'].lower()])]['first_letter']
                result = str(s.values).strip("['").strip("']")
                annotation = annotation_maker(result, num, add)
                add_list.append(annotation)
            elif add == 'visitation':
                num = pid.search(str(df.loc[df['head'] == 'day of Visitn'])).group()
                annotation = annotation_maker('V', num, add)
                add_list.append(annotation)
            elif add == 'hell':
                num = pid.search(str(df.loc[df['head'] == 'Xts. descension into hell'])).group()
                annotation = annotation_maker('H', num, add)
                add_list.append(annotation)
            elif add == 'run[n] away':
                num = pid.search(str(df.loc[df['head'] == 'run away'])).group()
                annotation = annotation_maker('R', num, add)
                add_list.append(annotation)
            elif add == 'adiaph':
                num = pid.search(str(df.loc[df['head'] == 'adiaphory'])).group()
                annotation = annotation_maker('A', num, add)
                add_list.append(annotation)
            elif add == 'repentance':
                num = pid.search(str(df.loc[df['head'] == 'repentance late'])).group()
                annotation = annotation_maker('R', num, add)
                add_list.append(annotation)
            elif add == 'hands':
                num = pid.search(str(df.loc[df['head'] == 'laying on of hands'])).group()
                annotation = annotation_maker('H', num, add)
                add_list.append(annotation)
            elif add == 'term':
                num = pid.search(str(df.loc[df['head'] == 'term of life prefixt'])).group()
                annotation = annotation_maker('T', num, add)
                add_list.append(annotation)
            elif add == 'prayer':
                num = pid.search(str(df.loc[df['head'] == 'prayers & Lords prayer'])).group()
                annotation = annotation_maker('P', num, add)
                add_list.append(annotation)
            elif add == 'various':
                num = pid.search(str(df.loc[df['head'] == 'various lections'])).group()
                annotation = annotation_maker('U', num, add)
                add_list.append(annotation)
            elif add == 'Divinity':
                num = pid.search(str(df.loc[df['head'] == 'divinity scholastica'])).group()
                annotation = annotation_maker('D', num, add)
                add_list.append(annotation)
            elif add == 'change':
                num = pid.search(str(df.loc[df['head'] == 'change of Sex'])).group()
                annotation = annotation_maker('C', num, add)
                add_list.append(annotation)
            elif add == 'shells':
                num = pid.search(str(df.loc[df['head'] == 'shells of snails'])).group()
                annotation = annotation_maker('S', num, add)
                add_list.append(annotation)
            elif add == 'Wit':
                num = pid.search(str(df.loc[df['head'] == 'wit. witticism'])).group()   
                annotation = annotation_maker('W', num, add)
                add_list.append(annotation)
            elif add == 'lilly time':
                num = pid.search(str(df.loc[df['head'] == 'lillies'])).group()
                annotation = annotation_maker('L', num, add)
                add_list.append(annotation)
            elif add == 'dainties':
                num = pid.search(str(df.loc[df['head'] == 'Dainty meats'])).group()
                annotation = annotation_maker('D', num, add)
                add_list.append(annotation)
            elif add == 'worship':
                num = pid.search(str(df.loc[df['head'] == 'will worship'])).group()
                annotation = annotation_maker('W', num, add)
                add_list.append(annotation)
            elif add == 'kingdom':
                num = pid.search(str(df.loc[df['head'] == 'kingdom of God'])).group()
                annotation = annotation_maker('K', num, add)
                add_list.append(annotation)
            elif add == 'passive':
                num = pid.search(str(df.loc[df['head'] == 'passive obed'])).group()
                annotation = annotation_maker('P', num, add)
                add_list.append(annotation)
            elif df['head'].str.lower().isin([add.lower()]).any():
                num = pid.search(str(df.loc[df['head'].str.lower().isin([add.lower()])])).group()
                s = df.loc[df['head'].str.lower().isin([add.lower()])]['first_letter']
                result = str(s.values).strip("['").strip("']")
                annotation = annotation_maker(result, num, add)
                add_list.append(annotation)
            else:
                add_list.append(add)
        new_add = '|'.join(add_list)
        df.loc[row,'add'] = new_add
        
new_csv = df.to_csv('index-add.csv',index=False)
print('Done.')

# brother add love should be love of ye brethren?
# Country add fashions needs to be added — data entered as "See"
# Symboles add Motto needs to be added — data entered as "See"
