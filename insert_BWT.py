# Computational Genomics
# Final Project

import sys

def move(j, j_prime, bwt):
	bwt.insert(j_prime, bwt[j])
	if j < j_prime:
		bwt.pop([j])
	elif j > j_prime:
		bwt.pop([j+1])
	return

def one_b(suff_array, bwt, i, ch, char_counts):
	char_counts[ch] += 1 #char_counts is map from character to number of times character occurs
	ch_index = suff_array.index(i) #i = index of inserted character in text, ch_index = index of char in F of bwt
	overwrote_ch = bwt[ch_index]
	bwt[ch_index] = ch
	return overwrote_ch, bwt, char_counts
	
def two_a(bwt, overwrote_ch):
	insert_index = partial_sums_index(overwrote_ch) # needs to be written
	bwt.insert(insert_index, overwote_ch)
	return bwt
	
def two_b(suff_array, bwt, i): 
	j = suff_array.index(i - 1)
	ch_index = suff_array.index(i)
	j_prime = LF(bwt, char_counts, checkpoints, ch_index) # needs to be written
	while j != j_prime:
		new_j = LF(bwt, char_counts, checkpoints, j)
		bwt = move(j, j_prime, bwt)
		j = new_j
		j_prime = LF(bwt, char_counts, checkpoints, j_prime)
	return bwt

#random test 
overwrote_ch, bwt, char_counts = one_b([0, 1, 2, 3, 4], ['G', 'A', 'T', 'C', 'A'], 2, 'G', { 'G':1, 'A':2, 'T':1, 'C':1})
bwt = two_a(bwt, overwrote_ch)
bwt = two_b([0, 1, 2, 3, 4], ['G', 'A', 'T', 'C', 'A'], 2)

		
	