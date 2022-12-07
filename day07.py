# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""
# assumptions: We always ls folders before cd'ing into any subfolder, no folder is ls'ed twice, folders are non-empty 

with open("input-day07", 'r') as f:
# with open("input-day07-test", 'r') as f:
    lines = [l.strip() for l in f.readlines()]
nlines = len(lines)

class Node:
    def __init__(self):
        self.children = []
        self.parent = None
        self.name = None
        self.size = None

root = Node()
root.name = '/'
cd = root

for i,l in enumerate(lines): # build tree
    # print("line", l)
    if l.startswith('$'): 
        if l.split()[1] == "ls": # create all listed dirs
            lineidx = i+1
            nextline = lines[lineidx]
            while not nextline.startswith('$'): # read ahead until next prompt
                newdir = Node()
                newdir.parent = cd
                cd.children.append(newdir)
                if nextline.startswith('dir'):
                    newdir.name = nextline.split()[1]
                else: # it's a file
                    (newsize, newname) = nextline.split()
                    newdir.size = int(newsize)
                    newdir.name = newname
                lineidx += 1
                if lineidx >= nlines:
                    break
                else:
                    nextline = lines[lineidx]
            
        elif l.split()[1] == "cd": # assuming we always do ls in a dir before cd'ing to it
            changeTo = l.split()[-1]
            if changeTo == '/':
                cd = root
            elif changeTo == '..':
                cd = cd.parent
            else:
                for child in cd.children:
                    if child.name == changeTo:
                        cd = child
                        break
                assert(cd.name == changeTo)
            
# go through tree in postorder to calculate sizes
def calcSize(cd):
    if not cd.children: # it's a file or empty folder
        if cd.size == None: # empty folder
            return 0
        else: # file
            return cd.size
    else:
        size = 0
        for c in cd.children:
            size += calcSize(c)
        cd.size = size
        return size
        
calcSize(root)

correctSizedDirs = []

def findDirsForTask1(cd): # go through the whole tree and write out all dirs in requested size range
    if cd.children: # only for directories; ignore files
        if cd.size <= 100000:
            correctSizedDirs.append(cd.size) # write to external list as we need to count some dirs and files multiple times
        for c in cd.children:
            findDirsForTask1(c) 
    
def printFiles(cd, depth=0): # for debug
    p = ' '*depth
    p += f"- {cd.name} ({'dir' if cd.children else 'file'}, {cd.size})"
    print(p)
    for c in cd.children:
        printFiles(c, depth+1)

findDirsForTask1(root)
res1 = sum(correctSizedDirs)

print(f"Task 1: {res1}")

totalsize = 70000000
requiredSize = 30000000
unusedSize = totalsize - root.size
toDeleteSize = requiredSize - unusedSize

deletableDirs = []

def findDirsForTask2(cd):
    if cd.children:
        if cd.size > toDeleteSize:
            deletableDirs.append(cd.size)
        for c in cd.children:
            findDirsForTask2(c)

findDirsForTask2(root)

print(f"Task 2: {min(deletableDirs)}")

