# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

from collections import deque
from math import prod

with open("input-day11", 'r') as f:
# with open("input-day11-test", 'r') as f:
    lines = [l.strip().split() for l in f.readlines()]

def readInput(lines):
    items = []
    ops =  []
    testModulo = []
    targets = []
    counter = []
    
    for i in range(0, len(lines), 7):
        items.append(deque())
        for item in lines[i+1]:
            try:
                items[-1].append(int(item.strip(',')))
            except ValueError:
                continue
        if lines[i+2][-1] == 'old':
            ops.append([lines[i+2][-2], lines[i+2][-1]])
        else:
            ops.append([lines[i+2][-2], int(lines[i+2][-1])])
        testModulo.append(int(lines[i+3][-1]))
        targets.append([int(lines[i+4][-1]), int(lines[i+5][-1])])
        counter.append(0)
    return items, ops, testModulo, targets, counter

def play(Nrounds, items, ops, testModulo, targets, counter, divide=True, verbose=False):
    Nmonkeys = len(items)
    masterMod = prod(testModulo) # that's the trick: Keep the items modulo the product of all divisors
       # inspired by Reddit: (a mod k*n) mod n = a mod n for any integer k 
       # so instead of storing a, we store a mod k*n where k = the product of all testModulos
    for i in range(Nrounds):
        for j in range(Nmonkeys):
            # print(f"\n  Monkey {j}:")
            while items[j]:
                counter[j] += 1
                it = items[j].popleft()
                # print(f"\n   item {it}")
                operand = it if ops[j][1] == 'old' else ops[j][1]
                it = it + operand  if ops[j][0] == '+' else it * operand
                if divide:
                    it = it // 3
                # print(f"   new value: {it}")
            
                if it % testModulo[j] == 0:
                    items[targets[j][0]].append(it % masterMod)
                    # print(f"   target: {targets[j][0]}")
                else:
                    items[targets[j][1]].append(it % masterMod)
                    # print(f"   target: {targets[j][1]}")
        
        if verbose:
            if divide:
                print(f"\nRound {i+1}:")
                for m in range(Nmonkeys):
                    print(f"Monkey {m}: {list(items[m])}")
            else:
                if (i+1) % 1000 == 0:
                    print(f"\nRound {i+1}")
                    for m in range(Nmonkeys):
                        print(f"Monkey {m}: {counter[m]}")

    counter.sort()
    return counter[-1]*counter[-2]

def main():
    # Task 1
    Nrounds = 20
    items, ops, testModulo, targets, counter = readInput(lines)
    res1 = play(Nrounds, items, ops, testModulo, targets, counter, divide=True, verbose=False)
    print(f"\nTask 1: Monkey business level is {res1}")    
    
    # Task 2
    Nrounds = 10000
    items, ops, testModulo, targets, counter = readInput(lines)
    res2 = play(Nrounds, items, ops, testModulo, targets, counter, divide=False, verbose=False)
    print(f"\nTask 2: Monkey business level is {res2}")    

if __name__ == "__main__":
    main()