from dynamic_wavelet_tree import *
from naive_rank_count import *
import random, sys, time

nucleotides = ['A', 'C', 'G', 'T']
genome = sys.stdin.readline()
dynamic_wavelet_tree_times, naive_rank_count_times = [], []

start = time.clock()
dwt = DynamicWaveletTree(genome)
end = time.clock()

print 'Dynamic wavelet tree setup time: ' + str(end - start)

start = time.clock()
nrc = NaiveRankCount(genome)
end = time.clock()

print 'Naive rank/count data structure setup time: ' + str(end - start)

for i in xrange(0, 1000):
    start = time.clock()
    dwt.insert(nucleotides[random.randint(0, 3)], random.randint(0, 5000))
    end = time.clock()
    dynamic_wavelet_tree_times.append(end - start)

print

print 'Dynamic wavelet tree average insertion time: ' + str(sum(dynamic_wavelet_tree_times)/len(dynamic_wavelet_tree_times))

for i in xrange(0, 1000):
    start = time.clock()
    nrc.insert(nucleotides[random.randint(0, 3)], random.randint(0, 5000))
    end = time.clock()
    naive_rank_count_times.append(end - start)

print 'Naive rank/count data structure  average insertion time: ' + str(sum(naive_rank_count_times)/len(naive_rank_count_times))

dwt.print_count_table()
print dwt.rank('A', 20000)
