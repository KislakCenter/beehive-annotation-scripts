#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:59:27 2019

@author: davidnelson

This script will automatically add IIIF urls for the Beehive for thumbnails for
the data from the data export.

For the index, thumbnails are small versions of the annotation. For the 
alphabetical section, thumbnails of the annotation are visually unsatisfying.
The script will then select the upper left-hand corner of each annotation,
assuming that the word falls somewhere in this range. The values may need
to be updated if the code produces too many unsatisfactory images. 
"""

import csv
import re

selec = re.compile(r',\d+,\d+/full')

# 'alpha_old.csv' is the path to the source file
# 'alpha.csv' is the new file you write to
with open('beehive-data-sorted-for-wax.csv', 'r') as csvfile, open('beehive-data.csv', 'w') as newfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    fields = reader.fieldnames
    writer = csv.DictWriter(newfile, delimiter=',', fieldnames=fields)
    writer.writeheader()
    for row in reader:
        if row['volume'] == 'Volume 3':
            annotation = row['selection']
            annotation = annotation.replace('full', '150,')
            row['thumbnail'] = annotation
            writer.writerow(row)
            print(f"Updating {row['pid']}...")
        else: 
            annotation = row['selection']
            old = selec.search(annotation).group()
            annotation = annotation.replace(old, ',600,180/250,')
            row['thumbnail'] = annotation
            writer.writerow(row)
            print(f"Updating {row['pid']}...")
            
        
print('Done.')
