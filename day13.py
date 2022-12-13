# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

import ast

with open("input-day13", 'r') as f:
# with open("input-day13-test", 'r') as f:
    lines = [l.strip() for l in f.readlines()]

packets = []

# def parseList(string):
#     skip = range(-1,-1)
#     curlist = []
#     for i,c in enumerate(string):
#         if i not in skip:
#             if c == '[':
#                 sublist, charcount = parseList(string[i+1:])
#                 curlist.append(sublist)
#                 skip = range(i, i+charcount)
#             elif c == ']':
#                 return curlist, i
#             else:
#                 curlist.append(c)
#     properlist = []
#     curnr = 0
#     digitcount = 0
#     while curlist:
#         cur = curlist.pop(0)
#         if type(cur) == list:
#             properlist.append(cur)
#         elif type(cur) == ',':
#             properlist.add(curnr)
#             curnr = 0
#             digitcount = 0
#         else: # number
#             digitcount +=1
#             curnr += int(cur) * digitcount*10
        
#     print(properlist)
#     return properlist
                
    
for l in lines:
    if l != '':
        packets.append(ast.literal_eval(l))
        # packets.append(parseList(l))
        # print(f" curitem: {curitem}")
  
def compare(el1, el2):
    if type(el1) == list and type(el2) == int:
        el2 = [el2]
    elif type(el1) == int and type(el2) == list:
        el1 = [el1]
    
    # print(f"in rekCheck: {el1} | {el2}")
    if type(el1) == int and type(el2) == int:
        if el1 < el2: # correct order
            return 1
        elif el1 > el2: # wrong order
            return -1
    elif type(el1) == list and type(el2) == list:
        for innerel1, innerel2 in zip(el1, el2): # zip only zips up to the end of the shorter one
            val = compare(innerel1, innerel2)
            if val != 0:
                return val
        if len(el1) < len(el2):
           return 1
        elif len(el1) > len(el2):
            return -1
    else:
        print("SHOULDN'T HAPPEN")
    return 0        

rightorderidcs = []

for i in range(0, len(packets), 2):
    p1 = packets[i]
    p2 = packets[i+1]
    idx = i // 2
    # print(p1)
    # print(p2)
    # print()
    order = compare(p1, p2)
       
    if order == 1:
        # print('-> right order!')
        rightorderidcs.append(idx+1)
    # elif order == -1:
    #     print('-> wrong order!')
    # else:
    #     print('-> dunno')
    # print()
    # print()
    
print(f"Task 1: Sum of indices of correctly ordered pairs: {sum(rightorderidcs)}")

# Task 2: Bubblesort
packets.append([[2]]) # additional packages according to task
packets.append([[6]])

def swapPackets(packets, idx1, idx2):
    swap = packets[idx1]
    packets[idx1] = packets[idx2]
    packets[idx2] = swap

for n in range(len(packets)): # do bubblesort
    for i in range(len(packets)-1):
        if compare(packets[i], packets[i+1]) == -1:
            swapPackets(packets, i, i+1)

# for p in packets:
#     print(p)

res2 = (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
print(f"Task 2: Product of the divider packages is {res2}")

