from dynamic_wavelet_tree import *

sequence = 'AAAAACGAAAAAT$'
dwt = DynamicWaveletTree(sequence)

for i in xrange(0, len(sequence)):
    print i
    print dwt.select('A', i)
    print
