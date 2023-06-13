#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 10:35:28 2019

@author: davidnelson

The following script will take the data export from the Beehive and put it in
an order closely approximating Pastorius's order. As of 2019-25-11, all entries
should be correctly placed.

The code assumes that volumes one and two only needed to be sorted along the
y axis and that no boxes have been redrawn for Volume 3 since the data pull
on 2019-11-13. If multi-column sections have been annotated in Volume 1 or 2,
the code will have to be updated.

The script will also assign pids and metadata for the "first_letter" column
needed to make the wax collections. Please have available the two files
in which problematic entries are contained for the alphabetical section and the
index.

Note that you must first manually delete any extraneous entries from the data
export (for example, tests or entries from sections that haven't been
reviewed.) This code will not delete bad or 'problem' entries. The code will
alert you of any entries that don't fit the expected schema.


This script will automatically add IIIF urls for the Beehive for thumbnails for
the data from the data export.

For the index, thumbnails are small versions of the annotation. For the
alphabetical section, thumbnails of the annotation are visually unsatisfying.
The script will then select the upper left-hand corner of each annotation,
assuming that the word falls somewhere in this range. The values may need
to be updated if the code produces too many unsatisfactory images.

The script also adds "label" metadata necessary for the Wax galleries.

Finally, this script will create links for entries in the Beehive data export
to their corresponding page generated from the Table of Contents CSV.
You need a copy of the master table fo contents CSV.
"""

import re
import pandas as pd
import csv
from beehive import find_numbers
import os

# get x value from IIIF URL
# takes value of right edge to avoid sorting errors that result when only using
# the x value


def find_x_value(item):
    loc = re.compile(r'/\d+')
    loc_info = loc.search(item).group()
    end_value = re.compile(r',\d+,\d+/')
    to_strip = re.compile(r',\d+/')
    end_match = end_value.search(item).group()
    end_strip = to_strip.search(item).group()
    loc_info = int(loc_info.strip('/'))
    end_match = int(end_match.replace(end_strip, '').strip(','))
    total = loc_info + end_match
    return(total)

# get y value from IIIF URL


def find_y_value(item):
    loc = re.compile(r'/\d+,\d+,\d+,\d+/')
    loc_info = loc.search(item).group()
    front_value = re.compile(r'/\d+,')
    back_value = re.compile(r',\d+,\d+/')
    to_strip = front_value.search(loc_info).group()
    also_strip = back_value.search(loc_info).group()
    loc_info = loc_info.replace(to_strip, '')
    loc_info = loc_info.replace(also_strip, '')
    return(loc_info)


def get_pids(data):
    reader = csv.DictReader(data)
    pages = {}
    for row in reader:
        vol = row['volume']
        img = str(row['image']).zfill(3)
        loc = f'{vol}.{img}'
        pages.update({loc: row['pid']})
    return pages


with open('data/beehive-data-raw.csv', 'r') as f:
    df = pd.read_csv(f)
    df.fillna('', inplace=True)
    df['sort_value'] = ''  # make new empty column for sorting

# handle insertions

insertion_xref = re.compile(r'\[:\d+\.\]')
tag = re.compile(r'#item-\w+')
df['insertion'] = ''

print('Parsing insertions...')

for row in df.index:
    if 'Insertion Xref' in df.loc[row, 'unparsed']:
        unparsed = df.loc[row, 'unparsed']
        insert = insertion_xref.search(unparsed).group()
        item_tag = tag.search(unparsed).group()
        df.loc[row, 'head'] = insert
        df.loc[row, 'item'] = item_tag
    elif 'Insertion' in df.loc[row, 'unparsed']:
        unparsed = df.loc[row, 'unparsed']
        insert = insertion_xref.search(unparsed).group()
        df.loc[row, 'insertion'] = insert

# to sort, we concatenate the volume number, image number, x value and y value
# into one string that we can then sort. Since the x values for volume 3
# will fall between a range, we need to sort them into columns based on this
# x value.

print('Sorting data...')

for row in df.index:
    url = df.loc[row, 'selection']
    new_x_value = find_x_value(url)
    new_y_value = find_y_value(url)
    vol = df.loc[row, 'volume']
    vol = vol.strip('Volume ')
    img = df.loc[row, 'image_number']
    if vol != '3':  # for volumes 1 and 2, assign dummy value "1"
        column = '1'
    # sole entry that can't be sorted automatically
    elif df.loc[row, 'head'] == 'Quakers':
        column = '1'
    elif img % 2 == 0:  # for versos in Volume 3
        if int(new_x_value) < 1400:
            column = '1'
        elif 1400 <= int(new_x_value) < 2010:
            column = '2'
        else:
            column = '3'
    else:  # for rectos in volume 3
        if int(new_x_value) < 1000:
            column = '1'
        elif 1000 <= int(new_x_value) < 1800:
            column = '2'
        else:
            column = '3'
    sort_value = vol + str(img).zfill(3) + column + new_y_value.zfill(4)
    df.loc[row, 'sort_value'] = sort_value

df = df.sort_values(by=['sort_value'])
df = df.drop(['sort_value'], axis=1)
df = df.reset_index(drop=True)

# Write sorted data to csv so we have a clean version of the data to upload
# to the project Github
# new_csv = df.to_csv('beehive-data-sorted.csv', index=False)

# now we assign necessary wax metadata, starting with pids

print('Assigning pids...')

df.insert(0, 'pid', '')
n = 1
for row in df.index:
    if df.loc[row, 'head'] == '':
        entry = df.loc[row, 'entry']
        if find_numbers(entry) is False:
            pid = 'alpha_' + str(n).zfill(4)
            df.loc[row, 'pid'] = pid
            n = n + 1
n = 1
for row in df.index:
    if df.loc[row, 'head'] == '':
        entry = df.loc[row, 'entry']
        if find_numbers(entry) is True:
            pid = 'num_' + str(n).zfill(4)
            df.loc[row, 'pid'] = pid
            n = n + 1

n = 1
for row in df.index:
    if df.loc[row, 'head'] != '':
        pid = 'index_' + str(n).zfill(4)
        df.loc[row, 'pid'] = pid
        n = n + 1

# now we assign the row first_letter. Since Pastorius's alphabetization is
# idiosyncratic, we use a separate file to determine first if any items
# don't start with the expected letter (i.e. 'to bring' instead of 'bring').
# You'll need the corresponding files for both the alphabetical section and the
# index.

# First letter metadata for numerical entries sorts the numbers within a range.

print('Creating additional metadata...')

df.insert(6, 'first_letter', '')
alpha_problems = {}
with open('data/beehive-alpha-sorts.csv', 'r') as file:
    alpha_reader = csv.DictReader(file)
    for row in alpha_reader:
        alpha_problems.update({row['topic']: row['first_letter']})

index_problems = {}
with open('data/beehive-index-sorts.csv', 'r') as File:
    index_reader = csv.DictReader(File)
    for row in index_reader:
        index_problems.update({row['head']: row['first_letter']})

num_ranges = [range(n * 25 + 1, n * 25 + 26) for n in range(0, 198)]

with open('issues_sort-metadata.txt', 'w') as issues:

    for row in df.index:
        if df.loc[row, 'pid'].startswith('alpha'):
            entry = str(df.loc[row, 'entry'])
            topic = str(df.loc[row, 'topic'])
            if topic in alpha_problems:
                letter = alpha_problems[topic]
                df.loc[row, 'first_letter'] = letter
            else:
                try:
                    letter = topic[0].upper()
                    # Pastorius doesn't distinguish between I and J or U and V,
                    # following early-modern conventions, so we need to catch these
                    if letter == 'I':
                        df.loc[row, 'first_letter'] = 'I/J'
                    elif letter == 'J':
                        df.loc[row, 'first_letter'] = 'I/J'
                    elif letter == 'U':
                        df.loc[row, 'first_letter'] = 'U/V'
                    elif letter == 'V':
                        df.loc[row, 'first_letter'] = 'U/V'
                    else:
                        df.loc[row, 'first_letter'] = letter
                except IndexError:
                    issues.writelines(f"Data for {df.loc[row,'pid']} needs clean-up.")
                    print(f"Data for {df.loc[row,'pid']} needs clean-up.")
        elif df.loc[row, 'pid'].startswith('index'):
            head = str(df.loc[row, 'head'])
            img_num = str(df.loc[row, 'image_number'])
            test = img_num + head
            # insertions are categorized separately
            if df.loc[row, 'image_number'] == 54:
                df.loc[row, 'first_letter'] = 'insertion'
            # some entries appear twice in the index, so we have to check by
            # both image number and head
            elif test in index_problems:
                letter = index_problems[test]
                df.loc[row, 'first_letter'] = letter
            else:
                try:
                    letter = head[0].upper()
                    if letter == 'I':
                        df.loc[row, 'first_letter'] = 'I/J'
                    elif letter == 'J':
                        df.loc[row, 'first_letter'] = 'I/J'
                    elif letter == 'U':
                        df.loc[row, 'first_letter'] = 'U/V'
                    elif letter == 'V':
                        df.loc[row, 'first_letter'] = 'U/V'
                    else:
                        df.loc[row, 'first_letter'] = letter
                except IndexError:
                    issues.writelines(f"Data for {df.loc[row,'pid']} needs clean-up.")
                    print(f"Data for {df.loc[row,'pid']} needs clean-up.")
        # numerical entries list the range they fall within as "first letter"
        elif df.loc[row, 'pid'].startswith('num'):
            entry = int(df.loc[row, 'entry'])
            for i in num_ranges:
                if entry in i:
                    letter = str(i[0]) + '-' + str(i[24])
                    df.loc[row, 'first_letter'] = letter

issues.close()

# line = pd.DataFrame(
# {'volume': 'Volume 0', 'image_number': 0, 'unparsed': 'Force UTF-8: büngt'},
# index=[-1])
# df = df.append(line, ignore_index=False, sort=False)
df = df.sort_index().reset_index(drop=True)
df['thumbnail'] = ''  # create empty thumbnail column for next part of the code

new_csv = df.to_csv('data/beehive-data-temp.csv', index=False)

selec = re.compile(r',\d+,\d+/full')


print('Creating thumbnails...')

with open(
        'data/beehive-data-temp.csv', 'r') as csvfile, open(
                'data/beehive-data.csv', 'w') as newfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    fields = reader.fieldnames
    writer = csv.DictWriter(newfile, delimiter=',', fieldnames=fields)
    writer.writeheader()
    for row in reader:
        annotation = row['selection']
        if row['volume'] == 'Volume 3':
            annotation = annotation.replace('full', '150,')
            row['thumbnail'] = annotation
            writer.writerow(row)
        else:
            old = selec.search(annotation).group()
            annotation = annotation.replace(old, ',600,180/250,')
            row['thumbnail'] = annotation
            writer.writerow(row)

print('Writing labels...')
with open('data/beehive-data.csv', 'r') as f:
    df = pd.read_csv(f)
    df.fillna('', inplace=True)
    df['label'] = ''
for row in df.index:
    pid = str(df.loc[row, 'pid'])
    entry = str(df.loc[row, 'entry'])
    if pid.startswith('alpha'):
        df.loc[row, 'label'] = entry
    elif pid.startswith('num'):
        topic = str(df.loc[row, 'topic'])
        df.loc[row, 'label'] = f'{entry}. {topic}'
    elif pid.startswith('index'):
        head = str(df.loc[row, 'head'])
        df.loc[row, 'label'] = head

# create links to wax pages for toc

print('Creating links to ToC pages...')

with open('data/master_toc.csv', 'r') as f:
    toc = get_pids(f)

df['location'] = ''

with open('issues_sort-toc.txt', 'w') as issues:
    for row in df.index:
        volume = str(df.loc[row, 'volume'])
        volume = volume.strip('Volume ')
        image = str(df.loc[row, 'image_number']).zfill(3)
        loc = f'{volume}.{image}'
        try:
            pid = toc[loc]
            pid_link = f"<a href='/digital-beehive/toc/{pid}/'>Full Page</a>"
            df.loc[row, 'location'] = pid_link
        except:
            issues.writelines(f"Data for {df.loc[row,'pid']} needs clean-up.")
            print(f"Data bad for {df.loc[row,'pid']}.")

issues.close()

# line = pd.DataFrame(
# {'volume': 'Volume 0', 'image_number': 0, 'unparsed': 'Force UTF-8: büngt'},
# index=[-1])
# df = df.append(line, ignore_index=False, sort=False)
# df = df.sort_index().reset_index(drop=True)
new_csv = df.to_csv('data/beehive-data-for-wax.csv', index=False)
print('Done.')

os.remove('data/beehive-data-temp.csv')
os.remove('data/beehive-data.csv')
