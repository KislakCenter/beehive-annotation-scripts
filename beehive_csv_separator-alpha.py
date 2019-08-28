#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:46:30 2019

@author: davidnelson

This script will divide the large csv file for the alphabetical section
from the data grab into five smaller, more manageable files.

Run the remote urls script first after you've performed the necessary data 
cleanup.
"""

import csv
import collections

# Make sure you are in the correct directory, or change paths as needed.
# This assumes you are in the '_data' directory for your Jekyll site.
# 'alpha.csv' is the csv from the data grab.

with open('alpha-num-linked.csv', 'r') as f:
    reader = csv.DictReader(f)   
    # 'alpha1.csv' is the file that will be created with the first set of entries 


    with open('alpha1.csv', 'w', newline='') as out_file:
        fieldnames = reader.fieldnames # we only get the fieldnames once
        writer= csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if row['first_letter'].startswith(('A', 'B', 'C', 'D')):
                index1 = collections.OrderedDict()
                index1.update(row)
                writer.writerow(index1) # writes rows to csv
                    
        # terrible, inelegant code, but now we just repeat with the next sets
with open('alpha-num-linked.csv', 'r') as f:
    reader = csv.DictReader(f)   
    
    with open('alpha2.csv', 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if row['first_letter'].startswith(('E', 'F', 'G', 'H')):
                index2 = collections.OrderedDict()
                index2.update(row)
                fieldnames = index2.keys() # gets fieldnames from csv
                writer.writerow(index2) # writes rows to csv

with open('alpha-num-linked.csv', 'r') as f:
    reader = csv.DictReader(f)   

    with open('alpha3.csv', 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if row['first_letter'].startswith(('I', 'K', 'L', 'M', 'N')):
                index3 = collections.OrderedDict()
                index3.update(row)
                fieldnames = index3.keys() # gets fieldnames from csv
                writer.writerow(index3) # writes rows to csv

                    
with open('alpha-num-linked.csv', 'r') as f:
    reader = csv.DictReader(f)   

    with open('alpha4.csv', 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if row['first_letter'].startswith(('O', 'P', 'Q', 'R', 'S')):
                index4 = collections.OrderedDict()
                index4.update(row)
                fieldnames = index4.keys() # gets fieldnames from csv
                writer.writerow(index4) # writes rows to csv
                    
with open('alpha-num-linked.csv', 'r') as f:
    reader = csv.DictReader(f)   

    with open('alpha5.csv', 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if row['first_letter'].startswith(('T', 'U', 'W', 'X', 'Y', 'Z', '{')):
                index5 = collections.OrderedDict()
                index5.update(row)
                fieldnames = index5.keys() # gets fieldnames from csv
                writer.writerow(index5) # writes rows to csv

                    
print('Done')
