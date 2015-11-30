#! /usr/bin/env python
from __future__ import division
import math
from StringIO import StringIO
import sys
from collections import defaultdict
import random

'''Class which handles BWT/BWM creation as well as LF function
   Methods derived from class notes'''
class BWT():
    EOS = "$"
    self.bwt
    self.bwm

    def __init__(self, t):
        
        
    def rotations(t):
        #the data concat'd to itself, to facilitate rotations
        tt = t * 2
        return [ tt[i:i+len(t)] for i in range(0, len(t)) ]
    def bwm(t):
        return sorted(rotations(t))
    def bwtViaBwm(t):
        ''' Given T, returns BWT(T) by way of the BWM '''
        assert self.EOS not in s, "Provide a T without $"
        t += self.EOS
        return ''.join(map(lambda x: x[-1], bwm(t)))
        


