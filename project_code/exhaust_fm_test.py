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
    findLong(int(sys.argv[1]))
    sys.exit(0) 
    
def findLong(n):
    #random.seed()
    string = ''.join([random.choice('ACGT') for _ in xrange(n)])
    print string
    stressTest(string)
    return 


def stressTest(string): 
    numCorrect = 0
    numTotal = 0
    for i in range(0, len(string) + 1):
        for c in "ACGT":
            fm = fmindex.createFM(string)
            afterString = string[:i] + c + string[i:]
            afterfm = fmindex.FMindex(afterString)
            fm = testIns(string, i, c)
            if afterfm.bwt == fm.bwt:
                numCorrect+=1
            numTotal+=1
    #print '\n'.join(output)
    #print string
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
    return fm


if __name__ == '__main__':
    main()
