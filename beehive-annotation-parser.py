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
import beehive
import os

# =============================================================================
# The first part of the script will create links between the Alvearium and the
# Octavo Index. At the end, it provides clean files of both sections for
# further use.
# =============================================================================

a = re.compile(r'alpha_\d+')
idx = re.compile(r'index_\d+')
num = re.compile(r'\d+')
with open('data/beehive-data-for-wax.csv', 'r') as unlinked:
    df = pd.read_csv(unlinked)
    df.fillna('', inplace=True)
    

# get pids from toc

with open('data/master_toc.csv', 'r') as f:
    toc = csv.DictReader(f, delimiter=',')
    pages = {}
    for row in toc:
        if row['volume'] == '2':
            if beehive.find_numbers(row['first_entry']) is True:
                page_range = list(range(int(row['first_entry']),
                                        int(row['last_entry']) + 1))
                pages.update({row['pid']: page_range})

toc_link = "<a href='/digital-beehive/toc/"

# create dummy column for numerical entry matching
df['num_match'] = ''
for row in df.index:
    if df.loc[row, 'pid'].startswith('num'):
        entry = str(df.loc[row, 'entry'])
        topic = df.loc[row, 'topic']
        num_match = f'{entry} [{topic}]'
        df.loc[row, 'num_match'] = num_match

with open('issues_parse_alvearium.txt', 'w') as issues:
    for row in df.index:
        head = str(df.loc[row, 'head'])
        if head != '': # script is identifying Vol. 1 and Vol. 2 to work on
            entry = str(df.loc[row, 'entry'])
            entry_list = []
            if '|' in entry:
                entries = entry.split('|')
                for i in entries:
                    if i == 'a':
                        # Since the index is added manually to each alphabetical
                        # entry, we don't need to control for case.
                        index_match = df[df['index'] == head]
                        try:
                            annotation = beehive.alpha_annotator(index_match, 'a')
                            entry_list.append(annotation)
                        except IndexError:
                            issues.write("%s\n" % f'{entry}')
                            issues.write("%s\n" % f'{head} has a problem with "a."')
                            print(f'{head} has a problem with "a."')
                            entry_list.append(i)
                    # numerical section annotated up to 1000 for now, so we
                    # can try to link these. Adjust number at next datapull
                    elif beehive.find_numbers(i) is True:
                        num_entry = int(re.search(r'\d+', i).group())
                        if '[PAGE_MISSING' in i:
                            entry_list.append(i)
                        elif num_entry <= 4927:
                            match = df[df['num_match'] == i]
                            try:
                                annotation = beehive.num_annotator(match, i)
                                entry_list.append(annotation)
                            except IndexError:
                                issues.write("%s\n" % f'{entry}')
                                issues.write("%s\n" % f'{head} has a numerical problem.')
                                print(f'{head} has a numerical problem.')
                                entry_list.append(i)
                        else:
                            for pid, contents in pages.items():
                                if num_entry in contents:
                                    annotation = f"{toc_link}{pid}/'>{i}</a>"
                                    entry_list.append(annotation)
                                else:
                                    continue
                    else:
                        entry_list.append(i)
            elif entry == 'a':
                index_match = df[df['index'] == head]
                try:
                    annotation = beehive.alpha_annotator(index_match, 'a')
                    entry_list.append(annotation)
                except IndexError:
                    issues.write("%s\n" % f'{entry}')
                    issues.write("%s\n" % f'{head} has a problem with "a."')
                    print(f'{head} has a problem with "a."')
                    entry_list.append(entry)
            elif beehive.find_numbers(entry) is True:
                num_entry = int(re.search(r'\d+', entry).group())
                if '[PAGE_MISSING' in entry:
                    entry_list.append(entry)
                elif num_entry <= 4927:
                    match = df[df['num_match'] == entry]
                    try:
                        annotation = beehive.num_annotator(match, entry)
                        entry_list.append(annotation)
                    except IndexError:
                        issues.write("%s\n" % f'{entry}')
                        issues.write("%s\n" % f'{head} has a numerical problem.')
                        print(f'{head} has a numerical problem.')
                        entry_list.append(entry)
                else:
                    for pid, contents in pages.items():
                        if num_entry in contents:
                            annotation = f"{toc_link}{pid}/'>{entry}</a>"
                            entry_list.append(annotation)
                        else:
                            continue
            else:
                entry_list.append(entry)   
            new_entry = '|'.join(entry_list)
            df.loc[row, 'entry'] = new_entry

issues.close()


print('Links to Alvearium done.')

# write links to index

with open('issues_parse_index.txt', 'w') as issues:

    for row in df.index:
        index = str(df.loc[row, 'index'])
        if index != '':
            index_list = []
            if '|' in index:
                indices = index.split('|')
                for i in indices:
                    index_match = df[df['head'] == i]
                    try:
                        annotation = beehive.index_annotator(index_match, i)
                        index_list.append(annotation)
                    except IndexError:
                        issues.writelines("%s\n" % f"{df.loc[row, 'entry']} {df.loc[row, 'topic']} has an index problem.")
                        print(f"{df.loc[row, 'entry']} {df.loc[row, 'topic']} has an index problem.")
                        index_list.append(i)
            # handle missing entries separately to avoid excessive errors
            elif index == '[NOT_IN_INDEX]':
                index_list.append(index)
            else:
                index_match = df[df['head'] == index]
                try:
                    annotation = beehive.index_annotator(index_match, index)
                    index_list.append(annotation)
                except IndexError:
                    issues.writelines("%s\n" % f"{df.loc[row, 'entry']} [{df.loc[row, 'topic']}] has an index problem.")
                    print(f"{df.loc[row, 'entry']} [{df.loc[row, 'topic']}] has an index problem.")
                    index_list.append(index)
            new_index = '|'.join(index_list)
            df.loc[row, 'index'] = new_index

    df = df.drop(['num_match'], axis=1)

issues.close()

# write issues from issue trackers

df['issue'] = ''

# load issues

alpha_issues = beehive.load_issues('data/alpha-issues.csv')
num_issues = beehive.load_issues('data/num-issues.csv')
index_issues = beehive.load_issues('data/index-issues.csv')

for i in alpha_issues.keys():
    match = df.index[df['item'] == i].tolist()
    df.loc[match, 'issue'] = alpha_issues[i]

for i in num_issues.keys():
    match = df.index[df['item'] == i].tolist()
    df.loc[match, 'issue'] = num_issues[i]

for i in index_issues.keys():
    match = df.index[df['item'] == i].tolist()
    df.loc[match, 'issue'] = index_issues[i]

linked_csv = df.to_csv('beehive-data-linked.csv', index=False)
print('Links to index done.')

beehive.write_csv(
        'beehive-data-linked.csv', 'alvearium.csv', ('alpha', 'num'), 'pid')
print('Alvearium separated')

beehive.write_csv(
        'beehive-data-linked.csv', 'beehive-index.csv', 'index', 'pid')
print('Index separted')

os.remove('beehive-data-linked.csv')

# =============================================================================
# The next part of the script creates cross-references between entries
# in the Alvearium. For numerical entries that have not yet been annotated,
# the script creates a link to the corresponding Wax ToC page. Note that this
# feature of the code will become obsolete when the entire Numerical Section
# has been annotated.
# =============================================================================

# load corrections

corrections = beehive.load_corrections('data/alpha-corrections.csv')

# create links to cross references

with open('alvearium.csv', 'r') as f:
    df = pd.read_csv(f)
    df.fillna('', inplace=True)

df['num_match'] = ''
for row in df.index:
    if df.loc[row, 'pid'].startswith('num'):
        entry = str(df.loc[row, 'entry'])
        topic = df.loc[row, 'topic']
        num_match = f'{entry} [{topic}]'
        df.loc[row, 'num_match'] = num_match

with open('issues_parse_alvearium_xref.txt', 'w') as issues:

    for row in df.index:
        xref = df.loc[row, 'xref']
        xref_list = []
        if '|' in xref:
            xrefs = xref.split('|')
            for i in xrefs:
                if i in corrections:  # we shouldn't get problems here, so no check
                    xref_match = df[df['item'] == corrections[i]]
                    annotation = beehive.alpha_annotator(xref_match, i)
                    xref_list.append(annotation)
                elif beehive.find_numbers(i) is True:
                    xref_num = int(re.search(r'\d+', i).group())
                    if '[PAGE_MISSING' in i:
                        xref_list.append(i)
                    elif xref_num <= 1000:
                        try:
                            xref_match = df[df['num_match'] == i]
                            annotation = beehive.num_annotator(xref_match, i)
                            xref_list.append(annotation)
                        except IndexError:
                            issues.writelines("%s\n" % f'Cross-reference {i} in entry '
                                  f"{df.loc[row, 'entry']} has a problem.")
                            print(f'Cross-reference {i} in entry '
                                  f"{df.loc[row, 'entry']} has a problem.")
                            xref_list.append(i)
                    else:
                        for pid, contents in pages.items():
                            if xref_num in contents:
                                a = f"{toc_link}{pid}/'>{i}</a>"
                                xref_list.append(a)
                            else:
                                continue
                elif i == '[WORD_MISSING]':  # tag used for bith xrefs and entries
                    xref_list.append(i)
                else:
                    xref_match = df[df['entry'].str.lower() == i.lower()]
                    try:
                        annotation = beehive.alpha_annotator(xref_match, i)
                        xref_list.append(annotation)
                    except IndexError:
                        issues.writelines("%s\n" % f'Cross-reference {i} in entry '
                             f"{df.loc[row, 'entry']} has a problem.")
                        print(f'Cross-reference {i} in entry'
                              f"{df.loc[row, 'entry']} has a problem.")
                        xref_list.append(i)
        else:
            if xref in corrections:
                xref_match = df[df['item'] == corrections[xref]]
                annotation = beehive.alpha_annotator(xref_match, xref)
                xref_list.append(annotation)
            elif xref == '':
                xref_list.append(xref)
            elif beehive.find_numbers(xref) is True:
                xref_num = int(re.search(r'\d+', xref).group())
                if '[PAGE_MISSING' in xref:
                    xref_list.append(xref)
                elif xref_num <= 1000:
                    try:
                        xref_match = df[df['num_match'] == xref]
                        annotation = beehive.num_annotator(xref_match, xref)
                        xref_list.append(annotation)
                    except IndexError:
                        issues.writelines("%s\n" % f'Cross-reference {xref} in entry '
                              f"{df.loc[row, 'entry']} has a problem.")
                        print(f'Cross-reference {xref} in entry '
                              f"{df.loc[row, 'entry']} has a problem.")
                        xref_list.append(xref)
                else:
                    for pid, contents in pages.items():
                        if xref_num in contents:
                            a = f"{toc_link}{pid}/'>{xref}</a>"
                            xref_list.append(a)
                        else:
                            continue
            elif xref == '[WORD_MISSING]':
                xref_list.append(xref)
            else:
                xref_match = df[df['entry'].str.lower() == xref.lower()]
                try:
                    annotation = beehive.alpha_annotator(xref_match, xref)
                    xref_list.append(annotation)
                except IndexError:
                    issues.writelines("%s\n" % f'Cross-reference {xref} in entry '
                              f"{df.loc[row, 'entry']} has a problem.")
                    print(f'Cross-reference {xref} in entry '
                          f"{df.loc[row, 'entry']} has a problem.")
                    xref_list.append(xref)
        new_xref = '|'.join(xref_list)
        df.loc[row, 'xref'] = new_xref

issues.close()

print('Alvearium cross-references created.')

# Create metadata that alerts user when a numerical entry shares an entry
# number with another entry

df['also_in_entry'] = ''

for row in df.index:
    entry = df.loc[row, 'entry']
    topic = df.loc[row, 'topic']
    also_in_list = []
    if beehive.find_numbers(entry) is True:
        entry_match = df[df['entry'] == entry]
        if len(entry_match) > 1:
            for item in entry_match.index:
                if df.iloc[item]['topic'] != topic:
                    also_entry = beehive.num_annotator(
                            df.iloc[item], df.iloc[item]['topic'])
                    also_in_list.append(also_entry)
    also_in = '|'.join(also_in_list)
    df.loc[row, 'also_in_entry'] = also_in

print('Also in data created.')

# =============================================================================
# Now we handle page links. You'll need the data file with Pastorius's
# pagination. Note that this file is different from the pages in the Table of
# Contents and must be updated to reflect the desired links.
# =============================================================================

with open('data/pastorius-pages.csv', 'r') as f:
    toc = csv.DictReader(f, delimiter=',')
    p_pages = {}
    for row in toc:
        p_pages.update({row['pastorius_page_numbers']: row['pid']})

with open('issues_parse_alvearium_page-xref.txt', 'w') as issues:

    for row in df.index:
        if df.loc[row, 'page'] != '':
            page = df.loc[row, 'page']
            p_list = []
            if '|' in page:
                paginae = page.split('|')
                for i in paginae:
                    pnumber = re.search(r'p.\d+', i).group().strip('p.')
                    if pnumber in p_pages:
                        n = p_pages[pnumber]
                        annotation = f"{toc_link}{n}/'>{i}</a>"
                        p_list.append(annotation)
                    else:
                        issues.writelines("%s\n" % f"{pnumber} for {df.loc[row, 'entry']} missing.")
                        print(f"{pnumber} for {df.loc[row, 'entry']} missing.")
                        p_list.append(i)
            else:
                pnumber = re.search(r'p.\d+', page).group().strip('p.')
                if pnumber in p_pages:
                    n = p_pages[pnumber]
                    annotation = f"{toc_link}{n}/'>{page}</a>"
                    p_list.append(annotation)
                else:
                    issues.writelines("%s\n" % f"{pnumber} for {df.loc[row, 'entry']} missing.")
                    print(f"{pnumber} for {df.loc[row, 'entry']} missing.")
                    p_list.append(page)
            new_page = '|'.join(p_list)
            df.loc[row, 'page'] = new_page

    df = df.drop(['num_match'], axis=1)
    new_csv = df.to_csv('data/alvearium-linked.csv', index=False)
    
issues.close()
    
print('Page references created for the Alvearium.')
os.remove('alvearium.csv')

with open('beehive-index.csv', 'r') as f:
    df = pd.read_csv(f)
    df.fillna('', inplace=True)

with open('issues_parse_index_page-xref.txt', 'w') as issues:

    for row in df.index:
        if df.loc[row, 'page'] != '':
            page = df.loc[row, 'page']
            p_list = []
            if '|' in page:
                paginae = page.split('|')
                for i in paginae:
                    pnumber = re.search(r'p.\d+', i).group().strip('p.')
                    if pnumber in p_pages:
                        n = p_pages[pnumber]
                        annotation = f"{toc_link}{n}/'>{i}</a>"
                        p_list.append(annotation)
                    else:
                        issues.writelines("%s\n" % f"{pnumber} for {df.loc[row, 'head']} missing.")
                        print(f"{pnumber} for {df.loc[row, 'head']} missing.")
                        p_list.append(i)
            else:
                pnumber = re.search(r'p.\d+', page).group().strip('p.')
                if pnumber in p_pages:
                    n = p_pages[pnumber]
                    annotation = f"{toc_link}{n}/'>{page}</a>"
                    p_list.append(annotation)
                else:
                    issues.writelines("%s\n" % f"{pnumber} for {df.loc[row, 'head']} missing.")
                    print(f"{pnumber} for {df.loc[row, 'head']} missing.")
                    p_list.append(page)
            new_page = '|'.join(p_list)
            df.loc[row, 'page'] = new_page
            
issues.close()            

print('Index page references created.')

# =============================================================================
# Now we handle see and add references in the index. Both of these can be
# problematic, so you will need the corresponding files for corrections.
# =============================================================================

corrections = beehive.load_corrections('data/index-see-corrections.csv')

with open('issues_parse_see-annotations.txt', 'w') as issues:

    for row in df.index:
        if df.loc[row, 'see'] != '':
            see = df.loc[row, 'see']
            see_list = []
            if '|' in see:
                vide = see.split('|')
                for i in vide:
                    if i in corrections:
                        see_match = df[df['item'] == corrections[i]]
                        annotation = beehive.index_annotator(see_match, i)
                        see_list.append(annotation)
                    else:
                        see_match = df[df['head'].str.lower() == i.lower()]
                        try:
                            annotation = beehive.index_annotator(see_match, i)
                            see_list.append(annotation)
                        except IndexError:
                            issues.writelines("%s\n" % f'See reference {i} for header '
                                  f"{df.loc[row, 'head']} has a problem.")
                            print(f'See reference {i} for header '
                                  f"{df.loc[row, 'head']} has a problem.")
                            see_list.append(i)
            else:
                if see in corrections:
                    see_match = df[df['item'] == corrections[see]]
                    annotation = beehive.index_annotator(see_match, see)
                    see_list.append(annotation)
                else:
                    see_match = df[df['head'].str.lower() == see.lower()]
                    try:
                        annotation = beehive.index_annotator(see_match, see)
                        see_list.append(annotation)
                    except IndexError:
                        issues.writelines("%s\n" % f'See reference {see} for header '
                              f"{df.loc[row, 'head']} has a problem.")
                        print(f'See reference {see} for header '
                              f"{df.loc[row, 'head']} has a problem.")
                        see_list.append(see)
            new_see = '|'.join(see_list)
            df.loc[row, 'see'] = new_see
            
issues.close()

print('See annotations created.')

# make add annotations

corrections = beehive.load_corrections('data/index-add-corrections.csv')

with open('issues_parse_add-annotations.txt', 'w') as issues:

    for row in df.index:
        if df.loc[row, 'add'] != '':
            add = df.loc[row, 'add']
            add_list = []
            if '|' in add:
                adde = add.split('|')
                for i in adde:
                    if i in corrections:
                        add_match = df[df['item'] == corrections[i]]
                        annotation = beehive.index_annotator(add_match, i)
                        add_list.append(annotation)
                    else:
                        add_match = df[df['head'].str.lower() == i.lower()]
                        try:
                            annotation = beehive.index_annotator(add_match, i)
                            add_list.append(annotation)
                        except IndexError:
                            issues.writelines("%s\n" % f'Add reference {i} for header '
                                  f"{df.loc[row, 'head']} has a problem.")
                            print(f'Add reference {i} for header '
                                  f"{df.loc[row, 'head']} has a problem.")
                            add_list.append(i)
            elif add in corrections:
                add_match = df[df['item'] == corrections[add]]
                annotation = beehive.index_annotator(add_match, add)
                add_list.append(annotation)
            else:
                add_match = df[df['head'].str.lower() == add.lower()]
                try:
                    annotation = beehive.index_annotator(add_match, add)
                    add_list.append(add)
                except IndexError:
                    issues.writelines("%s\n" % f'Add reference {add} for header '
                                  f"{df.loc[row, 'head']} has a problem.")
                    print(f'Add reference {add} for header '
                          f"{df.loc[row, 'head']} has a problem.")
                    add_list.append(add)
            new_add = '|'.join(add_list)
            df.loc[row, 'add'] = new_add
            
issues.close()

print('Add annotations created.')

# create insertion links

ins = re.compile(r'\[:\d+.\]')

crochets = {}  # get pids from insertions
for row in df.index:
    if df.loc[row, 'insertion'] != '':
        insertion = df.loc[row, 'insertion']
        pid = df.loc[row, 'pid']
        beehive.add_or_append(crochets, insertion, pid)

with open('issues_parse_index-crochets.txt', 'w') as issues:

    for row in df.index:
        ins_match = ins.match(str(df.loc[row, 'head']))
        key_list = []
        xref_list = []
        if ins_match is not None:
            head = df.loc[row, 'head']
            if head == '[:70.]':
                issues.writelines("%s\n" % 'Crochet [:70.] needs updated protocol!')
                print('Crochet [:70.] needs updated protocol!')
            else:
                key_list = crochets.get(head)
                for i in key_list:
                    xref = df.loc[df['pid'] == i]['head'].to_list()
                    xref = xref[0]
                    link = f"<a href='/digital-beehive/index5/{i}/'>{xref}</a>"
                    xref_list.append(link)
            annotation = '|'.join(xref_list)
            df.loc[row, 'insertion_xref'] = annotation

issues.close()

print('Index crochets linked.')

new_csv = df.to_csv('data/beehive-index-linked.csv', index=False)
print('Index file created.')
os.remove('beehive-index.csv')

print('Creating individual files for the Alvearium...')

beehive.write_csv('data/alvearium-linked.csv', 'data/alpha1.csv',
                  ('A', 'B', 'C', 'D'), 'first_letter')
beehive.write_csv('data/alvearium-linked.csv', 'data/alpha2.csv',
                  ('E', 'F', 'G', 'H'), 'first_letter')
beehive.write_csv('data/alvearium-linked.csv', 'data/alpha3.csv',
                  ('I', 'K', 'L', 'M', 'N'), 'first_letter')
beehive.write_csv('data/alvearium-linked.csv', 'data/alpha4.csv',
                  ('O', 'P', 'Q', 'R', 'S'), 'first_letter')
beehive.write_csv('data/alvearium-linked.csv', 'data/alpha5.csv',
                  ('T', 'U', 'W', 'X', 'Y', 'Z'), 'first_letter')
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num1.csv', 1, 250)
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num2.csv', 251, 500)
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num3.csv', 501, 725)
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num4.csv', 866, 1000)
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num5.csv', 1001, 1250)
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num6.csv', 1251, 1500)
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num7.csv', 1501, 1750)
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num8.csv', 1501, 1750)
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num9.csv', 1751, 2000)
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num10.csv', 2001, 2250)
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num11.csv', 2001, 2250)
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num12.csv', 2251, 4495)
beehive.write_num_csv('data/alvearium-linked.csv', 'data/num13.csv', 4496, 4927)

print('Creating individual files for the index...')

beehive.write_csv('data/beehive-index-linked.csv', 'data/index1.csv',
                  ('A', 'B', 'C', 'D'), 'first_letter')
beehive.write_csv('data/beehive-index-linked.csv', 'data/index2.csv',
                  ('E', 'F', 'G', 'H'), 'first_letter')
beehive.write_csv('data/beehive-index-linked.csv', 'data/index3.csv',
                  ('I', 'K', 'L', 'M', 'N'), 'first_letter')
beehive.write_csv('data/beehive-index-linked.csv', 'data/index4.csv',
                  ('O', 'P', 'Q', 'R', 'S'), 'first_letter')
beehive.write_csv('data/beehive-index-linked.csv', 'data/index5.csv',
                  ('T', 'U', 'W', 'X', 'Y', 'Z', 'i'), 'first_letter')
print('Done.')
