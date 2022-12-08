# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

import numpy as np 

with open("input-day08", 'r') as f:
# with open("input-day08-test", 'r') as f:
    lines = [l.strip() for l in f.readlines()]

grid = np.zeros((len(lines[0]), len(lines)), dtype=int)

for i,l in enumerate(lines):
    for j,c in enumerate(l):
        grid[i,j] = c

X, Y = grid.shape
visible = 2*(X-1) + 2*(Y-1)
visibleList = set() # to ensure we only count each tree once

for i in range(1, X-1): # looking from the left and right
    fromleft   = grid[i,0]
    fromright  = grid[i,Y-1]
    leftcount  = 0
    rightcount = 0
    for j in range(1, Y-1):
        if grid[i,j] > fromleft and not (i,j) in visibleList:
            leftcount += 1
            visibleList.add((i,j))
        fromleft = max((fromleft, grid[i,j]))
    for j in range(Y-2, 0, -1):
        if grid[i,j] > fromright and not (i,j) in visibleList:
            rightcount += 1
            visibleList.add((i,j))
        fromright = max((fromright, grid[i,j]))
    # print(f"line {i}: new from left: {leftcount}, new from right: {rightcount}")
    visible += leftcount + rightcount

for j in range(1, Y-1): # looking from the top and bottom
    fromtop     = grid[0,j]
    frombottom  = grid[X-1,j]
    topcount    = 0
    bottomcount = 0
    for i in range(1, X-1):
        if grid[i,j] > fromtop and not (i,j) in visibleList:
            topcount += 1
            visibleList.add((i,j))
        fromtop = max((fromtop, grid[i,j]))
    for i in range(X-2, 0, -1):
        if grid[i,j] > frombottom and not (i,j) in visibleList:
            bottomcount += 1
            visibleList.add((i,j))
        frombottom = max((frombottom, grid[i,j]))
    # print(f"column {j}: from top: {topcount}, from bottom: {bottomcount}")
    visible += topcount + bottomcount      
      
print(f"Task 1: Number of visible trees is {visible}")

maxscore = 0

for i in range(X):
    for j in range(Y):
        right, left, down, up = 0, 0, 0, 0
        for k in range(i+1, X): # walk down
            if grid[k,j] < grid[i,j]:
                down += 1
            else:
                down += 1 # last visible tree is taller or equally tall one
                break
        for k in range(i-1, -1, -1): # walk up
            if grid[k,j] < grid[i,j]:
                up += 1
            else:
                up += 1
                break
        for k in range(j+1, Y): # walk right
            if grid[i,k] < grid[i,j]:
                right += 1
            else:
                right += 1
                break
        for k in range(j-1, -1, -1): # walk left
            if grid[i,k] < grid[i,j]:
                left += 1
            else:
                left += 1
                break
        scenicScore = up * left * down * right
        # print(f"({i},{j}): {up}, {left}, {down}, {right}")
        maxscore = max((maxscore, scenicScore))
        
print(f"Task 2: Maximum scenic score is {maxscore}")