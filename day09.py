# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

with open("input-day09", 'r') as f:
# with open("input-day09-test", 'r') as f:
# with open("input-day09-test-2", 'r') as f:
    moves = [l.strip().split() for l in f.readlines()]
    moves = [(m[0], int(m[1])) for m in moves]

hpos = [0,0]
tpos = [0,0]

tvisits = set()

for m in moves:
    for _ in range(abs(m[1])):
        # move head
        if m[0] == 'R':
            hpos[0] += 1
        elif m[0] == 'U':
            hpos[1] += 1
        elif m[0] == 'L':
            hpos[0] -= 1
        elif m[0] == 'D':
            hpos[1] -= 1
        # difference h to t
        diff = [hpos[0]-tpos[0], hpos[1]-tpos[1]]
        # move tail; no need to move if difference <= 1 in any or both directions
        if diff[0] == 0 and diff[1] > 1: # on the same column, H above T
            tpos[1] = hpos[1]-1
        elif diff[0] == 0 and diff[1] < -1: # on the same columns, H below T
            tpos[1] = hpos[1]+1
        elif diff[0] > 1 and diff[1] == 0: # on the same line, H right of T
            tpos[0] = hpos[0]-1
        elif diff[0] < -1 and diff[1] == 0: # on the same line, H left of T
            tpos[0] = hpos[0]+1
        elif abs(diff[0]) == 1 and diff[1] > 1: # diagonal, H above T
            tpos[1] = hpos[1]-1
            tpos[0] = hpos[0]
        elif abs(diff[0]) == 1 and diff[1] < -1: # diagonal, H below T
            tpos[1] = hpos[1]+1
            tpos[0] = hpos[0]
        elif diff[0] > 1 and abs(diff[1]) == 1: # diagonal, H right of T
            tpos[0] = hpos[0]-1
            tpos[1] = hpos[1]
        elif diff[0] < -1 and abs(diff[1]) == 1: # diagonal, H left of T
            tpos[0] = hpos[0]+1
            tpos[1] = hpos[1]
        
        tvisits.add(tuple(tpos))
        
    # print(f"move: {m}, hpos: {hpos}, tpos: {tpos}, diff {diff}")

print(f"Task 1: Tail visited {len(tvisits)} positions")

def printgrid(knotpos):
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

lenRope = 10
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
            
            # difference h to t
            diff = [hpos[0]-tpos[0], hpos[1]-tpos[1]]
            # print(k, diff)
            # move tail; no need to move if difference <= 1 in any or both directions
            if diff[0] == 0 and diff[1] > 1: # on the same column, H above T
                tpos[1] = hpos[1]-1
            elif diff[0] == 0 and diff[1] < -1: # on the same columns, H below T
                tpos[1] = hpos[1]+1
            elif diff[0] > 1 and diff[1] == 0: # on the same line, H right of T
                tpos[0] = hpos[0]-1
            elif diff[0] < -1 and diff[1] == 0: # on the same line, H left of T
                tpos[0] = hpos[0]+1
            elif abs(diff[0]) == 1 and diff[1] > 1: # diagonal, H above T
                tpos[1] = hpos[1]-1
                tpos[0] = hpos[0]
            elif abs(diff[0]) == 1 and diff[1] < -1: # diagonal, H below T
                tpos[1] = hpos[1]+1
                tpos[0] = hpos[0]
            elif diff[0] > 1 and abs(diff[1]) == 1: # diagonal, H right of T
                tpos[0] = hpos[0]-1
                tpos[1] = hpos[1]
            elif diff[0] < -1 and abs(diff[1]) == 1: # diagonal, H left of T
                # print('oink')
                tpos[0] = hpos[0]+1
                tpos[1] = hpos[1]
            elif diff[0] > 1 and diff[1] > 1 and diff[0] == diff[1]: # move along diagonal right up
                # print('oink')
                tpos[0] = hpos[0]-1
                tpos[1] = hpos[1]-1
            elif diff[0] < -1 and diff[1] < -1 and diff[0] == diff[1]: # move along diagonal left down
                # print(k, hpos, tpos, diff)
                # print('oink')
                tpos[0] = hpos[0]+1
                tpos[1] = hpos[1]+1
            elif diff[0] > 1 and diff[1] < -1 and diff[0] == -diff[1]: # move along diagonal right down
                # print('oink')
                tpos[0] = hpos[0]-1
                tpos[1] = hpos[1]+1
            elif diff[0] < -1 and diff[1] > 1 and diff[0] == -diff[1]: # move along diagonal left up
                # print('oink')
                tpos[0] = hpos[0]+1
                tpos[1] = hpos[1]-1
        tvisits.add(tuple(knotpos[-1]))
    # printgrid(knotpos)


print(f"Task 2: Tail visited {len(tvisits)} positions")

