#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 11:07 2019

@author: davidnelson

This script will automatically add urls for the Beehive for the ToC. Both 
thumbnails and full images are IIIF. Place all three csvs in the same
directory and navigate into it, or modify paths in the script below.
"""

import csv
import collections

# 'toc_for_website.csv' is the path to the source file
# 'toc.csv' is the new file you write to
with open('master_toc_for_website.csv', 'r') as csvfile, open('master_toc.csv', 'w') as newfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    fields = reader.fieldnames
    writer = csv.DictWriter(newfile, delimiter=',', fieldnames=fields)
    writer.writeheader()
    new_csv = collections.OrderedDict()
    for row in reader:
        if row['thumbnail'] == '':
            vol = row['volume']
            page_number = row['image']
            if vol == '1':
                p_number = int(page_number) - 1
                str_number = str(p_number).zfill(3) # need three digits, leading zeros
                # switch out thumbnail for whatever header appears in your csv
                thumbnail = 'https://stacks.stanford.edu/image/iiif/ps974xt6740%2F1607_0' + str_number + '/full/100,/0/default.jpg'
                full = 'https://stacks.stanford.edu/image/iiif/ps974xt6740%2F1607_0' + str_number + '/full/full/0/default.jpg'
                new_csv.update(row)
                new_csv['thumbnail'] = thumbnail
                new_csv['full'] = full # update 'thumbnail' to match header in your csv
                print(f'Updating {row["pid"]}...')
                writer.writerow(new_csv)
            elif vol == '2':
                p_number = int(page_number) + 467
                str_number = str(p_number).zfill(3)
                thumbnail = 'https://stacks.stanford.edu/image/iiif/fm855tg5659%2F1607_0' + str_number + '/full/100,/0/default.jpg'
                full = 'https://stacks.stanford.edu/image/iiif/fm855tg5659%2F1607_0' + str_number + '/full/full/0/default.jpg'
                new_csv.update(row)
                new_csv['thumbnail'] = thumbnail
                new_csv['full'] = full
                print(f'Updating {row["pid"]}...')
                writer.writerow(new_csv)
            else:
                page_number = row['image']
                p_number = int(page_number) + 943
                str_number = str(p_number).zfill(4) # need four digits
                thumbnail = 'https://stacks.stanford.edu/image/iiif/gw497tq8651%2F1607_' + str_number +'/full/100,/0/default.jpg'
                full = 'https://stacks.stanford.edu/image/iiif/gw497tq8651%2F1607_' + str_number +'/full/full/0/default.jpg'
                new_csv.update(row)
                new_csv['thumbnail'] = thumbnail
                new_csv['full'] = full
                print(f'Updating {row["pid"]}...')
                writer.writerow(new_csv)
        else:
            new_csv.update(row)
            writer.writerow(new_csv)

print('Done.')
