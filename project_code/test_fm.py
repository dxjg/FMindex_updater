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
    findLong(int(sys.argv[1]))
    '''
    string = sys.argv[1]
    if '$' in string:
        print "Don't include $ in genome"
        sys.exit(0)
    if len(sys.argv) == 4:
        fm = testIns(string, int(sys.argv[3]), sys.argv[2])
    else:
        stressTest(string)
    '''
def findLong(n):
    random.seed(5234)
    string = ''.join([random.choice('ACGT') for _ in xrange(n)])
    print string
    stressTest(string)
    return 


def stressTest(string): 
    numCorrect = 0
    numTotal = 0
    for c in "ACGT":
        for i in range(len(string) + 1):
            fm = fmindex.createFM(string)
            print "\n===================================================="
            print "Testing i =", i, ", c =,", c
            print "Before: T =", string +'$ ', "BWT =", fm.bwt
            afterString = string[:i] + c + string[i:]
            afterfm = fmindex.FMindex(afterString)
            print "After: T'= ", afterString + '$', "BWT'=", afterfm.bwt
            fm = testIns(string, i, c)
            #fm = testDel(fm, i)
            if afterfm.bwt == fm.bwt:
                print "SUCCEEDED"
                numCorrect += 1
            else:
                print "FAILED"
            print "Correct result:", afterfm.bwt
            print "Actual results:", fm.bwt
            print " Actual | Correct"
            for j in range(len(afterfm.bwt)):
                correctResults=' '.join([str(afterfm.sa[j]),str(afterfm.isa[j]), sorted(afterfm.bwt)[j], afterfm.bwt[j]])
                if j >= len(fm.bwt):
                    actualResults = "         |"
                else:
                    actualResults=' '.join([str(fm.sa[j]),str(fm.isa[j]),sorted(fm.bwt)[j],fm.bwt[j], "|"])
                print actualResults, correctResults
            numTotal += 1
            del fm
    print numCorrect, "correct.", numTotal - numCorrect, "wrong." 
    

def testIns(string, i, c):
    print "Inserting", c, "at index", i
    fm = fmindex.createFM(string)
    before = fm.bwt
    fm.insBase(i, c)
    afterString = string[:i] + c + string[i:]
    afterfm = fmindex.FMindex(afterString)
    print "After: T'= ", afterString + '$', "BWT'=", afterfm.bwt
    #fm = testDel(fm, i)
    if afterfm.bwt == fm.bwt:
        print "SUCCEEDED"
    else:
        print "FAILED"
    print "Correct result:", afterfm.bwt
    print "Actual results:", fm.bwt
    print " Actual | Correct"
    for j in range(len(afterfm.bwt)):
        correctResults=' '.join([str(afterfm.sa[j]),str(afterfm.isa[j]), sorted(afterfm.bwt)[j], afterfm.bwt[j]])
        if j >= len(fm.bwt):
            actualResults = "         |"
        else:
            actualResults=' '.join([str(fm.sa[j]),str(fm.isa[j]),sorted(fm.bwt)[j],fm.bwt[j], "|"])
        print actualResults, correctResults
    return fm

def testDel(fm, index):
    print "Deleting 'G' from index 2" 
    print fm.bwt
    fm.delBase(index)
    return fm

if __name__ == '__main__':
    main()
