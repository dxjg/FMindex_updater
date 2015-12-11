#! /usr/bin/env python
from __future__ import division
import math
from StringIO import StringIO
import sys
from collections import defaultdict
import random
import fmindex


output = []
n = '{: <'+str(len(str(sys.argv[1])))+'}'
def main():
    #Genome from paper is: CTCTGC 
  #  findLong(int(sys.argv[1]))
   # sys.exit(0) 
    string = sys.argv[1]
    if '$' in string:
        print "Don't include $ in genome"
        sys.exit(0)
    
    
    fm = fmindex.createFM(string)
    if fm.getInverse() != string:
        print "LF function does not correctly inverse BWT. Not equal", string, fm.getInverse()
        sys.exit(0)
    if len(sys.argv) == 4:
        fm = testIns(string, int(sys.argv[3]), sys.argv[2])
        fm = testDel(string, int(sys.argv[3]), sys.argv[2])
    else:
        stressTest(string)
    
def findLong(n):
    #random.seed()
    string = ''.join([random.choice('ACGT') for _ in xrange(n)])
    stressTest(string)
    return 


def stressTest(string): 
    numCorrect = 0
    numTotal = 0
    for i in range(0, len(string) - 1):
        for c in "ACGT":
            fm = fmindex.createFM(string)
#            print "Testing i =", i, ", c =,", c
#            print "Before: T =", string +'$ ', "BWT =", fm.bwt
#            afterString = string[:i] + c + string[i:]
            afterString = string[:i] + string[i+ 1]
            afterfm = fmindex.FMindex(afterString)
#            print "After: T'= ", afterString + '$', "BWT'=", afterfm.bwt
            fm = testDel(string, i, c)
            if afterfm.bwt == fm.bwt:
                numCorrect+=1
            numTotal+=1
    print '\n'.join(output)
    print string
    print  numCorrect,"PASS;",numTotal-numCorrect,"FAIL;","SCORE:",float(numCorrect)/float(numTotal)*100

            
    

def testIns(string, i, c):
    fm = fmindex.createFM(string)
    before = fm.bwt
    fm.insBase(i, c)
    afterString = string[:i] + c + string[i:]
    afterfm = fmindex.FMindex(afterString)
    
    if afterfm.bwt == fm.bwt:
        output.extend(["PASS: " + c + " " + n.format(str(i))])
    else:
        output.extend(["FAIL: " + c + " " + n.format(str(i))])
    '''print "Correct result:", afterfm.bwt
    print "Actual results:", fm.bwt
    print " Actual | Correct"
    for j in range(len(afterfm.bwt)):
        correctResults=' '.join([str(afterfm.sa[j]),str(afterfm.isa[j]), sorted(afterfm.bwt)[j], afterfm.bwt[j]])
        if j >= len(fm.bwt):
            actualResults = "         |"
        else:
            actualResults=' '.join([str(fm.sa[j]),str(fm.isa[j]),sorted(fm.bwt)[j],fm.bwt[j], "|"])
        print actualResults, correctResults
    '''
    return fm

def testDel(string, i, c):
    fm = fmindex.createFM(string)
    before = fm.bwt
    fm.delBase(i)
    afterString = string[:i] + c + string[i:]
    afterfm = fmindex.FMindex(afterString)
    
    if afterfm.bwt == fm.bwt:
        output.extend(["PASS: " + c + " " + n.format(str(i))])
    else:
        output.extend(["FAIL: " + c + " " + n.format(str(i))])
    return fm

if __name__ == '__main__':
    main()
