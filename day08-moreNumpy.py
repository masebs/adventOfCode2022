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

visible = np.zeros_like(grid, dtype=bool)
visible[0,:]   = 1 # all edges are visible
visible[X-1,:] = 1
visible[:,0]   = 1
visible[:,Y-1] = 1

for _ in range(4): # rotate four times and search along X axis for each rotation
    for i in range(1, X-1): # looking from the left and right
        tallest = grid[i,0]
        for j in range(1, Y-1):
            if grid[i,j] > tallest:
                visible[i,j] = 1
            tallest = max((tallest, grid[i,j]))
    grid    = np.rot90(grid) 
    visible = np.rot90(visible) 

visCount = np.count_nonzero(visible)

print(f"Task 1: Number of visible trees is {visCount}")

scenicScore = np.ones_like(grid)

for _ in range(4):
    for i in range(X):
        for j in range(Y):
            score = 0
            for k in range(j+1, Y): # walk right
                if grid[i,k] < grid[i,j]:
                    score += 1
                else:
                    score += 1 # count last equally tall tree
                    break
            scenicScore[i,j] *= score
    grid        = np.rot90(grid)
    scenicScore = np.rot90(scenicScore)

maxscore = np.max(scenicScore)

print(f"Task 2: Maximum scenic score is {maxscore}")