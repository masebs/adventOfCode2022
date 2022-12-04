# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

# start time: 6:11, finish: 6:33

lines = []
with open("input-day04", 'r') as f:
# with open("input-day04-test", 'r') as f:
    lines = f.readlines()

subsetcount = 0
overlapcount = 0

for l in lines:
    l = l.strip().split(',')
    (lower0, upper0) = map(int, l[0].split('-'))
    (lower1, upper1) = map(int, l[1].split('-'))
    s1 = set(range(lower0, upper0+1))
    s2 = set(range(lower1, upper1+1))
    
    if s1.issubset(s2) or s2.issubset(s1):
        subsetcount += 1
    if s1.intersection(s2):
        overlapcount += 1
        
    
print(f"Task 1: There are {subsetcount} sections included in others.")
print(f"Task 2: There are {overlapcount} overlapping sections.")

