from dynamic_wavelet_tree import *

sequence = 'GG'
dwt = DynamicWaveletTree(sequence)
dwt.insert('T', 2)
print dwt.rank('T', 2)
dwt.print_count_table()
print dwt.select('T', 1)
'''
print 'Original sequence: ' + sequence
print

print 'Counts:'
print dwt.count('$')
print dwt.count('A')
print dwt.count('C')
print dwt.count('G')
print dwt.count('T')
print

print 'Insert 4 A\'s at index 0:'
dwt.insert('A', 0)
dwt.insert('A', 0)
dwt.insert('A', 0)
dwt.insert('A', 0)

print 'Counts:'
print dwt.count('$')
print dwt.count('A')
print dwt.count('C')
print dwt.count('G')
print dwt.count('T')
print

print 'Delete the first 4 characters:'
dwt.delete(0)
dwt.delete(0)
dwt.delete(0)
dwt.delete(0)

print 'Counts:'
print dwt.count('$')
print dwt.count('A')
print dwt.count('C')
print dwt.count('G')
print dwt.count('T')
print

print 'Ranks for T:'
print dwt.rank('T', 0)
print dwt.rank('T', 1)
print dwt.rank('T', 2)
print dwt.rank('T', 3)
print

print 'Selects for T:'
print dwt.select('T', 0)
print dwt.select('T', 1)
'''
