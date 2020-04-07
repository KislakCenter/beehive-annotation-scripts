#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 11:03:56 2019

@author: davidnelson
"""

import csv


def find_numbers(entry):
    '''
    This function will determine if string input contains numbers or not.
    '''
    return any(char.isdigit() for char in entry)


def alpha_annotator(item, ref):
    '''
    This function will create links in HTML syntax to alphabetical
    entries in the Beehive
    '''
    pid = item['pid'].to_list()
    pid = pid[0]
    first_letter = item['first_letter'].to_list()
    first_letter = first_letter[0]
    if first_letter.startswith(('A', 'B', 'C', 'D')):
        return f"<a href='/digital-beehive/alpha1/{pid}/'>{ref}</a>"
    elif first_letter.startswith(('E', 'F', 'G', 'H')):
        return f"<a href='/digital-beehive/alpha2/{pid}/'>{ref}</a>"
    elif first_letter.startswith(('I', 'K', 'L', 'M', 'N')):
        return f"<a href='/digital-beehive/alpha3/{pid}/'>{ref}</a>"
    elif first_letter.startswith(('O', 'P', 'Q', 'R', 'S')):
        return f"<a href='/digital-beehive/alpha4/{pid}/'>{ref}</a>"
    else:
        return f"<a href='/digital-beehive/alpha5/{pid}/'>{ref}</a>"


def num_annotator(entry, ref):
    '''
    This function will create links in HTML syntax to numerical entries
    in the Beehive.
    '''
    try:
        pid = entry['pid'].to_list()
        pid = pid[0]
        num = entry['entry'].to_list()
        num = int(num[0])
    except AttributeError:
        pid = entry['pid']
        num = int(entry['entry'])
    if int(num) <= 250:
        return f"<a href='/digital-beehive/num1/{pid}/'>{ref}</a>"
    elif int(num) > 250:
        return f"<a href='/digital-beehive/num2/{pid}/'>{ref}</a>"


def corrections_annotator(entry, ref):
    pid = entry['pid'].to_list()
    pid = pid[0]
    if pid.startswith('num'):
        return num_annotator(entry, ref)
    elif pid.startswith('alpha'):
        return alpha_annotator(entry, ref)


def index_annotator(item, ref):
    '''
    This function will create links in HTML syntax to index headers in
    the Beehive.
    '''
    pid = item['pid'].to_list()
    pid = pid[0]
    first_letter = item['first_letter'].to_list()
    first_letter = first_letter[0]
    if first_letter.startswith(('A', 'B', 'C', 'D')):
        return f"<a href='/digital-beehive/index1/{pid}/'>{ref}</a>"
    elif first_letter.startswith(('E', 'F', 'G', 'H')):
        return f"<a href='/digital-beehive/index2/{pid}/'>{ref}</a>"
    elif first_letter.startswith(('I', 'K', 'L', 'M', 'N')):
        return f"<a href='/digital-beehive/index3/{pid}/'>{ref}</a>"
    elif first_letter.startswith(('O', 'P', 'Q', 'R', 'S')):
        return f"<a href='/digital-beehive/index4/{pid}/'>{ref}</a>"
    else:
        return f"<a href='/digital-beehive/index5/{pid}/'>{ref}</a>"


def write_csv(infile, outfile, cond, data):
    with open(infile, 'r') as ip, open(outfile, 'w') as f:
        reader = csv.DictReader(ip, delimiter=',')
        fields = reader.fieldnames
        writer = csv.DictWriter(f, delimiter=',', fieldnames=fields)
        writer.writeheader()
        for row in reader:
            if row[data].startswith(cond):
                writer.writerow(row)


def write_num_csv(infile, outfile, cond1, cond2):
    with open(infile, 'r') as ip, open(outfile, 'w') as f:
        reader = csv.DictReader(ip, delimiter=',')
        fields = reader.fieldnames
        writer = csv.DictWriter(f, delimiter=',', fieldnames=fields)
        writer.writeheader()
        for row in reader:
            if row['pid'].startswith('num'):
                if cond1 <= int(row['entry']) <= cond2:
                    writer.writerow(row)


def add_or_append(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)


def load_corrections(data):
    with open(data, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        corrections = {}
        for row in reader:
            corrections.update({row['input']: row['match']})
        return corrections


def load_issues(data):
    with open(data, 'r') as f:
        reader = csv.DictReader(f, delimiter=',')
        issues = {}
        for row in reader:
            add_or_append(issues, row['item'], row['problem'])
        for i in issues.keys():
            issues[i] = '|'.join(issues[i])
        return issues
