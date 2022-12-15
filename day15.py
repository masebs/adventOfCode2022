#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

import re

def readInput(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    sensors = []
    for l in lines:
        nrs = [n for n in map(int, re.findall(r'-*\d+', l))]
        sensors.append([tuple(nrs[:2]), tuple(nrs[2:]), distance(nrs[:2], nrs[2:])])
    return sensors
    
def distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def getOccupation(sensors, targetrow, axis=0):
    occupList = []
    subtractBeacons = []
    
    for s in sensors:
        if abs(s[0][1-axis] - targetrow) <= s[2]: # otherwise sensor too far away
            extent = 2 * s[2] - abs(s[0][1-axis] - targetrow) * 2 # number of occupied elems in targetrow
            occupList.append((s[0][axis]-extent//2, s[0][axis]+extent//2))
            subtractBeacons.append(s[1] if s[1][1] == targetrow else 0)
    occupList.sort(key = lambda el: el[0])
    return occupList, subtractBeacons

def uniteTupels(first, second):
    res = None
    if second[0] > first[0] and second[1] <= first[1]: # second is in first
        res = first
    elif second[0] <= first[0] and second[1] > first[1]: # first is in second
        res = second
    elif second[0] <= first[0] and second[1] <= first[1] and second[1] >= first[0]-1: # overlaps on the left
        res = (second[0], first[1])
    elif second[0] > first[0] and second[1] > first[1] and second[0] <= first[1]+1: # overlaps on the right
        res = (first[0], second[1])
    return res

def uniteList(occupList):
    united = []
    united.append(occupList[0])
    for i in range(1, len(occupList)):
        for j in range(len(united)):
            first = united[j]
            second = occupList[i]
            res = uniteTupels(first, second)
            if res:
                united[j] = res
        if res == None:
            united.append(second)
    return united

def uniteListFull(occupList):
    united = sorted(uniteList(occupList), key = lambda x: x[0])
    while len(united) != len(occupList):
        occupList = united 
        united = sorted(uniteList(occupList), key = lambda x: x[0])
    return united

def countOccupied(united, uniqueBeacons):
    count = 0
    for r in united: 
        count += r[1] - r[0] + 1
    count -= len(uniqueBeacons)
    return count

sensors = readInput("input-day15"); targetrow = 2000000; xmax = ymax = 4000000
# sensors = readInput("input-day15-test"); targetrow = 10; xmax = ymax = 20

occupList, subtractBeacons = getOccupation(sensors, targetrow)
united = uniteListFull(occupList)    
uniqueBeacons = set(b for b in subtractBeacons if type(b) == tuple)
count = countOccupied(united, uniqueBeacons)

print(f"\nTask 1: {count} cols cannot contain beacon\n")

# Task 2: The naive way, going through all relevant rows and columns (until we found a gap)
xcoord, ycoord = -1, -1

for i in range(ymax-1,-1,-1):
    occupList, subtractBeacons = getOccupation(sensors, i)
    united = uniteListFull(occupList)
    united = [(max((0, u[0])), min((u[1], ymax))) for u in united] # limit interval to bounds
    if len(united) > 1:
        print(united)
        assert(united[0][1]+2 == united[1][0]) # check if it is actually a gap of 1
        xcoord = united[0][1]+1
        break
    if i%100000 == 0:
        print(i)

for i in range(xmax-1,-1,-1):
    occupList, subtractBeacons = getOccupation(sensors, i, axis=1)
    united = uniteListFull(occupList)
    united = [(max((0, u[0])), min((u[1], xmax))) for u in united] # limit interval to bounds
    if len(united) > 1:
        print(united)
        assert(united[0][1]+2 == united[1][0]) # check if it is actually a gap of 1
        ycoord = united[0][1]+1
        break
    if i%100000 == 0:
        print(i)

print(f"\nTask 2: Distress beacon must be at ({xcoord},{ycoord}), result = {4000000*xcoord + ycoord}\n")


