
import sys
from aligner import Aligner
import random
import time


string = "ACTCTGCTTTAG"
a = Aligner(string)


#test exact match
pos, edits = a.align("TCTGC")
assert pos == 2
#print pos, edits

#test insertion
pos, edits = a.align("ACTTGC")
#print pos, edits
assert pos == 0

#test replacement
pos, edits = a.align("TACTT")
#print pos, edits
assert pos == 4

#test deletion
pos, edits = a.align("TCTTT")
#print pos, edits
assert pos == 6

#test deletion and substitution
pos, edits = a.align("AAA")
#print pos, edits
assert pos == 9

#test insert and delete
pos, edits = a.align("TCTGTTTC")
#print pos, edits
assert pos == 2

#test 2 deletions and substitution
pos, edits = a.align("AAAA")
#print pos, edits
assert pos == 9

string = "TCAGATTACG"
a = Aligner(string)
pos, edits = a.align("TCAGTACG")
#print pos, edits
assert pos == 0

string = "TCAGATGACG"
a = Aligner(string)
pos, edits = a.align("TCAGGACG")
assert pos == 0
#print pos, edits

#string = "TCAGATGACGTCAGATGACGTCAGATGACGTCAGATGACGTCAGGACGTCAGGACGTCAGATTACGTCAGATTACG"
#a = Aligner(string)
#pos, edits = a.align("TGACGTCAGATGACGTCAGCTGACGGCAGGA")
#assert pos == 0
#print pos, edits

'''
data = []
n = 500
genome = ''.join([random.choice('ACGT') for _ in xrange(n)])
a = Aligner(genome)
i = 5
while i < 50:
	r1 = random.randint(0, n-i)
	read = genome[r1:r1+i]
	r2 = random.randint(0,i)
	read = read[0:r2] + random.choice('ACGT') + read[r2:]
	t_before = time.clock()
	pos, edits = a.align(read)
	t_after = time.clock()
	data.append([i, t_after-t_before, r1, r2])
	i += 5

fh = open("test_aligner_data.txt", "w")
fh.write("Test reads of increasing length with 1 insertion, genome length 500\n")
for x in data:
	string = str(x[0]) + "\t" + str(x[1]) + "\t" + str(x[2]) + "\t" + str(x[3]) + "\n" 
	fh.write(string)
'''
'''
data = []
n = 100
genome = ''.join([random.choice('ACGT') for _ in xrange(n)])
a = Aligner(genome)
i = 10
r1 = random.randint(0, n-i)
read = genome[r1:r1+i]
for i in range(0, 3):
	r2 = random.randint(0,10)
	read = read[0:r2] + random.choice('ACGT') + read[r2:]
	print r2, read
	t_before = time.clock()
	pos, edits = a.align(read)
	t_after = time.clock()
	data.append([i, t_after-t_before])

fh = open("test_aligner_data.txt", "w")
fh.write("Test reads with increasing number of edits\n")
for x in data:
	string = str(x[0]) + "\t" + str(x[1]) + "\n" 
	fh.write(string)

'''
'''
data = []
n = 300
while n < 2000:
	genome = ''.join([random.choice('ACGT') for _ in xrange(n)])
	r1 = random.randint(0, n-20)
	read = genome[r1:r1+20]
	r2 = random.randint(0,20)
	read = read[0:r2] + "A" + read[r2:]
	a = Aligner(genome)
	t_before = time.clock()
	pos, edits = a.align(read)
	t_after = time.clock()
	data.append([n, t_after-t_before])
	n += 200

fh = open("test_aligner_data.txt", "w")
fh.write("Test alignment with increasing genome size\n")
for x in data:
	string = str(x[0]) + "\t" + str(x[1]) + "\n" 
	fh.write(string)
'''