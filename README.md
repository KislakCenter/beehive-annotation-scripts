# Beehive Scripts

This repository contains scripts that can be used to parse annotations as part of the [Digital Beehive Project](http://kislakcenter.github.io/digital-beehive). The scripts will parse a CSV of Beehive annotations and create paths to links for the linked entries section of the Digital Beehive Project.

To run the scripts, you will need to install Python3 as well as the pandas module. The experimental network visualization code uses the NetworkX module, but this module is not necessary for building the Jekyll site.

To install Python via Anaconda (which includes both pandas and NetworkX), follow this [Software Carpentry tutorial](http://swcarpentry.github.io/python-novice-gapminder/setup/).

Note if you are using an older MacBook, your computer ships with Python2 installed. This code will not run on Python2, so you will have to install Python3.

Once you have Python3 installed, open a new terminal on the command line. Navigate to a location on your computer in which you would like to store the files, and clone the repo:

```
cd path/to/directory
git clone https://github.com/drnelson6/beehive-scripts.git
```

You will need the latest version of the data from Doug Emery. Delete all extraneous entries (blank, incomplete, experimental, redundant, etc), and copy over the file "beehive-data-raw.csv" with the newer data:

```
cp path/to/data.csv data/beehive-data-raw.csv
```

Run the script to sort the data:

```
python beehive-sort-data-for-wax.py
```

Run the script to parse the annotations. This script will alert you to any data that needs reviewing:

```
python beehive-annotation-parser.py
```

The second script will produce the datasets you need to build the Jekyll site. Copy these (alpha1.csv, alpha2.csv, etc.) into the \_data file of the Jekyll repo and proceed with building the site.

To update the issue tracker, replace the issue tracker files with their latest versions and run the code:

```
cp path/to/file data/alpha-issues.csv
cp path/to/file data/num-issues.csv
cp path/to/file data/index-issues.csv

python problem-tracker.py
```
