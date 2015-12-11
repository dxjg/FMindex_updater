import sys, os

from hashTracker import hashRangeTracker
from aligner import Aligner
import pprint


pp = pprint.PrettyPrinter()



ref = "ATCGATCGATCGATCGAACGATCGA"
read = "TCGGTCGATCGATCGAAC"
a = Aligner(ref)

rt = hashRangeTracker()
rt.setRefLen(len(ref))
rt.setInterval(len(ref))

aligned = a.align(read)
print(aligned)

for _ in range(100):
	ret = rt.addAlignment(read, aligned[1], aligned[0])
	if len(ret) > 0:
		pp.pprint(ret)







