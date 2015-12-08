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
            fm = testIns(fm, i, c)
            #testDel(fm, index)
            if afterfm.bwt == fm.bwt:
                print "SUCCEEDED"
                numCorrect += 1
            else:
                print "FAILED"
                print "Correct result:", afterfm.bwt
                print "Actual results:", fm.bwt
                print " Actual | Correct"
                for j in range(len(afterfm.bwt)):
                    if j >= len(fm.bwt):
                        print " ", " ", " ", " ", "|", afterfm.sa[j], afterfm.isa[j], sorted(afterfm.bwt)[j], afterfm.bwt[j]
                    else:
                        print fm.sa[j], fm.isa[j], sorted(fm.bwt)[j], fm.bwt[j], "|", afterfm.sa[j], afterfm.isa[j], sorted(afterfm.bwt)[j], afterfm.bwt[j]
            numTotal += 1
            del fm
    print numTotal - numCorrect, "are wrong" 

    

def testIns(fm, index, insert):
    print "Inserting", insert, "at index", index
    before = fm.bwt
    fm.insBase(index, insert)
    return fm

def testDel(fm, index):
    print "Deleting 'G' from index 2" 
    print fm.bwt
    fm.delBase(index)

if __name__ == '__main__':
    main()
