# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

import numpy as np

def readInput(filename, padx=20, makeBottom=False):
    with open(filename, 'r') as f:
        lines = [l.strip().split() for l in f.readlines()]
    
    paths = []
    for l in lines:
        paths.append([list(map(int, coord.split(','))) for coord in l[::2]])
        
    minx = min(c[0] for p in paths for c in p)
    maxx = max(c[0] for p in paths for c in p)
    maxy = max(c[1] for p in paths for c in p)
    
    pady = 2
    grid = np.zeros((maxx-minx+padx, maxy+pady+1), dtype=int)
    
    for path in paths:
        for i in range(len(path)-1):
            p1, p2 = path[i], path[i+1]
            # print(p1, p2)
            if p1[0] == p2[0]: # vertical line
                fromy, toy = min((p1[1], p2[1])), max((p1[1], p2[1]))
                grid[p1[0]-minx+padx//2, fromy:toy+1] = 1
            if p1[1] == p2[1]: # horizontal line
                fromx, tox = min((p1[0], p2[0])), max((p1[0], p2[0]))
                grid[fromx-minx+padx//2:tox-minx+padx//2+1, p1[1]] = 1

    sandsource = [500-minx+padx//2, 0] # adapted coordinates for source
    
    if makeBottom:
        grid[:,-1] = 1  # bottom for part 2
    
    return grid, sandsource

def printgrid(grid):
    for rowidx in range(grid.shape[1]):
        line = grid[:,rowidx]
        for l in line:
            if l == 0:
                c = '.'
            elif l == 1:
                c = '#'
            elif l == 2:
                c = 'o'
            print(c, end='')
        print()

def sandstep(grid, source):
    x, y = source
    moved = True
    while moved:
        moved = False
        if y < grid.shape[1]-1:
            if grid[x, y+1] == 0:
                y += 1
                moved = True
            elif grid[x-1, y+1] == 0:
                x -= 1
                y += 1
                moved = True
            elif grid[x+1, y+1] == 0:
                x += 1
                y += 1
                moved = True
    if x in range(0, grid.shape[0]) and y < grid.shape[1]-1:
        grid[x,y] = 2

def fillgrid(grid, sandsource, showgrid=False):
    if showgrid:
        print("initial:")
        printgrid(grid)   
        
    nsandold, nsand = -1, 0
    while nsand > nsandold:
        sandstep(grid, sandsource) 
        # print(nsand)
        # printgrid(grid)
        nsandold = nsand
        nsand = len(np.where(grid==2)[0])
    
    if showgrid:
        print("End of filling:")
        printgrid(grid)
    
    return nsand
    
def main():
    inputname = "input-day14"
    # inputname = "input-day14-test"
    
    grid, sandsource = readInput(inputname)
    res1 = fillgrid(grid, sandsource, showgrid=False)
    
    print(f"Task 1: Sand steady after {res1} rounds")
     
    grid, sandsource = readInput(inputname, padx=400, makeBottom=True)
    res2 = fillgrid(grid, sandsource, showgrid=False)
    
    if grid[tuple(sandsource)] == 2: # filling completed
        print(f"Task 2: Sand steady after {res2} rounds")
    else: 
        print("Task 2: not full yet; enlarge padx!")
        
        
if __name__ == "__main__":
    main()
    