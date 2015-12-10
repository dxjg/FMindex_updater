import pprint
from tracker import basicTracker
pp = pprint.PrettyPrinter()

class rangeTracker:

	refLen = 0
	interval = 100
	counts = []
	trackers = []
	triggerPoint = 100

	def setInterval(self, interval):
		self.interval = interval
		self.__init__(self.refLen)

	def setRefLen(self, length):
		self.refLen = length

	def setTrigger(self, trig):
		self.triggerPoint = trig

	def setMinReads(self, num):
		for t in self.trackers:
			t.setMinReads(num)

	def __init__(self, refLen):
		self.counts = [0 for _ in range(int(self.refLen/self.interval)+1)]
		self.trackers = [basicTracker(refLen=self.interval) for _ in self.counts]
		self.refLen = refLen

	def setRefLen(length):
		self.refLen = length

	def addAlignment(self, read, alignment, alignmentPos):
		ret = []
		idx = int(alignmentPos/self.interval)
		self.counts[idx] += 1
		self.trackers[idx].addAlignment(read, alignment, alignmentPos)
		if self.counts[idx] >= self.triggerPoint:
			ret = self.trackers[idx].getUpdateable()
			self.trackers[idx].reset()
			self.counts[idx] = 0
		return ret

