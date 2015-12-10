import pprint
pp = pprint.PrettyPrinter()

class basicTracker:
	""" Basic tracker of the most common allele """

	minReads = 10 # number of reads minimum at position before even considering it for update
	confidence = 50 # We'll update if we have more than this percent
	refLen = 1000 # Length of the reference geneome
	counts = [] # self.counts for a region
#	alignments = [] # self.alignments for every position


	def setMinReads(self, minR):
		self.minReads = minR


	def setRefLen(self, length):
		self.refLen = length
		self.__init__()


	def __init__(self, refLen, minReads=10, confidence=50):
		self.refLen = refLen
		self.minReads = minReads
		self.confidence = confidence
		self.counts = [{'A':0, 'C':0, 'G':0, 'T':0, 'BASE':None} for _ in range(refLen)]
#		self.alignments = [[]] * self.refLen # Takes a lot of space

	
	def reset(self, refLen=refLen, minReads=minReads, confidence=confidence):
		self.__init__(refLen=refLen, minReads=minReads, confidence=confidence)


	def addAlignment(self, read, alignment, alignmentPos):
		"""Adds an aligntment and increments the counts """
		for i,alignPos in enumerate(alignment):
			idx = alignmentPos + i
#			self.alignments[alignmentPos + i].append(alignPos)
			if len(alignPos) == 1: # This is a sub or a match
				if self.counts[idx]['BASE'] == None:
					# Mark the correct base
					self.counts[idx]['BASE'] = read[i]
				# Increment the counters
				self.counts[idx][alignPos] += 1
			elif alignPos == None:
				if '' in self.counts[idx]:
					self.counts[idx][''] += 1
				else:
					self.counts[idx][''] = 0
			else:
				# Insert
				if alignPos in self.counts[idx]:
					self.counts[idx][alignPos] += 1
				else:
					self.counts[idx][alignPos] = 0
			


	def getUpdateable(self):
		"""
		Return a list of tuples that give the positions
		and change needed for all the positions that have an alternate
		base that is more common, as constrained by the minReads and
		confidence
		"""
		ret = []
		for i,terval in enumerate(self.counts):
			# Check number of reads that have happened
			tot = 0
			for key in terval:
				if key != 'BASE':
					tot += terval[key]
			if tot < self.minReads:
				# Not enough reads at this position
				continue
			m = None # The most common base
			for key in terval:
				if key == 'BASE':
					continue
				if tot != 0 and (100*terval[key])/tot > self.confidence:
					if m == None or terval[key] > terval[m]:
						m = key
			if m != terval['BASE'] and m != None:
				ret.append(tuple((i, m)))
		return ret

