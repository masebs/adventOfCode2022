# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

import re

with open("input-day15", 'r') as f:
    lines = f.readlines() #[l.strip().split() for l in f.readlines()]
targetrow = 2000000
# with open("input-day15-test", 'r') as f:
#     lines = f.readlines() #[l.strip().split() for l in f.readlines()]
# targetrow = 11

def distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

sensors = []
for l in lines:
    nrs = [n for n in map(int, re.findall(r'\d+', l))]
    sensors.append([tuple(nrs[:2]), tuple(nrs[2:]), distance(nrs[:2], nrs[2:])])

occupList = []
subtractBeacons = []

for s in sensors:
    if abs(s[0][1] - targetrow) <= s[2]: # otherwise sensor too far away
        extent = 2 * s[2] - abs(s[0][1] - targetrow) * 2 # number of occupied elems in targetrow
        occupList.append((s[0][0]-extent//2, s[0][0]+extent//2))
        subtractBeacons.append(s[1] if s[1][1] == targetrow else 0)
        print(extent, occupList[-1], subtractBeacons[-1])

def uniteTupels(first, second):
    res = None
    if second[0] > first[0] and second[1] <= first[1]: # second is in first
        res = first
        print("  case 1", res) 
    elif second[0] <= first[0] and second[1] > first[1]: # first is in second
        res = second
        print("  case 2", res) 
    elif second[0] <= first[0] and second[1] <= first[1] and second[1] >= first[0]-1: # overlaps on the left
        res = (second[0], first[1])
        print("  case 3", res) 
    elif second[0] > first[0] and second[1] > first[1] and second[0] <= first[1]+1: # overlaps on the right
        res = (first[0], second[1])
        print("  case 4", res)
    return res

def uniteList(occupList):
    united = []
    united.append(occupList[0])
    print("Before start: united:", united)
    for i in range(1, len(occupList)):
        for j in range(len(united)):
            first = united[j]
            second = occupList[i]
            print("using first =", first)
            print("using second =", second)
            res = uniteTupels(first, second)
            if res:
                united[j] = res
        if res == None:
            print("APPENDING")
            united.append(second)
    print("  united:", united)
    return united

print(occupList)
united = sorted(uniteList(occupList), key = lambda x: x[0])
while len(united) != len(occupList):
    occupList = united 
    united = sorted(uniteList(occupList), key = lambda x: x[0])
    
uniqueBeacons = set(b for b in subtractBeacons if type(b) == tuple)

count = 0
for r in united: 
    count += r[1] - r[0] + 1
count -= len(uniqueBeacons)

print()
print(f"Task 1: {count} cols cannot contain beacon.")
