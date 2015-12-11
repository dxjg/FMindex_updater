import sys, os

from hashTracker import hashRangeTracker
from aligner import Aligner
import pprint


pp = pprint.PrettyPrinter()



ref  = "ATCGATCGATCGATCGAACGATCGA"
read = "ATGGATCGATCGATCAA"
read2 =             "TCGAACGATCGC"


a = Aligner(ref)
rt = hashRangeTracker()

rt.setRefLen(len(ref))
rt.setInterval(5) # Split genome into this many blocks
rt.setMinReads(50) # Minimum times a read should overlap a position
rt.setTrigger(100) # How many times to hit a region before reporting

aligned = a.align(read)

changes = []

for _ in range(100):
	ret = rt.addAlignment(read, aligned[1], aligned[0])
	if len(ret) > 0:
		changes +=ret


aligned = a.align(read2)

for _ in range(100):
	ret = rt.addAlignment(read2, aligned[1], aligned[0])
	if len(ret) > 0:
		changes += ret

pp.pprint(changes)








