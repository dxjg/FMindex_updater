#! /usr/bin/env python
from __future__ import division
import math
from StringIO import StringIO
import sys
from collections import defaultdict
import random
'''Generate original genomes of set lengths '''


random.seed(5234)
string = ''.join([random.choice('ACGT') for _ in xrange(sys.argv[1])])
print string

