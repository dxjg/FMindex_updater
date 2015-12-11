from naive_rank_count import *

sequence = 'CGCGCGCGCGT$'
nrc = NaiveRankCount(sequence)

print sequence
print

for i in xrange(0, len(sequence)):
    print nrc.rank('$', i)
    print nrc.rank('A', i)
    print nrc.rank('C', i)
    print nrc.rank('G', i)
    print nrc.rank('T', i)
    print
