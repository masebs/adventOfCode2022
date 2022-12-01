# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

lines = []
with open("input-day01", 'r') as f:
# with open("input-day01-test", 'r') as f:
    lines = f.readlines()
    
vals = []

count = 0
for l in lines:
    if l != '\n':
        count += int(l[:-1])
    else: 
        vals.append(count)
        count = 0
vals.append(count) # at eof
        
print(f"Task 1: Maximum sum is {max(vals)}")

most = []
for i in range(3):
    most.append(max(vals))
    vals.remove(max(vals))

print(f"Task 2: Sum of max 3: {sum(most)}")  
