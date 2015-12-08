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
    import pprint
    numCorrect = 0
    numTotal = 0
    for c in "ACGT":
        for i in range(len(string)):
            fm = fmindex.createFM(string)
            print "\nTesting i =", i, ", c =,", c
            print "Before: T =", string +'$ ', "BWT =", fm.bwt
            afterString = string[:i] + c + string[i:]
            afterfm = fmindex.FMindex(afterString)
            print "After: T'= ", afterString + '$', "BWT'=", afterfm.bwt
            testIns(fm, i, c)
            #testDel(fm, index)
            if afterfm.bwt == fm.bwt:
                numCorrect += 1
            numTotal += 1
            print "Expected result:", afterfm.bwt
            print "Actual results: ", fm.bwt
            del fm
    print numTotal - numCorrect, "are wrong" 

    

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
