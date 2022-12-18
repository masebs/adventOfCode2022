# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

# Only the part for simplification of the graph (all nodes with rate 0 and two neighbors can be omitted)
# Actual solutions found by hand in the simplified graph  
from functools import lru_cache

with open("input-day16", 'r') as f:
# with open("input-day16-test", 'r') as f:
    lines = [l.strip().split() for l in f.readlines()]

valves = {}
known = set()
for l in lines:
    nbrs = []
    for nbr in l[::-1]:
        if nbr.startswith("valve"):
            break
        else:
            nbrs.append(nbr.strip(','))
    rate = int(l[4].split('=')[-1][:-1])
    valves[l[1]] = [rate, [(n, 1) for n in nbrs]]

def simplifyGraph(cur, seen):
    global valves
    curnode = valves[cur]
    seen.add(cur)
    # print(" processing", cur)
    toProcess = curnode[1].copy()
    
    if curnode[0] == 0 and len(curnode[1]) == 2:
        n1 = curnode[1][0][0]
        n2 = curnode[1][1][0]
        # print(n1, curnode[1][1], n2, [v for v in valves[n1][1] if v[0] == cur][0])
        # remove cur node and directly connect the neighbors
        n1OldNbr = [v for v in valves[n1][1] if v[0] == cur][0]
        valves[n1][1].remove(n1OldNbr)
        valves[n1][1].append((n2, 1+n1OldNbr[1]))
        n2OldNbr = [v for v in valves[n2][1] if v[0] == cur][0]
        valves[n2][1].remove(n2OldNbr)
        valves[n2][1].append((n1, 1+n2OldNbr[1]))
        del valves[cur]
        
    for n in toProcess:
        if n[0] not in seen:
            simplifyGraph(n[0], seen)
             
simplifyGraph('AA', set())
print(valves)

# # @lru_cache(maxsize = None)
# def searchPath(cur, timeRemaining, opennodes=set()):
#     # visited.add(cur)
#     curnode = valves[cur]
#     vals = [0]
#     for n in curnode[1]:
#         # open current node
#         if timeRemaining - n[1] - 1 > 0 and n[0] not in opennodes:
#             opennodes.add(n[0])
#             vals.append(searchPath(n[0], timeRemaining-n[1]-1, opennodes) + timeRemaining*curnode[0])
#         # don't open current node
#         if timeRemaining - n[1] > 0:
#             vals.append(searchPath(n[0], timeRemaining-n[1], opennodes))
#     print(curnode, max(vals))
#     return max(vals)
    
# print(searchPath('AA', 30))
