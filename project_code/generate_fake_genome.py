import sys, random

nucleotides = ['A', 'C', 'G', 'T']
size = int(sys.stdin.readline())
genome = ''

for i in xrange(0, size):
   genome += nucleotides[random.randint(0, 3)]

genome += '$'

sys.stdout.write(genome)
