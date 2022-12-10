# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

with open("input-day10", 'r') as f:
# with open("input-day10-test", 'r') as f:
    cmds = [l.strip().split() for l in f.readlines()]

def run(cmds, evalTimes):
    clock = 1
    reg = 1
    evals = []
    regvals = []
    
    def evaluate():
        if clock in evalTimes:
            evals.append(reg*clock)
            regvals.append(reg)
    
    evaluate()
    for c in cmds:
        if c[0] == 'noop':
            clock += 1
            evaluate()
        elif c[0] == 'addx':
            clock += 1
            evaluate()
            clock += 1
            reg += int(c[1])
            evaluate()
        else:
            raise ValueError
    return evals, regvals


def printgrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            print(grid[i][j], end='')
        print('\n', end='')
    print()

def main():
    # Task 1
    evals, _ = run(cmds, [20, 60, 100, 140, 180, 220])
    print(f"Task 1: Sum of signal strengths is {sum(evals)}")
    
    # Task 2
    _, regvals = run(cmds, range(241))

    grid = [[], [], [], [], [], []] # active pixels in each row

    for clock in range(240):
        if clock%40 in range(regvals[clock]-1, regvals[clock]+2):
            grid[clock//40].append('#')
        else:
            grid[clock//40].append('.')
            
    print("Task 2: Please read:")
    printgrid(grid)

if __name__ == "__main__":
    main()