# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

lines = []
with open("input-day05", 'r') as f:
# with open("input-day05-test", 'r') as f:
    lines = f.readlines()

# read commands and input field
def readinput():
    s = []
    cmds = []
    parsecmds = True
    colpos = []
    for l in lines[::-1]: 
        if l != '\n' and parsecmds:
            cmd = l.replace('move', '')
            cmd = cmd.replace('from', '')
            cmd = cmd.replace('to', '')
            cmd = cmd.strip()
            cmd = cmd.split()
            cmd = [int(c) for c in cmd]
            cmds.append(cmd)
        elif l == '\n':
            parsecmds = False
            continue
    
        if l.startswith(' 1 '): # find the indices of the columns
            l = l[:-1]
            for i, c in enumerate(l):
                if c == ' ':
                    continue
                else:
                    colpos.append(i)
                    assert(len(colpos) == int(c))
            for _ in colpos:
                s.append([])
        elif not parsecmds:
            assert(len(colpos) > 0)
            for i, col in enumerate(colpos):
                if l[col] != ' ':
                    s[i].append(l[col])
    return s, cmds

def getResult(s):
    res = ''
    for stack in s:
        res += stack.pop()
    return res

# Task 1
s, cmds = readinput()
for c in cmds[::-1]:
    for _ in range(c[0]): # nr of moves
        val = s[c[1]-1].pop()
        s[c[2]-1].append(val)

print(f"Task 1: Top of the stacks is {getResult(s)}")

# Task 2
s, cmds = readinput()
helpstack = []
for c in cmds[::-1]:
    for _ in range(c[0]): # nr of moves
        helpstack.append(s[c[1]-1].pop())
    while helpstack:
        s[c[2]-1].append(helpstack.pop())
            
print(f"Task 2: Top of the stacks is {getResult(s)}")

