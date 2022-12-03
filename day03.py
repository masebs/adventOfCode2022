# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

lines = []
with open("input-day03", 'r') as f:
# with open("input-day03-test", 'r') as f:
    lines = f.readlines()

def getPrio(item):
    p = ord(item) - ord('a') + 1
    if p <= 0:
        p = ord(item) - ord('A') + 1 + 26
    return p

prioT1 = 0
prioT2 = 0

for lnr in range(0, len(lines), 3):
    elfsets = []
    for elfnr in range(3):
        l = lines[lnr+elfnr]
        l = l.strip()
        items1 = set(l[:len(l)//2])
        items2 = set(l[len(l)//2:])
        # Part 1: find double item in each elf's rucksack
        (doubleItem,) = set.intersection(items1, items2)
        prioT1 += getPrio(doubleItem)
        # print(doubleItem)
        elfsets.append(set.union(items1, items2))
        
    # Part 2: for the set of 3 elves, find their common item (= badge)
    (badge,) = set.intersection(elfsets[0], elfsets[1], elfsets[2])
    # print(badge)
    prioT2 += getPrio(badge)
    
print(f"Task 1: Priority sum for double items is {prioT1}")
print(f"Task 2: Priority sum for badges is {prioT2}")
