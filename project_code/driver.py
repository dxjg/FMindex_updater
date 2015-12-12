"""
December 11, 2015
Computational Genomics Final Project
Ravi Gaddipati
Craig Hennessy
Gwen Hoffmann
David Gong

Main driver program. Reads a list of reads, aligns to the provided reference
and aligns it. Required changes are kept track of, and the index is updated
when conditions are met.
"""

import sys
import timeit

from hashTracker import hashRangeTracker
from aligner import Aligner
import pprint

pp = pprint.PrettyPrinter()

def printInfo():
	print("\n------------------------------------Usage-----------------------------------------")
	print("python driver.py [reference] <reads> <Interval> <MinReads> <TriggerPoint> <confidence>")
	print("[reference] and <reads> are required.")
	print("Outputs the updated reference on stdout.")
	print("<> params can be comma seperated lists, all combinations will be run")
	print("----------------------------------------------------------------------------------\n")


def makeChange(aligner, change):
	""" Updates the aligner with the given change"""
	if len(change[1]) == 0:
		aligner.delBase(change[0])
	elif len(change[1]) == 1:
		aligner.subBase(change[0], change[1])
	else:
		aligner.insBase(change[0], change[1][:-1])

def main():
	# Get command line arguments
	if len(sys.argv) < 3:
		printInfo()
		exit(1)


	ref = ""
	refLen = 0
	refFile = sys.argv[1]
	READFILE = sys.argv[2].strip().split(',')
	with open(refFile) as fi:
		ref = fi.read().strip()
		refLen = len(ref)

	INTERVAL = [refLen]
	MINREADS = [10]
	TRIGGERPOINT = [10]
	CONFIDENCE = [50]

	# Convert args into a list of args
	if len(sys.argv) > 3:
		INTERVAL = [int(i) for i in sys.argv[3].strip().split(',')]
	if len(sys.argv) > 4:
		MINREADS = [int(i) for i in sys.argv[4].strip().split(',')]
	if len(sys.argv) > 5:
		TRIGGERPOINT = [int(i) for i in sys.argv[5].strip().split(',')]
	if len(sys.argv) > 6:
		CONFIDENCE = [int(i) for i in sys.argv[6].strip().split(',')]

	print("time \t Read File \t num changes \t interval \t minReads \t triggerPoint \t confidence")

	# Iterate through all combinations of parameters
	for readFile in READFILE:
		for interval in INTERVAL:
			for minReads in MINREADS:
				for triggerPoint in TRIGGERPOINT:
					for confidence in CONFIDENCE:
						start_time = timeit.default_timer() # Times the block with alignment
						# Init the alignment tracker and aligner
						a = Aligner(ref)
						rt = hashRangeTracker()
						rt.setRefLen(refLen)
						rt.setInterval(interval) # Split genome into this many blocks
						rt.setMinReads(minReads) # Minimum times a read should overlap a position
						rt.setTrigger(triggerPoint) # How many times to hit a region before reporting
						rt.setConfidence(confidence)

						allChanges = []
						with open(readFile) as readsFi:
							for read in readsFi:
								read = read.strip()
								if read[0] == '#':
									# Comment line
									continue

								elapsed_time = timeit.default_timer() - start_time
								aligned = a.align(read)
								start_time = timeit.default_timer()

								changes = rt.addAlignment(read, aligned[1], aligned[0])
								if len(changes) > 0:
									# We have some changes to make
									allChanges += changes
									for c in changes:
										makeChange(a, c)
										# ref = ref[:c[0]] + c[1] + ref[c[0] + 1:] # to update ref w/out the index
									#a = Aligner(ref)

							# Get the remaining updates
							changes = rt.flush()
							if len(changes) > 0:
								allChanges += changes
								for c in changes:
									makeChange(a, c)
									# ref = ref[:c[0]] + c[1] + ref[c[0] + 1:] # to update ref w/out the index

						elapsed_time += timeit.default_timer() - start_time
						ref = a.getRef()

						print(str(elapsed_time) + " \t " + readFile + " \t " + str(len(allChanges)) + " \t " + str(interval) + " \t " + str(minReads) + " \t " + str(triggerPoint) + " \t " + str(confidence))
	print(ref)


if __name__ == "__main__":
	main()




