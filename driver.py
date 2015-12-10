from tracker import basicTracker
from rangeTracker import rangeTracker
import pprint
pp = pprint.PrettyPrinter()

tracker = basicTracker(refLen=5, minReads=0)

test = ['G','A','A','A']
tracker.addAlignment('GAAA', ['G','A','','A'], 0)
tracker.addAlignment('GAAA', ['G','A','','A'], 0)
tracker.addAlignment('GAAA', ['G','A','','A'], 0)
tracker.addAlignment('GAAA', ['G','A','A','A'], 0)

tracker.getUpdateable()

rt = rangeTracker(4)
rt.setInterval(5)
rt.setTrigger(3)
rt.setMinReads(2)

for i in range(10):
	pp.pprint(rt.addAlignment('GAAA', ['G','A','C','A'], 0))


