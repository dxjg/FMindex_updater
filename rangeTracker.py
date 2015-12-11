import pprint
pp = pprint.PrettyPrinter()



class basicTracker:
	""" Basic tracker of the most common allele, backed by a list """

	minReads = 10 # number of reads minimum at position before even considering it for update
	confidence = 50 # We'll update if we have more than this percent
	refLen = 1000 # Length of the reference geneome
	counts = [] # self.counts for a region
#	alignments = [] # self.alignments for every position


	def setMinReads(self, minR):
		""" Minimum number of reads before considering an update"""
		self.minReads = minR


	def setRefLen(self, length):
		""" Stores a list this long to track variants"""
		self.refLen = length
		self.__init__(length)


	def __init__(self, refLen, minReads=10, confidence=50):
		self.refLen = refLen
		self.minReads = minReads
		self.confidence = confidence
		self.counts = [{'A':0, 'C':0, 'G':0, 'T':0, 'BASE':None} for _ in range(refLen)]
#		self.alignments = [[]] * self.refLen # Takes a lot of space

	
	def reset(self):
		self.__init__(refLen=self.refLen, minReads=self.minReads, confidence=self.confidence)


	def addAlignment(self, read, alignment, alignmentPos):
		"""Adds an aligntment and increments the counts.
		Insertions are represented as deletions in the reference,
		deletetions are represented as insertions in the reference"""
		for i,alignPos in enumerate(alignment):
			idx = alignmentPos
			for c in range(i):
				idx += len(alignment[c])
#			self.alignments[alignmentPos + i].append(alignPos)
			if len(alignPos) == 1: # This is a sub or a match
				if self.counts[idx]['BASE'] == None:
					# Mark the correct base
					self.counts[idx]['BASE'] = read[i]
				# Increment the counters
				if i == 0 or alignment[i - 1] != '':
					# To prevent double counting w/dels
					self.counts[idx][alignPos] += 1
			elif alignPos == '':
				#deletion
				if i == len(alignment) - 1 or alignment[i+1] != '':
					inv = alignment[i+1]
					curr = i
					# Get the str that would need to be inserted into the ref
					while curr >= 0 and alignment[curr] == '':
						inv = read[curr] + inv
						curr -= 1

					if inv in self.counts[idx]:
						self.counts[idx][inv] += 1
					else:
						self.counts[idx][inv] = 0
			else:
				# Insert aka delete from ref
				for ins in range(len(alignPos) - 1):
					if '' in self.counts[idx + ins]:
						self.counts[idx + ins][''] += 1
					else:
						self.counts[idx + ins][''] = 0
	

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
				# See if we have enough confidence
				if tot != 0 and (100 * terval[key]) / tot > self.confidence:
					if m == None or terval[key] > terval[m]:
						m = key
			if m != terval['BASE'] and m != None:
				ret.append(tuple((i, m)))
		return ret



class rangeTracker:
	"""
	This uses basicTrackers to split up the neccessary changes into chunks.
	This way we can update group by group, and spend less time
	trying to figure out which updates go together when actually
	updating the index
	"""

	refLen = 10
	interval = 10
	counts = []
	trackers = []
	triggerPoint = 100


	def setInterval(self, interval):
		""" The overall length is split in ranges so we can update a block at a time"""
		self.interval = interval
		self.__init__(self.refLen)


	def setRefLen(self, length):
		""" Reference genome length"""
		self.refLen = length


	def setTrigger(self, trig):
		""" When should we determine if there are valid updates?"""
		self.triggerPoint = trig


	def setMinReads(self, num):
		""" Set the minimum number of reads before considering a change valid"""
		for t in self.trackers:
			t.setMinReads(num)


	def __init__(self, refLen):
		self.counts = [0 for _ in range(int(self.refLen/self.interval)+1)]
		self.trackers = [basicTracker(self.interval) for _ in self.counts]
		for t in self.trackers:
			t.setRefLen(self.interval)
		self.refLen = refLen


	def addAlignment(self, read, alignment, alignmentPos):
		""" Adds an alignment to the correct interval tracker"""
		ret = []
		idx = int(alignmentPos/self.interval)
		self.counts[idx] += 1
		self.trackers[idx].addAlignment(read, alignment, alignmentPos)
		if self.counts[idx] >= self.triggerPoint:
			ret = self.trackers[idx].getUpdateable()
			self.trackers[idx].reset()
			self.counts[idx] = 0
		return ret


if __name__ == '__main__':

	rt = rangeTracker(160)
	rt.setInterval(160)
	rt.setTrigger(5)	
	rt.setMinReads(2)

	with open('test_data/x.fa') as fi:
		ref = fi.readline().strip()
		mod = fi.readline().strip()
		for align in fi:
			splitStr = align.split(',')
			ret = rt.addAlignment(splitStr[1].strip(), list(splitStr[1].strip()), int(splitStr[0]))
			if len(ret) > 0:
				pp.pprint(ret)

