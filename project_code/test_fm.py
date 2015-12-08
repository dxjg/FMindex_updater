#! /usr/bin/env python
from __future__ import division
import math
from StringIO import StringIO
import sys
from collections import defaultdict
import random
import fmindex


def main():
    #Genome from paper is: CTCTGC 
    string = sys.argv[1]
    if '$' in string:
        print "Don't include $ in genome"
        sys.exit(0)
    fm = fmindex.createFM(string)
    import pprint
    index = int(sys.argv[2])
    insert = sys.argv[3]
    print "Before", fm.bwt
    afterString = string[:index] + insert + string[index:]
    afterfm = fmindex.FMindex(afterString)
    testIns(fm, index, insert)
    print "Expected result:", afterfm.bwt
    print "Actual results: ", fm.bwt
    #testDel(fm, index)

def testIns(fm, index, insert):
    print "Inserting", insert, "at index", index
    before = fm.bwt
    fm.insBase(index, insert)        
    print "After insertion"
    after = fm.bwt
    for i in range(len(fm.bwt)):
        print fm.sa[i], sorted(fm.bwt)[i], fm.bwt[i]

def testDel(fm, index):
    print "Deleting 'G' from index 2" 
    print fm.bwt
    fm.delBase(index)
    print "After deletion"
    for i in range(len(fm.bwt)):
        print fm.sa[i], sorted(fm.bwt)[i], fm.bwt[i]

if __name__ == '__main__':
    main()
