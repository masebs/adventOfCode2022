#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

def buildList(multiply=1):
    with open("input-day20", 'r') as f:
    # with open("input-day20-test-3", 'r') as f:
        inp = [int(l) for l in f.readlines()]
        
    nrs = [] # contains the numbers in their original order
    newnr = Number(inp[0] * multiply)
    nrs.append(newnr)
    zero = None
    
    for n in inp[1:]:
        newnr = Number(n * multiply)
        nrs.append(newnr)
        if newnr.value == 0:
            zero = newnr
        
    for i in range(len(nrs)-1):
        nrs[i].succ = nrs[i+1]
        nrs[i+1].pred = nrs[i]
    nrs[0].pred = nrs[-1]
    nrs[-1].succ = nrs[0]
    
    # checkNrs(nrs[0])
    # checkNrs(nrs[0], backwards=True)
    
    return nrs, zero

class Number:
    def __init__(self, value):
        self.value = value
        self.pred = None
        self.succ = None

# def checkNrs(start, backwards = False): # for printing and / or debugging
#     print(f"backw? {backwards}: {start.value}, ", end='')
#     if backwards:
#         nxt = start.pred
#     else:
#         nxt = start.succ
    
#     count = 0
#     while nxt != start:
#         print(f"{nxt.value}, ", end='')
#         if backwards:
#             nxt = nxt.pred
#         else:
#             nxt = nxt.succ
#         count += 1
#         # if count >= len(nrs):
#         #     print("inifinite loop for n =", start.value, ", backwards", backwards)
#         #     raise ValueError
#     print()

def mix(nrs):
    for n in nrs:   
        if n.value != 0:
            removeLocAfter = n.succ
            removeLocBefore = n.pred
            removeLocBefore.succ = removeLocAfter
            removeLocAfter.pred = removeLocBefore
        
            if n.value > 0:
                insertLocAfter = n.succ
                for _ in range(n.value % (len(nrs)-1)):
                    insertLocAfter = insertLocAfter.succ
                insertLocBefore = insertLocAfter.pred
            elif n.value < 0:
                insertLocBefore = n.pred
                for _ in range(abs(n.value) % (len(nrs)-1)):
                    insertLocBefore = insertLocBefore.pred
                insertLocAfter = insertLocBefore.succ
            
            insertLocBefore.succ = n 
            insertLocAfter.pred = n
            n.succ = insertLocAfter
            n.pred = insertLocBefore
                
        # checkNrs(nrs[0])
        # checkNrs(nrs[0], backwards=True)

def getResult(cur):
    coords = []
    for i in range(3000):
        cur = cur.succ
        if (i+1)%1000 == 0:
            coords.append(cur.value)
    return coords
            
if __name__ == '__main__':    
    # Part 1
    nrs, zero = buildList()
    mix(nrs)
    coords = getResult(zero)
    
    print(coords)
    print(f"Part 1: {sum(coords)}")
    
    # Part 2
    nrs, zero = buildList(811589153)
    for k in range(10):
        print(f"\nround {k+1}\n")
        mix(nrs)
    coords = getResult(zero)
        
    print(coords)
    print(f"Part 2: {sum(coords)}")
    