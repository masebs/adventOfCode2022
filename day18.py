# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

from functools import lru_cache

def countSides(cubes, task2=False):
    contactCount = 0
    for i in range(len(cubes)):
        for j in range(len(cubes)):
            count = 0
            for idcs in zip(cubes[i], cubes[j]):
                if idcs[0] == idcs[1]:
                    count += 1
            if count == 2:
                idx = [k for k in zip(cubes[i], cubes[j]) if k[0] != k[1]][0]
                if abs(idx[0]-idx[1]) == 1:
                    contactCount += 1
                    # print(idx)
        if task2:
            for nbr in [[-1,0,0], [1,0,0], [0,-1,0], [0,1,0], [0,0,-1], [0,0,1]]:
                idx = (cubes[i][0]+nbr[0], cubes[i][1]+nbr[1], cubes[i][2]+nbr[2])
                if idx not in cubeSet and not floodFillBFS(idx):
                    # print("floodfill not reached:", idx)
                    contactCount += 1
    return contactCount

@lru_cache(maxsize=None)     
def floodFillBFS(cur):
    # print(cur)
    global maxx, maxy, maxz, cubeSet
    if cur in cubeSet:
        return False
    visited = set()
    visited.add(cur)
    q = [cur]
    while q:
        cur = q.pop(0)
        if cur[0] in [-1, maxx+1] or cur[1] in [-1, maxy+1] or cur[2] in [-1, maxz+1]:
            return True # border reached -> success!
        
        for nbr in [[-1,0,0], [1,0,0], [0,-1,0], [0,1,0], [0,0,-1], [0,0,1]]:
            idx = (cur[0]+nbr[0], cur[1]+nbr[1], cur[2]+nbr[2])
            if -1 <= idx[0] <= maxx+1 and -1 <= idx[1] <= maxy+1 and -1 <= idx[2] <= maxz+1:  
                if idx not in visited:
                    if idx not in cubeSet:
                        q.append(idx)
                        visited.add(idx)
    return False # not reachable


with open("input-day18", 'r') as f:
# with open("input-day18-test", 'r') as f:
    cubes = [[int(i) for i in l.strip().split(',')] for l in f.readlines()  ]

cubeSet = set((x,y,z) for (x,y,z) in cubes)

maxx = max(c[0] for c in cubes)
maxy = max(c[1] for c in cubes)
maxz = max(c[2] for c in cubes)
sidesTotal = 6*len(cubes)

contactCount = countSides(cubes)

print(sidesTotal, contactCount)
print(f"Part 1: {sidesTotal-contactCount}")

contactCount = countSides(cubes, task2=True)   

print(sidesTotal, contactCount)
print(f"Part 2: {sidesTotal-contactCount}")

