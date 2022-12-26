# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

import numpy as np

with open("input-day17", 'r') as f:
# with open("input-day17-test", 'r') as f:
    dirs = [l for l in f.read().strip()]

gridwidth = 7
diridx = 0
grid = np.zeros((20000, gridwidth), dtype=int) # grid[y, x] with y from bottom to top, x from the left to right
grid[0,:] = 1
currentupper = 0

def printgrid(grid):
    for g in grid[::-1]:
        if not all([g[i] == 0 for i in range(len(g))]):
            for c in g:
                print('.' if c == 0 else '#', end='')
            print('\n', end='')
            
def printgridf(grid, f):
    for g in grid[::-1]:
        if not all([g[i] == 0 for i in range(len(g))]):
            for c in g:
                print('.' if c == 0 else '#', end='', file=f)
            print('\n', end='', file=f)

reached2871 = False
reached5544 = False
reached8217 = False

for i in range(10000):
    # print("\nrock nr", i+1)
    pos = [2, 4] # left wall to left end and stuff below to bottom end 
    
    if i % 5 == 0: # horizontal dash
        rockarray = np.array([[1,1,1,1]])
    elif i % 5 == 1: # cross
        rockarray = np.array([[0,1,0],[1,1,1], [0,1,0]])
    elif i % 5 == 2: # inverse L
        rockarray = np.array([[1,1,1],[0,0,1], [0,0,1]]) # upside down because of how it is used
    elif i % 5 == 3: # vertical dash
        rockarray = np.array([[1],[1],[1],[1]])
    elif i % 5 == 4: # square
        rockarray = np.array([[1,1],[1,1]])
    
    # print(pos)
    
    while True:
        blow = dirs[diridx]
        # print(blow, diridx)
        diridx = (diridx+1) % len(dirs)
        if blow == '>':        
            # if none of the elems at the right end collides, change horizontal position
            if not pos[0]+1+len(rockarray[0])-1 >= gridwidth and not any([any(row & grid[currentupper+pos[1]+rnr, pos[0]+1+np.where(row)[0][-1]]) for rnr, row in enumerate(rockarray)]):
                pos[0] += 1
        elif blow == '<':
            if not pos[0]-1 < 0 and not any([any(row & grid[currentupper+pos[1]+rnr, pos[0]-1+np.where(row)[0][0]]) for rnr, row in enumerate(rockarray)]):
                pos[0] -= 1
        # check for vertical collision and stop if there is one
        if                             any([el & grid[currentupper+pos[1]-1, pos[0]+colnr] for colnr, el in enumerate(rockarray[0])])  \
            or (len(rockarray) > 1 and any([el & grid[currentupper+pos[1],   pos[0]+colnr] for colnr, el in enumerate(rockarray[1])])) \
            or (len(rockarray) > 2 and any([el & grid[currentupper+pos[1]+1, pos[0]+colnr] for colnr, el in enumerate(rockarray[2])])):
            # print(pos)
            break
        else:
            pos[1] -= 1
        
        # print(pos)
    
    yvals, xvals = np.where(grid[currentupper+pos[1]:currentupper+pos[1]+len(rockarray), pos[0]:pos[0]+len(rockarray[0])])
    for y, x in zip(yvals, xvals):
        if grid[y, x] and rockarray[y,x]:
            raise ValueError
    
    grid[currentupper+pos[1]:currentupper+pos[1]+len(rockarray), pos[0]:pos[0]+len(rockarray[0])] = rockarray | grid[currentupper+pos[1]:currentupper+pos[1]+len(rockarray), pos[0]:pos[0]+len(rockarray[0])]
    
    currentupper = max(currentupper, currentupper + pos[1] + len(rockarray) - 1)
    # print(currentupper)
    
    # printgrid(grid)
    
    if currentupper == 197:
        print("  Task 2: end of non-periodic section 197 reached in round", i)
        # printgrid(grid[currentupper-5:currentupper+1, :])
    
    if currentupper >= 2871 and not reached2871:
        reached2871 = True
        print("  Task 2: end of 1st period 2871 reached in round", i)
        # printgrid(grid[currentupper-5:currentupper+1, :])
        
    if currentupper >= 5544 and not reached5544:
        reached5544 = True
        print("  Task 2: end of 2nd period 5544 reached in round", i)
        # printgrid(grid[currentupper-5:currentupper+1, :])
        
    if currentupper >= 8217 and not reached8217:
        reached8217 = True
        print("  Task 2: end of 3rd period 8217 reached in round", i)
        # printgrid(grid[currentupper-5:currentupper+1, :])
        
    if i+1 == 2022:
        print()
        print("Task 1:", np.where([not any(grid[i,:]) for i in range(len(grid))])[0][0]-1, currentupper)
        print()

with open('day17-output-check', 'w') as f:
    printgridf(grid[::-1], f)

print("\nCheck currentupper:", currentupper)

# Task 2: Simulate initial + one periodic stack + desired rounds modulo stack height
# This is really messy and requires:
# 1.) Finding the height per period and the onset of the first period manually from a text file (e.g. output for 10k rounds)
# 2.) Using these heights for the hard-coded lookups above (w.r.t. currentupper) to find the number of rounds per period and for the onset
# 3.) Simulating from the beginning to the end of the first cycle, and from the begin of the last incomplete cycle to the end. 
#     Everything in between is calculated from the number of cycles
diridx = 0
grid = np.zeros((10000, gridwidth), dtype=int) # grid[y, x] with y from bottom to top, x from the left to right
grid[0,:] = 1
currentupper = 0

heightPerPeriod = 2673       # found by hand from the textfile written above
roundTilEndOf1stStack = 1871 # found from the hard-coded output above
roundsPerPeriod = 1735       # found from the hard-coded output above

actualRounds = 1000000000000

runTo = roundTilEndOf1stStack + (actualRounds - roundTilEndOf1stStack) % roundsPerPeriod

for i in range(runTo):
    # print("\nrock nr", i+1)
    pos = [2, 4] # left wall to left end and stuff below to bottom end 
    
    if i % 5 == 0: # horizontal dash
        rockarray = np.array([[1,1,1,1]])
    elif i % 5 == 1: # cross
        rockarray = np.array([[0,1,0],[1,1,1], [0,1,0]])
    elif i % 5 == 2: # inverse L
        rockarray = np.array([[1,1,1],[0,0,1], [0,0,1]]) # upside down because of how it is used
    elif i % 5 == 3: # vertical dash
        rockarray = np.array([[1],[1],[1],[1]])
    elif i % 5 == 4: # square
        rockarray = np.array([[1,1],[1,1]])
    
    # print(pos)
    
    while True:
        blow = dirs[diridx]
        # print(blow, diridx)
        diridx = (diridx+1) % len(dirs)
        if blow == '>':        
            # if none of the elems at the right end collides, change horizontal position
            if not pos[0]+1+len(rockarray[0])-1 >= gridwidth and not any([any(row & grid[currentupper+pos[1]+rnr, pos[0]+1+np.where(row)[0][-1]]) for rnr, row in enumerate(rockarray)]):
                pos[0] += 1
        elif blow == '<':
            if not pos[0]-1 < 0 and not any([any(row & grid[currentupper+pos[1]+rnr, pos[0]-1+np.where(row)[0][0]]) for rnr, row in enumerate(rockarray)]):
                pos[0] -= 1
        # check for vertical collision and stop if there is one
        if                             any([el & grid[currentupper+pos[1]-1, pos[0]+colnr] for colnr, el in enumerate(rockarray[0])])  \
            or (len(rockarray) > 1 and any([el & grid[currentupper+pos[1],   pos[0]+colnr] for colnr, el in enumerate(rockarray[1])])) \
            or (len(rockarray) > 2 and any([el & grid[currentupper+pos[1]+1, pos[0]+colnr] for colnr, el in enumerate(rockarray[2])])):
            # print(pos)
            break
        else:
            pos[1] -= 1
        
        # print(pos)
    
    yvals, xvals = np.where(grid[currentupper+pos[1]:currentupper+pos[1]+len(rockarray), pos[0]:pos[0]+len(rockarray[0])])
    for y, x in zip(yvals, xvals):
        if grid[y, x] and rockarray[y,x]:
            raise ValueError
    
    grid[currentupper+pos[1]:currentupper+pos[1]+len(rockarray), pos[0]:pos[0]+len(rockarray[0])] = rockarray | grid[currentupper+pos[1]:currentupper+pos[1]+len(rockarray), pos[0]:pos[0]+len(rockarray[0])]
    
    currentupper = max(currentupper, currentupper + pos[1] + len(rockarray) - 1)

print("\ncurrentupper:", currentupper)

print("\nTask 2:", (actualRounds-roundTilEndOf1stStack) // roundsPerPeriod * heightPerPeriod + currentupper)
