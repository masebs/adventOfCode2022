#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

import re

def readInput():
    with open("input-day21", 'r') as f:
    # with open("input-day21-test", 'r') as f:
        lines = [l.strip().split(': ') for l in f.readlines()]
    
    monkeysNr = []
    monkeysNrVals = []
    monkeysExpr = []
    for l in lines:
        try:
            monkeysNrVals.append(int(l[1]))
            monkeysNr.append(l[0])
        except ValueError:
            monkeysExpr.append((l[0], re.findall('([a-z]+)\s([-+*/])\s([a-z]+)', l[1])[0]))
    return monkeysNr, monkeysNrVals, monkeysExpr

def reduceMonks(monkeysNr, monkeysNrVals, monkeysExpr):
    monkeysNrSet = set(monkeysNr)
    reducedExpr = []
    lastHumn = 'humn'
    while monkeysExpr:
        toRemove = []
        for monk, expr in monkeysExpr:
            if expr[0] in monkeysNrSet and expr[2] in monkeysNrSet:
                # print("Replacing", monk, expr)
                nr1 = monkeysNrVals[monkeysNr.index(expr[0])]
                nr2 = monkeysNrVals[monkeysNr.index(expr[2])]
                if expr[1] == '+':
                    result = nr1 + nr2
                elif expr[1] == '-':
                    result = nr1 -  nr2
                elif expr[1] == '*':
                    result = nr1 * nr2
                elif expr[1] == '/':
                    result = nr1 // nr2
                monkeysNr.append(monk)
                monkeysNrSet.add(monk)
                monkeysNrVals.append(result)
                toRemove.append((monk, expr))
        for r in toRemove:
            if r[1][0] == lastHumn or r[1][2] == lastHumn:
                lastHumn = r[0]
                reducedExpr.append(r)
            monkeysExpr.remove(r)
        # reducedExpr.append(monkeysExpr.copy())
    return monkeysNr, monkeysNrVals, reducedExpr

def getNrAndVarIdx(expr): # returns (index of variable, index of number)
    if type(expr[0]) == int and type(expr[1] == str):
        return (0, 2)
    elif type(expr[0]) == str and type(expr[1] == int):
        return (2, 0)
    else: # shouldn't happen on our input
        return None

if __name__ == '__main__':
    
    # Part 1
    # solve, and already get the reduced expression to be used for part 2
    monkeysNr, monkeysNrVals, reducedExpr = reduceMonks(*readInput())
    rootidx = monkeysNr.index('root')
    rootval = monkeysNrVals[rootidx]
    print(f"\nPart 1: root yells {rootval}\n")
    
    # Part 2
    # first, remove all variables which appear in the reduced expression from the known variables
    for monk in [r[0] for r in reducedExpr]:
        del monkeysNrVals[monkeysNr.index(monk)]
        monkeysNr.remove(monk)
    del monkeysNrVals[monkeysNr.index('humn')]
    monkeysNr.remove('humn')
    
    # in the reduced expression, replace all known variables by their value
    for i, r in enumerate(reducedExpr):
        if r[1][0] in monkeysNr:
            reducedExpr[i] = (r[0], (monkeysNrVals[monkeysNr.index(r[1][0])], r[1][1], r[1][2]))
        if r[1][2] in monkeysNr:
            reducedExpr[i] = (r[0], (r[1][0], r[1][1], monkeysNrVals[monkeysNr.index(r[1][2])]))
    
    # now calculate backwards from the desired value at root down to the required 'humn'
    # (this assumes that the variables are used (only) in the line after they are calculated, and that 
    #  only one variable is used per line, which is true for our input)
    nridx, varidx = getNrAndVarIdx(reducedExpr[-1])
    nextval = reducedExpr[-1][1][nridx]
    # print(nextval)
    for r in reducedExpr[-2::-1]:
        # print("processing", r)
        nridx, varidx = getNrAndVarIdx(r[1])
        if r[1][1] == '+':
            nextval = nextval - r[1][nridx]
        elif r[1][1] == '-':
            if nridx == 2:
                nextval = nextval + r[1][nridx]
            else:
                nextval = r[1][nridx] - nextval
        elif r[1][1] == '*':
            nextval = nextval // r[1][nridx]
        elif r[1][1] == '/':
            if nridx == 2:
                nextval = nextval * r[1][nridx]
            else:
                nextval = r[1][nridx] // nextval
        # print(nextval)
                
    print(f"Part 2: human should yell {nextval}\n")
            
        