#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 15:59:00 2019

@author: davidnelson
"""

import csv
import pandas as pd


def alpha_annotation_maker(fl, pid, ref):
    if fl.startswith(('A', 'B', 'C', 'D')):
        return f"<a href='/digital-beehive/alpha1/{pid}/'>{ref}</a>"
    elif fl.startswith(('E', 'F', 'G', 'H')):
        return f"<a href='/digital-beehive/alpha2/{pid}/'>{ref}</a>"
    elif fl.startswith(('I', 'K', 'L', 'M', 'N')):
        return f"<a href='/digital-beehive/alpha3/{pid}/'>{ref}</a>"
    elif fl.startswith(('O', 'P', 'Q', 'R', 'S')):
        return f"<a href='/digital-beehive/alpha4/{pid}/'>{ref}</a>"
    else:
        return f"<a href='/digital-beehive/alpha5/{pid}/'>{ref}</a>"


def index_annotation_maker(fl, pid, ref):
    if fl.startswith(('A', 'B', 'C', 'D')):
        return f"<a href='/digital-beehive/index1/{pid}/'>{ref}</a>"
    elif fl.startswith(('E', 'F', 'G', 'H')):
        return f"<a href='/digital-beehive/index2/{pid}/'>{ref}</a>"
    elif fl.startswith(('I', 'K', 'L', 'M', 'N')):
        return f"<a href='/digital-beehive/index3/{pid}/'>{ref}</a>"
    elif fl.startswith(('O', 'P', 'Q', 'R', 'S')):
        return f"<a href='/digital-beehive/index4/{pid}/'>{ref}</a>"
    else:
        return f"<a href='/digital-beehive/index5/{pid}/'>{ref}</a>"


def num_annotation_maker(entry, pid, ref):
    if int(entry) <= 4927:
        return f"<a href='/digital-beehive/num1/{pid}/'>{ref}</a>"
    elif int(entry) > 4927:
        return f"<a href='/digital-beehive/num2/{pid}/'>{ref}</a>"


with open('data/beehive-data-for-wax.csv', 'r') as ip:
    bh_data = csv.DictReader(ip, delimiter=',')
    ids = {}
    for row in bh_data:
        ids.update({row['item']: row['pid']})

with open('data/alpha-issues.csv', 'r') as f:
    alpha_issues = pd.read_csv(f)

for row in alpha_issues.index:
    item = alpha_issues.loc[row, 'item']
    entry = alpha_issues.loc[row, 'entry']
    first_letter = alpha_issues.loc[row, 'first_letter']
    pid = ids[item]
    link = alpha_annotation_maker(first_letter, pid, entry)
    alpha_issues.loc[row, 'reference_link'] = link

new_csv = alpha_issues.to_csv('alpha-issues.csv', index=False)
print('Alphabetical section done.')

with open('data/index-issues.csv', 'r') as f:
    index_issues = pd.read_csv(f)

for row in index_issues.index:
    item = index_issues.loc[row, 'item']
    head = index_issues.loc[row, 'head']
    first_letter = index_issues.loc[row, 'first_letter']
    pid = ids[item]
    link = index_annotation_maker(first_letter, pid, head)
    index_issues.loc[row, 'reference_link'] = link

new_csv = index_issues.to_csv('index-issues.csv', index=False)
print('Index done.')

with open('data/num-issues.csv', 'r') as f:
    num_issues = pd.read_csv(f)

for row in num_issues.index:
    item = num_issues.loc[row, 'item']
    entry = str(num_issues.loc[row, 'entry'])
    topic = num_issues.loc[row, 'topic']
    pid = ids[item]
    reference = f'{entry} [{topic}]'
    link = num_annotation_maker(entry, pid, reference)
    num_issues.loc[row, 'reference_link'] = link

new_csv = num_issues.to_csv('num-issues.csv', index=False)
print('Numerical section done.')
