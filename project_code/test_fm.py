#! /usr/bin/env python
from __future__ import division
import math
from StringIO import StringIO
import sys
from collections import defaultdict
import random
import fmindex


def main():
    string = "CTCTGC"
    fm = fmindex.createFM(string)
    print string, fm.bwt
    import pprint
    print "Count array"
    pprint.pprint(fm.count)
    print    "occurance array"
    for c in sorted(fm.occ.keys()):
        result = c + ": "
        for i in range(len(fm.bwt)):
            result +=  str(fm.occ[c][i]) + ", "
        print result
    print "suffix array indexes"
    for i in range(len(fm.bwt)):
        print fm.sa[i], sorted(fm.bwt)[i], fm.bwt[i]
    fm._insertIntoBWT(2, "G")        
    

if __name__ == '__main__':
    main()
