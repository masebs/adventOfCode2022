# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

from numpy import sign 

with open("input-day09", 'r') as f:
# with open("input-day09-test", 'r') as f:
# with open("input-day09-test-2", 'r') as f:
    moves = [l.strip().split() for l in f.readlines()]
    moves = [(m[0], int(m[1])) for m in moves]

def printgrid(knotpos): # only for debug; requires a sufficiently large grid (increase maxx and maxy if too small)
    grid = []
    maxx = max(k[0] for k in knotpos) + 5
    maxy = max(k[1] for k in knotpos) + 5
    for i in range(maxy):
        grid.append([])
        for _ in range(maxx):
            grid[i].append('.')
    for k, pos in enumerate(knotpos[::-1]):
        grid[pos[1]][pos[0]] = len(knotpos)-1-k
    for i in range(maxy-1,-1,-1):
        for j in range(maxx):
            print(grid[i][j], end='')
        print('\n', end='')
    print()

def doMoves(moves: list, lenRope: int) -> int:
    tvisits = set()
    knotpos = []
    for k in range(lenRope):
        knotpos.append([0,0])

    for m in moves:
        for _ in range(abs(m[1])):
            # move head
            if m[0] == 'R':
                knotpos[0][0] += 1
            elif m[0] == 'U':
                knotpos[0][1] += 1
            elif m[0] == 'L':
                knotpos[0][0] -= 1
            elif m[0] == 'D':
                knotpos[0][1] -= 1
                
            for k in range(1, lenRope):
                hpos = knotpos[k-1]
                tpos = knotpos[k]
                
                # move tail; no need to move if difference <= 1 in any or both directions
                diff = [hpos[0]-tpos[0], hpos[1]-tpos[1]] # difference h to t
                
                if diff[0] == 0: # on the same column
                    tpos[1] = hpos[1] - sign(diff[1])
                if diff[1] == 0: # on the same line
                    tpos[0] = hpos[0] - sign(diff[0])
                if abs(diff[0]) == 1 and abs(diff[1]) > 1: # one line offset to left or right, head moving up or down
                    tpos[1] = hpos[1] - sign(diff[1])
                    tpos[0] = hpos[0]
                if abs(diff[1]) == 1 and abs(diff[0]) > 1: # one line offset to up or down, head moving left or right
                    tpos[0] = hpos[0] - sign(diff[0])
                    tpos[1] = hpos[1]
                if abs(diff[0]) == abs(diff[1]): # diagonal offset (by 1 or 2) and diagonal motion 
                    tpos[0] = hpos[0] - sign(diff[0])
                    tpos[1] = hpos[1] - sign(diff[1])

            tvisits.add(tuple(knotpos[-1]))
        # printgrid(knotpos)
    return len(tvisits)

res1 = doMoves(moves, lenRope=2)
print(f"Task 1: Tail visited {res1} positions")

res2 = doMoves(moves, lenRope=10)
print(f"Task 2: Tail visited {res2} positions")


