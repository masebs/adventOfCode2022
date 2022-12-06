# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

from collections import deque

with open("input-day06", 'r') as f:
# with open("input-day06-test", 'r') as f:
    lines = f.readlines()
inp = lines[0].strip()

def findStart_list(m, nrChar): # inital version: Using list as fifo queue, removing first elem (inefficient)
    q = []
    for i, c in enumerate(inp):
        q.append(c)
        if len(q) == nrChar:
            if len(set(q)) == nrChar:
                return i+1
            q.remove(q[0])

def findStart_deque(m, nrChar): # using deque instead of list: Removing at the left-hand side is more efficient
    q = deque()
    for i, c in enumerate(inp):
        q.append(c)
        if len(q) == nrChar:
            if len(set(q)) == nrChar:
                return i+1
            q.popleft()

def findStart_substrings(m, nrChar): # investigating slices out of the message (no queue or list involved)
    for i in range(len(m)-nrChar):
        localChars = m[i:i+nrChar]
        if len(set(localChars)) == nrChar:
            return i+nrChar
        
        
# res1 = findStart_list(inp, 4)
# res2 = findStart_list(inp, 14)
# res1 = findStart_deque(inp, 4)
# res2 = findStart_deque(inp, 14)
res1 = findStart_substrings(inp, 4)
res2 = findStart_substrings(inp, 14)

print(f"Task 1: Transmission starts at {res1}")
print(f"Task 2: Message starts at {res2}")

