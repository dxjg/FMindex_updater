from dynamic_wavelet_tree import *

sequence = 'CGT'
dwt = DynamicWaveletTree(sequence)

for i in xrange(1, len(sequence)):
#    print dwt.select('A', i)
#    print dwt.select('C', i)
#    print dwt.select('G', i)
#    print dwt.select('T', i)
    print dwt.select('$', i)
    print

dwt.insert('A', 2)
dwt.insert('A', 0)
dwt.insert('A', 10)
dwt.insert('$',1)

for i in xrange(1, len(sequence)):
#    print dwt.select('A', i)
#    print dwt.select('C', i)
#    print dwt.select('G', i)
#    print dwt.select('T', i)
    print dwt.select('$', i)
    print

print dwt.select('$', 1)
dwt.delete(1)
print dwt.select('$', 1)
