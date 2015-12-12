from dynamic_wavelet_tree import *
from naive_rank_count import *
import random, sys, time

nucleotides = ['A', 'C', 'G', 'T']
genome = sys.stdin.readline()
size = 500000
dynamic_wavelet_tree_times, naive_rank_count_times = [], []

start = time.clock()
dwt = DynamicWaveletTree(genome)
end = time.clock()

print 'Dynamic wavelet tree setup time: ' + str(end - start)
print

for i in xrange(0, 1000):
    start = time.clock()
    dwt.insert(nucleotides[random.randint(0, 3)], random.randint(0, size-1))
    end = time.clock()
    dynamic_wavelet_tree_times.append(end - start)

print 'Dynamic wavelet tree average insert time: ' + str(sum(dynamic_wavelet_tree_times)/len(dynamic_wavelet_tree_times))
print

dynamic_wavelet_tree_times = []

for i in xrange(0, 1000):
    start = time.clock()
    dwt.delete(random.randint(0, size-1))
    end = time.clock()
    dynamic_wavelet_tree_times.append(end - start)

print 'Dynamic wavelet tree average delete time: ' + str(sum(dynamic_wavelet_tree_times)/len(dynamic_wavelet_tree_times))
print

dynamic_wavelet_tree_times = []

for i in xrange(0, 1000):
    start = time.clock()
    dwt.rank(nucleotides[random.randint(0, 3)], random.randint(0, size-1))
    end = time.clock()
    dynamic_wavelet_tree_times.append(end - start)

print 'Dynamic wavelet tree average rank time: ' + str(sum(dynamic_wavelet_tree_times)/len(dynamic_wavelet_tree_times))
print


start = time.clock()
nrc = NaiveRankCount(genome)
end = time.clock()

print 'Naive rank/count data structure setup time: ' + str(end - start)
print

for i in xrange(0, 1000):
    start = time.clock()
    nrc.insert(nucleotides[random.randint(0, 3)], random.randint(0, size-1))
    end = time.clock()
    naive_rank_count_times.append(end - start)

print 'Naive rank/count average insert time: ' + str(sum(naive_rank_count_times)/len(naive_rank_count_times))
print

naive_rank_count_times = []

for i in xrange(0, 1000):
    start = time.clock()
    nrc.delete(random.randint(0, size-1))
    end = time.clock()
    naive_rank_count_times.append(end - start)

print 'Naive rank/count average delete time: ' + str(sum(naive_rank_count_times)/len(naive_rank_count_times))
print

naive_rank_count_times = []

for i in xrange(0, 1000):
    start = time.clock()
    nrc.rank(nucleotides[random.randint(0, 3)], random.randint(0, size-1))
    end = time.clock()
    naive_rank_count_times.append(end - start)

print 'Naive rank/count average rank time: ' + str(sum(naive_rank_count_times)/len(naive_rank_count_times))
print
