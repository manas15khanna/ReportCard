import csv
import re
import sys

# Some fixed rules for the CSV:
# Must have a Name column, Father's name column, a Date of birth column,
# and the rest of the columns would be subjects and marks.
path = input("Enter the path to the CSV file: ")

with open(path, "r") as f:
    marks = f.readlines()

# Marking all the headers
headers = marks[0].split(',')

# we initialize the data dictionary to hold the necessary columns.
data = {}
for i in headers:
    data[i] = ""
