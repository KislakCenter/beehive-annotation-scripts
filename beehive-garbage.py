#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 10:02:33 2019

@author: davidnelson
"""

import pandas as pd
import re

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

def find_numbers(entry):
    return any(char.isdigit() for char in entry)

with open('alpha-linked.csv', 'r') as f:
    df = pd.read_csv(f)
    df.fillna('',inplace=True)
    
for row in df.index:
    xref = str(df.loc[row,'xref'])
    xref_list = []
    if '|' in xref:
        xrefs = xref.split('|')
        for i in xrefs:
            if find_numbers(i) == True:
                xref_list.append(i)
            elif i == '[WORD_MISSING]':
                xref_list.append(i)
            else:
                if df['entry'].str.lower().isin([i.lower().replace("'",'').replace('-','').rstrip('s').replace('mt', 'ment').replace('xst', 'christ').replace('[m]','m').replace('[n]','n')]).any():
                    a = re.search(r'alpha_\d+',str((df.loc[df['entry'].str.lower().isin([i.lower().replace("'",'').replace('-','').rstrip('s').replace('mt', 'ment').replace('xst', 'christ').replace('[m]','m').replace('[n]','n')])]['pid']))).group()
                    s = df.loc[df['entry'].str.lower().isin([i.lower().replace("'",'').replace('-','').rstrip('s').replace('mt', 'ment').replace('xst', 'christ').replace('[m]','m').replace('[n]','n')])]['first_letter']
                    result = str(s.values).strip("['").strip("']")
                    annotation = annotation_maker(result, a, i)
                    xref_list.append(annotation)
                elif df['entry'].str.lower().isin([i.lower() + 'ion']).any():
                    a = re.search(r'alpha_\d+',str((df.loc[df['entry'].str.lower().isin([i.lower() + 'ion'])]['pid']))).group()
                    s = df.loc[df['entry'].str.lower().isin([i.lower() + 'ion'])]['first_letter']
                    result = str(s.values).strip("['").strip("']")
                    annotation = annotation_maker(result, a, i)
                    xref_list.append(annotation)
                elif df['entry'].str.lower().isin([i.lower() + 'ness']).any():
                    a = re.search(r'alpha_\d+',str((df.loc[df['entry'].str.lower().isin([i.lower() + 'ness'])]['pid']))).group()
                    s = df.loc[df['entry'].str.lower().isin([i.lower() + 'ness'])]['first_letter']
                    result = str(s.values).strip("['").strip("']")
                    annotation = annotation_maker(result, a, i)
                    xref_list.append(annotation)
                elif df['entry'].str.lower().isin([i.lower() + 's']).any():
                    a = re.search(r'alpha_\d+',str((df.loc[df['entry'].str.lower().isin([i.lower() + 's'])]['pid']))).group()
                    s = df.loc[df['entry'].str.lower().isin([i.lower() + 's'])]['first_letter']
                    result = str(s.values).strip("['").strip("']")
                    annotation = annotation_maker(result, a, i)
                    xref_list.append(annotation)
                elif df['entry'].str.lower().isin([i.lower().replace('gods',"god's")]).any():
                    a = re.search(r'alpha_\d+',str((df.loc[df['entry'].str.lower().isin([i.lower().replace('gods',"god's")])]['pid']))).group()
                    s = df.loc[df['entry'].str.lower().isin([i.lower().replace('gods',"god's")])]['first_letter']
                    result = str(s.values).strip("['").strip("']")
                    annotation = annotation_maker(result, a, i)
                    xref_list.append(annotation)
                elif df['entry'].str.lower().isin([i.lower() + 'e']).any():
                    a = re.search(r'alpha_\d+',str((df.loc[df['entry'].str.lower().isin([i.lower() + 'e'])]['pid']))).group()
                    s = df.loc[df['entry'].str.lower().isin([i.lower() + 'e'])]['first_letter']
                    result = str(s.values).strip("['").strip("']")
                    annotation = annotation_maker(result, a, i)
                    xref_list.append(annotation)
                elif i == 'Discont':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Discontentment']['pid'])).group()
                    annotation = annotation_maker('D', a, i)
                    xref_list.append(annotation)
                elif i == 'Inequ.y':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Inequality']['pid'])).group()
                    annotation = annotation_maker('I', a, i)
                    xref_list.append(annotation)
                elif i == 'Hypocrisie':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Hypocrisy']['pid'])).group()
                    annotation = annotation_maker('H', a, i)
                    xref_list.append(annotation)
                elif i == 'New Testament':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'New Testamt']['pid'])).group()
                    annotation = annotation_maker('T', a, i)
                    xref_list.append(annotation)
                elif i == 'Com[m]andmt':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Com[m]andments'])).group()
                    annotation = annotation_maker('C', a, i)
                    xref_list.append(annotation)
                elif i == 'Unthankfullness':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Unthankfull']['pid'])).group()
                    annotation = annotation_maker('U', a, i)
                    xref_list.append(annotation)
                elif i == 'red haired':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Redhaired']['pid'])).group()
                    annotation = annotation_maker('R', a, i)
                    xref_list.append(annotation)
                elif i == 'Negligence':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Negligenge']['pid'])).group()
                    annotation = annotation_maker('N', a, i)
                    xref_list.append(annotation)
                elif i == 'Consid':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Considerateness']['pid'])).group()
                    annotation = annotation_maker('C', a, i)
                    xref_list.append(annotation)
                elif i.lower() == 'mediator':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Mediatour']['pid'])).group()
                    annotation = annotation_maker('M', a, i)
                    xref_list.append(annotation)
                elif i == 'Injust':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Injustice']['pid'])).group()
                    annotation = annotation_maker('I', a, i)
                    xref_list.append(annotation)
                elif i == 'Selfprofit':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Self profit']['pid'])).group()
                    annotation = annotation_maker('S', a, i)
                    xref_list.append(annotation)
                elif i == 'Servant':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Service']['pid'])).group()
                    annotation = annotation_maker('S', a, i)
                    xref_list.append(annotation)
                elif i == 'Doctorship':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Doctor']['pid'])).group()
                    annotation = annotation_maker('D', a, i)
                    xref_list.append(annotation)
                elif i == 'Minerals':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Mine Minerals']['pid'])).group()
                    annotation = annotation_maker('M', a, i)
                    xref_list.append(annotation)
                elif i == 'Small Way':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Broad & small way'])).group()
                    annotation = annotation_maker('W', a, i)
                    xref_list.append(annotation)
                elif i == 'Self-murd':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Self murder'])).group()
                    annotation = annotation_maker('S', a, i)
                    xref_list.append(annotation)
                elif i == 'disobed':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Disobedience'])).group()
                    annotation = annotation_maker('D', a, i)
                    xref_list.append(annotation)
                elif i == 'Stubborn':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Stubborness'])).group()
                    annotation = annotation_maker('S', a, i)
                    xref_list.append(annotation)
                elif i == 'Remission':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Remission of Sins'])).group()
                    annotation = annotation_maker('R', a, i)
                    xref_list.append(annotation)
                elif i == 'Impart':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Impartiality'])).group()
                    annotation = annotation_maker('I', a, i)
                    xref_list.append(annotation)
                elif i == 'Impat':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Impatience'])).group()
                    annotation = annotation_maker('I', a, i)
                    xref_list.append(annotation)
                elif i == 'Montebank':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Mountebank'])).group()
                    annotation = annotation_maker('M', a, i)
                    xref_list.append(annotation)
                elif i == 'Imposs':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Impossibility'])).group()
                    annotation = annotation_maker('I', a, i)
                    xref_list.append(annotation)
                elif i == 'Wisdom':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Wisedom'])).group()
                    annotation = annotation_maker('W', a, i)
                    xref_list.append(annotation)
                elif i == 'Worship':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Worshipping'])).group()
                    annotation = annotation_maker('W', a, i)
                    xref_list.append(annotation)
                elif i  == 'defense':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Defence'])).group()
                    annotation = annotation_maker('D', a, i)
                    xref_list.append(annotation)
                elif i == 'Too slow':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Too slow or quick'])).group()
                    annotation = annotation_maker('T', a, i)
                    xref_list.append(annotation)
                elif i == 'H. Ghost':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Holy Ghost'])).group()
                    annotation = annotation_maker('G', a, i)
                    xref_list.append(annotation)
                elif i == 'Pedantery':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Pedantry'])).group()
                    annotation = annotation_maker('P', a, i)
                    xref_list.append(annotation)
                elif i == 'will Worship':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Will-Worship'])).group()
                    annotation = annotation_maker('W', a, i)
                    xref_list.append(annotation)
                elif i == 'Livelyhood':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Livelihood'])).group()
                    annotation = annotation_maker('L', a, i)
                    xref_list.append(annotation)
                elif i == 'faithfullness':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Faithfulness'])).group()
                    annotation = annotation_maker('F', a, i)
                    xref_list.append(annotation)
                elif i == 'hotchpotch':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Hotch potch'])).group()
                    annotation = annotation_maker('H', a, i)
                    xref_list.append(annotation)
                elif i == 'many men':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Many men, many minds'])).group()
                    annotation = annotation_maker('H', a, i)
                    xref_list.append(annotation)
                elif i == 'Stubborn':
                    a = re.search(r'alpha_\d+', str(df.loc[df['entry'] == 'Stubborness'])).group()
                    annotation = annotation_maker('S', a , i)
                    xref_list.append(annotation)
                elif i == 'Prognostic':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Prognostications'])).group()
                    annotation = annotation_maker('P', a, i)
                    xref_list.append(annotation)
                elif i == 'ecclesiastical disc.':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Ecclesiastical discipline'])).group()
                    annotation = annotation_maker('E', a, i)
                    xref_list.append(annotation)
                elif i == 'martial discipl.':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Martial disciplines'])).group()
                    annotation = annotation_maker('W', a, i)
                    xref_list.append(annotation) 
                elif i == 'babling':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Babbling'])).group()
                    annotation = annotation_maker('B', a, i)
                    xref_list.append(annotation)
                elif i == 'Self-murther':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Self murder'])).group()
                    annotation = annotation_maker('S', a, i)
                    xref_list.append(annotation)
                elif i == 'Selfdenial':
                    a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Self denial'])).group()
                    annotation = annotation_maker('S', a, i)
                    xref_list.append(annotation)
                else:
                    xref_list.append(i)
    else:
        if find_numbers(xref) == True:
            xref_list.append(xref)
        elif xref == '':
            xref_list.append(xref)
        elif df['topic'].str.lower().isin([xref.lower().replace("'",'').replace('-','').rstrip('s').replace('mt', 'ment').replace('xst', 'christ').replace('[m]','m').replace('[n]','n')]).any():
            try:
                a = re.search(r'alpha_\d+',str((df.loc[df['entry'].str.lower().isin([xref.lower().replace("'",'').replace('-','').rstrip('s').replace('mt', 'ment').replace('xst', 'christ').replace('[m]','m').replace('[n]','n')])]['pid']))).group()
                s = df.loc[df['entry'].str.lower().isin([xref.lower().replace("'",'').replace('-','').rstrip('s').replace('mt', 'ment').replace('xst', 'christ').replace('[m]','m').replace('[n]','n')])]['first_letter']
                result = str(s.values).strip("['").strip("']")
                annotation = annotation_maker(result, a, xref)
                xref_list.append(annotation)
            except AttributeError:
                print(f'{xref} has a problem.')
                xref_list.append(xref)
        elif xref == 'Gods blessings':
            a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == "God's blessings"])).group()
            annotation = annotation_maker('G', a, xref)
            xref_list.append(annotation)
        elif xref == 'Love of Brethren':
            a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Love of the brethren'])).group()
            annotation = annotation_maker('L', a, xref)
            xref_list.append(annotation)
        elif xref == 'Civil':
            a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Civility'])).group()
            annotation = annotation_maker('C', a, xref)
            xref_list.append(annotation)
        elif xref == 'negligence':
            a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Negligenge'])).group()
            annotation = annotation_maker('N', a, xref)
            xref_list.append(annotation)
        elif xref == 'Hast':
            a = re.search(r'alpha_\d+',str(df.loc[df['entry'] == 'Haste'])).group()
            annotation = annotation_maker('H', a, xref)
            xref_list.append(annotation)    
        else:
            xref_list.append(xref)
    new_xref = '|'.join(xref_list)
    df.loc[row,'xref'] = new_xref

new_csv = df.to_csv('alpha-cleaned.csv', index=False)
print('Done.')
