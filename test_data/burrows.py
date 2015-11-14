#! /usr/bin/env python
from __future__ import division
import math
from StringIO import StringIO
import sys
from collections import defaultdict
import random
def rotations(t):
    tt = t * 2
    return [ tt[i:i+len(t)] for i in range(0, len(t)) ]
def bwm(t):
    return sorted(rotations(t))
def bwtViaBwm(t):
    ''' Given T, returns BWT(T) by way of the BWM '''
    return ''.join(map(lambda x: x[-1], bwm(t)))

string = sys.argv[1] 
bwt = bwtViaBwm(string)
print bwt



