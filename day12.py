# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""
# 483 too high

import numpy as np
from queue import PriorityQueue, deque

def readInput(filename):
    with open(filename, 'r') as f:
        grid = [[ord(i)-ord('a') for i in c] for l in f.readlines() for c in l.split()]
    grid = np.array(grid, dtype=int)
    nrows, ncols = grid.shape
    (starty, startx) = (a[0] for a in np.where(grid==-14))
    (endy, endx) = (a[0] for a in np.where(grid==-28))
    grid[starty, startx] = 0
    grid[endy, endx] = ord('z')-ord('a')
    return grid, (starty, startx), (endy, endx)

class Node:
    def __init__(self, index, value):
        self.index = index
        self.value = value
        self.dist  = 9e9
        self.prev  = None

def getNeighborIndices(n, bounds):
    nbs = []
    i,j = n.index
    idcs = [(i-1, j), (i, j-1), (i+1, j), (i, j+1)]
    for idx in idcs:
        if 0 <= idx[0] < bounds[0] and 0 <= idx[1] < bounds[1]:
            nbs.append(idx)
    return nbs

def createGraph(grid):
    ngrid = []
    for i, r in enumerate(grid):
        ngridrow = []
        for j, c in enumerate(r):
            n = Node((i,j), c)
            ngridrow.append(n)
        ngrid.append(ngridrow)
    return ngrid
        
def BFS(grid, startidx, endidx, backwards=False):
    q = deque()
    visited = set()
    ngrid = createGraph(grid)
    start = ngrid[startidx[0]][startidx[1]]
    start.dist = 0 # set source distance
    if not backwards:
        end = ngrid[endidx[0]][endidx[1]]
    q.append(start)
    visited.add(start.index)
    
    while q:
        print(len(visited))
        n = q.popleft()
        if (not backwards and n == end) or (backwards and n.value == 0):
            return n
        
        nbs = [ngrid[idx[0]][idx[1]] for idx in getNeighborIndices(n, (len(ngrid), len(ngrid[0])))]
        for nbr in nbs:
            if nbr.index not in visited:
                if (not backwards and nbr.value-n.value <= 1) or (backwards and nbr.value-n.value >= -1):
                    nbr.prev = n
                    nbr.dist = n.dist + 1
                    q.append(nbr)
                    visited.add(n.index)
                
def dijkstra(grid, startidx, endidx, backwards=False): # with distance = number of steps, this is effectively BFS
    yellow = PriorityQueue() # prio q seems to reduce by a factor of almost 10 to ~3s
    yellowSet = set() # using additional Set for more efficient "in" (contains) op saves ~3s
    green  = set() # using set instead of list for green: 26 s w/o, 45 s with output instead of > 10 min with list
    ngrid = createGraph(grid)
    
    start = ngrid[startidx[0]][startidx[1]]
    start.dist = 0 # set source distance
    if not backwards:
        end = ngrid[endidx[0]][endidx[1]]
    yellow.put((start.dist, start.index))
    yellowSet.add(start.index)
    
    while not yellow.empty():
        x, y = yellow.get(block=False)[1]
        n = ngrid[x][y]
        green.add(n.index)
        # print(f" setting green: idx {n.index}, len(green): {len(green)}, len(yellow): {yellow.qsize()}")
        if (not backwards and n == end) or (backwards and n.value == 0):
            return n
        nbs = [ngrid[idx[0]][idx[1]] for idx in getNeighborIndices(n, (len(ngrid), len(ngrid[0])))]
        for nbr in nbs:
            if nbr.index not in green and nbr.index not in yellowSet:
                if (not backwards and nbr.value-n.value <= 1) or (backwards and nbr.value-n.value >= -1): # only for neighbors which are maximum one step up
                    nbr.prev = n
                    # nbr.dist = n.dist + nbr.value # this would be usual Dijkstra (looking for total cost)
                    nbr.dist = n.dist + 1 # here: distance = path length, so just increment
                    # print(f"n: ({n.index[1]}, {n.index[0]}) {n.value}, {n.dist}; nbr: {nbr.value}, {nbr.dist}")
                    yellow.put((nbr.dist, nbr.index))
                    yellowSet.add(nbr.index)
            elif nbr in yellowSet: # we reach this node again
                # if nbr.dist > n.dist + nbr.value: # usual Dijkstra
                if nbr.dist > n.dist + 1:
                    if n(not backwards and nbr.value-n.value <= 1) or (backwards and nbr.value-n.value >= -1): # only for neighbors which are maximum one step up
                        nbr.prev = n
                        # nbr.dist = n.dist + nbr.value # this would be usual Dijkstra (looking for total cost)
                        nbr.dist = n.dist + 1 # here: distance = path length, so just increment

def traceback(end, startidx): # for debug or visualization
    # trace back to start
    countsteps = 0
    n = end
    print(f"\nTarget reached at dist {n.dist}, retracing...")
    print(f"({n.index[1]}, {n.index[0]}): {chr(n.value+ord('a'))} {n.dist}")
    while n.index != startidx:
        n = n.prev
        print(f"({n.index[1]}, {n.index[0]}): {chr(n.value+ord('a'))} {n.dist}")
        countsteps += 1
    
def main():
    grid, startidx, endidx = readInput("input-day12")
    # grid, startidx, endidx = readInput("input-day12-test")
    
    # Task 1
    # endnode = dijkstra(grid, startidx, endidx)
    endnode = BFS(grid, startidx, endidx)
    # traceback(endnode, startidx)
    print(f"Task 1: Easiest path takes {endnode.dist} steps")
    
    # Task 2: search from target to any point with height 'a' 
    # (this works because the first one found is automatically the one with the shortest path, as we only do BFS)
    # endnode = dijkstra(grid, endidx, None, backwards=True) 
    endnode = BFS(grid, endidx, None, backwards=True) 
    print(f"Task 2: Fewest steps from any possible starting point is {endnode.dist}")

if __name__ == "__main__":
    main()