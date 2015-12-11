import sys, os

from hashTracker import hashTracker
from aligner import Aligner
import pprint


pp = pprint.PrettyPrinter()



ref = "ATCG"
a = Aligner(ref)
pp.pprint(a._align("ATCG"))







