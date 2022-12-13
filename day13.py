# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

def readInput(filename):
    with open(filename, 'r') as f:
        lines = [l.strip() for l in f.readlines()]
    
    packets = []
    for l in lines:
        if l != '':
            # packets.append(eval(l)) # the cheating and risky way (conveniently it's Python syntax)
            packets.append(parseList(l)) # the proper way 
    return lines
        
def parseList(string):
    curlist = []
    stack = []
    nr = ''
    for i,c in enumerate(string):
        # print(f"char {c}, stack: {stack}")
        if c == '[': # open a new sub-list and store the current one on the stack
            stack.append(curlist) 
            curlist = []
        elif c == ',':
            if nr: # append nr; if nr='', then we are after a ']', so nothing to do
                curlist.append(int(nr))
                nr = ''
        elif c == ']': # this closes the current sub-list, so...
            if nr:     # if before it was a number, append it; otherwise we are after a ']'
                curlist.append(int(nr))
                nr = ''
            parentlist = stack.pop()   # get the next outer list from stack (it must be on top now)
            parentlist.append(curlist) # append the current inner list to the outer list
            curlist = parentlist       # go one level up
        else: # a number (character), so just collect in a string
            nr += c 
    return curlist[0] # the outer list ever only contains one single item (if there is only one list per line)

# compares two elements (lists or int) recursively; returns 1 if el1 < el2, -1 if el1 > el2, 0 if equal
def compare(el1, el2): 
    if type(el1) == list and type(el2) == int:
        el2 = [el2]
    elif type(el1) == int and type(el2) == list:
        el1 = [el1]
    
    # print(f"in compare: {el1} | {el2}")
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
    
def main():
    lines = readInput("input-day13")
    # lines = readInput("input-day13-test")
    
    packets = [parseList(l) for l in lines if l]
    rightorderidcs = [i//2+1 for i in range(0, len(packets), 2) if compare(packets[i], packets[i+1]) == 1]
        
    print(f"Task 1: Sum of indices of correctly ordered pairs: {sum(rightorderidcs)}")
    
    # Task 2: Bubblesort
    packets.append([[2]]) # additional packages according to task
    packets.append([[6]])
    
    for n in range(len(packets)): # do bubblesort; the funny way
        for i in range(len(packets)-1 - n):
            if compare(packets[i], packets[i+1]) == -1:
                packets[i], packets[i+1] = packets[i+1], packets[i]
    
    # from functools import cmp_to_key # use sort with custom compare function as key; the fast way
    # packets.sort(key=cmp_to_key(compare), reverse=True)
    
    # for p in packets:
    #     print(p)
    
    res2 = (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
    print(f"Task 2: Product of the divider packages is {res2}")

if __name__ == "__main__":
    main()