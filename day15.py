# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

import re

# with open("input-day15", 'r') as f:
#     lines = f.readlines() #[l.strip().split() for l in f.readlines()]
# targetrow = 2000000
with open("input-day15-test", 'r') as f:
    lines = f.readlines() #[l.strip().split() for l in f.readlines()]
targetrow = 10

def distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

sensors = []
for l in lines:
    nrs = [n for n in map(int, re.findall(r'\d+', l))]
    sensors.append([tuple(nrs[:2]), tuple(nrs[2:]), distance(nrs[:2], nrs[2:])])
    

occupList = []
subtractBeacons = []

for s in sensors:
    # print()
    # print(s)
    if abs(s[0][1] - targetrow) <= s[2]: # otherwise sensor too far away
        extent = 2 * s[2] - abs(s[0][1] - targetrow) * 2 # number of occupied elems in targetrow
        occupList.append((s[0][0]-extent//2, s[0][0]+extent//2))
        subtractBeacons.append(s[1] if s[1][1] == targetrow else 0)
        # print(extent, occupList[-1], subtractBeacons[-1])

# count = 0
# processedRanges = []
# for o, b in zip(occupList, subtractBeacons):
#     correct = 0
#     for pr, pb in processedRanges:
#         if o[0] <= pr[0] <= o[1] and o[0] <= pr[1] <= o[1]: # previous range is within current range
#             correct -= pr[1] - pr[0] + 1
#         elif o[0] <= pr[0] <= o[1]: # left part of a previous range is within current
#             correct -= o[1] - pr[0] + 1
#         elif o[0] <= pr[1] <= o[1]: # right part of a previous range is within current
#             correct -= pr[1] - o[0] + 1
#         #     if type(b) == tuple and o[0] <= b[0] <= pr[1]:
#         #         b = 0
#         #     o = (pr[1]+1, o[1])
#         # if pr[0] <= o[1] <= pr[1]: # upper end of current range overlaps with a previous range
#         #     if type(b) == tuple and pr[0] <= b[0] <= o[1]:
#         #         b = 0
#         #     o = (o[0], pr[0]-1)  
#     processedRanges.append([o, b])
#     # count += o[1] - o[0] + 1 - (1 if type(b) == tuple else 0)
#     count += o[1] - o[0] + 1 + correct

occupListAndBeacons = [[o, b] for o, b in zip(occupList, subtractBeacons)]
occupListAndBeacons.sort(key = lambda el: el[0][1]-el[0][0], reverse=True)
print(occupListAndBeacons)
print()

# # count = 0
# uniqueRanges = []
# uniqueBeacons = []
# for o, b in occupListAndBeacons:
#     for pr in uniqueRanges:
#         if pr[0] <= o[0] <= pr[1]: # lower end of current range overlaps with a previous range
#             print(f"cur: {o}, conflict lower with {pr}, corrected: ", end="")
#             o = (pr[1]+1, o[1]) # correct lower bound
#             print(f"{o}")
#         if pr[0] <= o[1] <= pr[1]: # upper end of current range overlaps with a previous range
#             print(f"cur: {o}, conflict upper with {pr}, corrected: ", end="")
#             o = (o[0], pr[0]-1) # correct upper bound
#             print(f"{o}")
#     if o[0] <= o[1]: 
#         uniqueRanges.append(o) 
#     if type(b) == tuple and b not in uniqueBeacons: 
#         uniqueBeacons.append(b)
#     # count += o[1] - o[0] + 1 - (1 if type(b) == tuple else 0)

# uniqueRanges.sort(key = lambda el: el[0])
# print()
# print(uniqueRanges)

# unite all ranges
oldlist = occupList.copy()
united = []
oldlist.sort(key = lambda el: el[0], reverse=False)
print(oldlist)
while len(united) != len(oldlist) and len(oldlist) > 1:
    if united: # not in the first round
        oldlist = united
        united = [] 
    
    for i in range(0, len(oldlist)-1, 2):
        print("  ", oldlist[i], oldlist[i+1], "->", end="")
        if oldlist[i+1][0] > oldlist[i][1] and oldlist[i+1][1] <= oldlist[i][1]: # i+1 is within i
            print("  case 1") 
            united.append(oldlist[i])
        elif oldlist[i+1][0] <= oldlist[i][1] and oldlist[i+1][1] <= oldlist[i][1]:
            print("  case 2")
            united.append((oldlist[i][0], oldlist[i][1]))
        elif oldlist[i+1][0] <= oldlist[i][1] and oldlist[i+1][1] > oldlist[i][1]: 
            print("  case 3")
            united.append((oldlist[i][0], oldlist[i+1][1]))
        # elif oldlist[i+1][0] > oldlist[i][1] and oldlist[i+1][1] > oldlist[i][1]:
        #     print("  case 4")
        #     united.append((oldlist[i][0], oldlist[i][1]))
        else: # no overlap, so add both
            print("  case else")
            united.append(oldlist[i])
            united.append(oldlist[i+1])
        print("  ", united[-1])
    united.sort(key = lambda el: el[0])
    print(oldlist)
    print(united)
    print()

united = oldlist
uniqueBeacons = set(b for b in subtractBeacons if type(b) == tuple)

count = 0
for r in united: 
    count += r[1] - r[0] + 1
count -= len(uniqueBeacons)

print()
print(f"Task 1: {count} cols cannot contain beacon.")