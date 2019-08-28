#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:59:27 2019

@author: davidnelson

This script will automatically add IIIF urls for the Beehive for thumbnails for
the data from the data export.
"""

import csv
import collections

# 'alpha_old.csv' is the path to the source file
# 'alpha.csv' is the new file you write to
with open('beehive-data-old.csv', 'r') as csvfile, open('beehive-data.csv', 'w') as newfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    fields = reader.fieldnames
    writer = csv.DictWriter(newfile, delimiter=',', fieldnames=fields)
    writer.writeheader()
    new_csv = collections.OrderedDict()
    for row in reader:  # because of Openn's continuous pagination, we have to 
                        # distinguish between vols one and two       
        if row['volume'] == 'Volume 1': 
            page_number = row['image_number']
            p_number = int(page_number) - 1
            str_number = str(p_number)
            # switch out thumbnail for whatever header appears in your csv
            # if you need full images, instead of thumbnails, replace "thumb" 
            # with "web" in the following line
            thumbnail = 'https://stacks.stanford.edu/image/iiif/ps974xt6740%2F1607_0' + str_number + '/full/100,/0/default.jpg'
            new_csv.update(row)
            new_csv['thumbnail'] = thumbnail # update 'thumbnail' to match header in your csv
            print(f'Updating {row["pid"]}...')
            writer.writerow(new_csv)
        elif row['volume'] == 'Volume 2': #rinse, wash, repeat with vol 2.
            page_number_2 = row['image_number']
            p_number_2 = int(page_number_2) + 467
            str_number_2 = str(p_number_2)
            thumbnail_2 = 'https://stacks.stanford.edu/image/iiif/ps974xt6740%2F1607_0' + str_number + '/full/100,/0/default.jpg'
            new_csv.update(row)
            new_csv['thumbnail'] = thumbnail_2
            print(f'Updating {row["pid"]}...')
            writer.writerow(new_csv)
        else:
            page_number_3 = row['image_number']
            p_number_3 = int(page_number_3) + 943
            str_number_3 = str(p_number_3).zfill(4)
            thumbnail_3 = 'https://stacks.stanford.edu/image/iiif/gw497tq8651%2F1607_' + str_number_3 +'/full/100,/0/default.jpg'
            new_csv.update(row)
            new_csv['thumbnail'] = thumbnail_3
            print(f'Updating {row["pid"]}...')
            writer.writerow(new_csv)
print('Done.')