# -*- coding: utf-8 -*-
"""
Advent of Code 2022

@author marc 
"""

# assumptions: We always ls folders before cd'ing into any subfolder, no folder is ls'ed twice, folders are non-empty 

def main():
    with open("input-day07", 'r') as f:
    # with open("input-day07-test", 'r') as f:
        lines = [l.strip() for l in f.readlines()]
        
    root = buildTree(lines)
    calcSize(root)
    
    res1 = task1(root)
    print(f"Task 1: {res1}")

    totalsize = 70000000
    requiredSize = 30000000
    unusedSize = totalsize - root.size
    toDeleteSize = requiredSize - unusedSize
    res2 = task2(root, toDeleteSize)
    print(f"Task 2: {res2}")

class Node:
    def __init__(self):
        self.children = []
        self.parent = None
        self.name = None
        self.size = None

def buildTree(lines):
    root = Node()
    root.name = '/'
    cd = root
    nlines = len(lines)
    
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
    return root
            
# go through tree in postorder to calculate sizes
def calcSize(cd):
    if not cd.children: # it's a file or empty folder
        if cd.size == None: # empty folder (doesn't occur actually)
            return 0
        else: # file
            return cd.size
    else: # it's a non-empty folder
        size = 0
        for c in cd.children:
            size += calcSize(c)
        cd.size = size
        return size
        
def task1(cd): # go through the whole tree and sum up all dirs smaller than the requested size
    size = 0
    for c in cd.children: # get sizes for all children which are directories
        if c.children:
            size += task1(c)
    if cd.size <= 100000: # add myself if i'm small enough
        size += cd.size
    return size

def task2(cd, toDeleteSize):
    if cd.children: # if it's a directory
        childsizes = [task2(c, toDeleteSize) for c in cd.children]
        childsizes.sort() # first elem is size of smallest deletable directory (if not 999999999 = it's a file or too small)
        if cd.size >= toDeleteSize and cd.size <= childsizes[0]:
            return cd.size # the current directory is the smallest deletable so far
        else:
            return childsizes[0] # one of the children is smaller but already deletable, so return this one
    else: # for files: return large value
        return 99999999

def printFiles(cd, depth=0): # for debug
    p = ' '*depth
    p += f"- {cd.name} ({'dir' if cd.children else 'file'}, {cd.size})"
    print(p)
    for c in cd.children:
        printFiles(c, depth+1)
        
if __name__ == "__main__":
    main()