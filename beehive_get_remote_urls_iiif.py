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
with open('toc_for_website_vol1.csv', 'r') as csvfile, open('toc_vol1.csv', 'w') as newfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    fields = reader.fieldnames
    writer = csv.DictWriter(newfile, delimiter=',', fieldnames=fields)
    writer.writeheader()
    new_csv = collections.OrderedDict()
    for row in reader:  # because of Openn's continuous pagination, we have to 
                        # distinguish between vols one and two       
            page_number = row['image']
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
            

# rinse, wash, repeat with volume 2            
with open('toc_for_website_vol2.csv', 'r') as csv_2, open('toc_vol2.csv', 'w') as newfile_2:
    reader = csv.DictReader(csv_2, delimiter=',')
    fields = reader.fieldnames
    writer = csv.DictWriter(newfile_2, delimiter=',', fieldnames=fields)
    writer.writeheader()
    new_csv_2 = collections.OrderedDict()
    for row in reader:
            page_number_2 = row['image']
            p_number_2 = int(page_number_2) + 467
            str_number_2 = str(p_number_2).zfill(3)
            thumbnail_2 = 'https://stacks.stanford.edu/image/iiif/fm855tg5659%2F1607_0' + str_number_2 + '/full/100,/0/default.jpg'
            full_2 = 'https://stacks.stanford.edu/image/iiif/fm855tg5659%2F1607_0' + str_number_2 + '/full/full/0/default.jpg'
            new_csv_2.update(row)
            new_csv_2['thumbnail'] = thumbnail_2
            new_csv_2['full'] = full_2
            print(f'Updating {row["pid"]}...')
            writer.writerow(new_csv_2)

with open('toc_for_website_index.csv', 'r') as csv_3, open('toc_index.csv', 'w') as newfile_3:
    reader = csv.DictReader(csv_3, delimiter=',')
    fields = reader.fieldnames
    writer = csv.DictWriter(newfile_3, delimiter=',', fieldnames=fields)
    writer.writeheader()
    new_csv_3 = collections.OrderedDict()
    for row in reader:
            page_number_3 = row['image_number']
            p_number_3 = int(page_number_3) + 943
            str_number_3 = str(p_number_3).zfill(4) # need four digits
            thumbnail_3 = 'https://stacks.stanford.edu/image/iiif/gw497tq8651%2F1607_' + str_number_3 +'/full/100,/0/default.jpg'
            full_3 = 'https://stacks.stanford.edu/image/iiif/gw497tq8651%2F1607_' + str_number_3 +'/full/full/0/default.jpg'
            new_csv_3.update(row)
            new_csv_3['thumbnail'] = thumbnail_3
            new_csv_3['full'] = full_3
            print(f'Updating {row["pid"]}...')
            writer.writerow(new_csv_3)
print('Done.')