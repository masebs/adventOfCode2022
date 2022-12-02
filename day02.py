# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

lines = []
with open("input-day02", 'r') as f:
# with open("input-day02-test", 'r') as f:
    lines = f.readlines()
    
scoremap = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}

rounds = []
for l in lines:
    rounds.append([scoremap[l[0]], scoremap[l[2]]])    
    
def score1(p1, p2):
    s = p2
    if p2-p1 in [1,-2]:
        s += 6
    elif p1 == p2:
        s += 3
    return s
    
myscore = 0
for r in rounds:
    myscore += score1(r[0], r[1])
        
print(f"Task 1: My score is {myscore}")

def score2(p1, p2):
    p2val = None
    
    if p2 == 1: # should lose
        p2val = (p1-1-1) % 3 + 1
    elif p2 == 2: # should be draw
        p2val = p1
    elif p2 == 3: # should win
        p2val = (p1+1-1) % 3 + 1
        
    return score1(p1, p2val)

myscore = 0
for r in rounds:
    myscore += score2(r[0], r[1])

print(f"Task 2: My score is {myscore}")
