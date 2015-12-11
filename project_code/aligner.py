
from fmindex import FMindex
import fmindex
import sys
import copy
import numpy


class Aligner(object):
	def __init__(self, genome):
		self.fm = fmindex.createFM(genome)

	def _setTemplate(self, genome):
		self.fm = fmindex.createFM(genome) #also fm.count, fm.occ, fm.sa

	def _recurse_query_fm(self, word, word_index, fm_index):
		# recursively do LF to find match in fm index
		prev_index = self.fm._lf(fm_index)
		word_index -= 1
		if word[word_index] == self.fm.bwt[fm_index]:
			if word_index > 0:
				return self._recurse_query_fm(word, word_index, prev_index)
			else:
				return self.fm.sa[fm_index] - 1
		else:
			return -1

	def _query_fm(self, word):
		# get range for word's last character in bwt
		word_index = len(word) - 1
		char = word[word_index]
		chars = ['A', 'C', 'G', 'T']
		if char in chars:
			char_ind = chars.index(char)
		else:
			print "Invalid Character. Please use only A, C, G, or T."
			exit()
		ch = len(self.fm.bwt)
		if char_ind < 3:
			ch = self.fm.count(chars[char_ind + 1])
		fm_start =  self.fm.count(char) # start of char's character range
		fm_end = ch # end of character range
		pos = -1
		# check for match with all characters in range
		i = fm_start
		while (pos == -1) and (i < fm_end):
			pos = self._recurse_query_fm(word, word_index, i)
			i += 1
		return pos #returns -1 if not found

	#Adapted from code provided in class. Cost function assigning 0 to match,
   	#1 to transition, 1 to transversion, and 1 to a gap """
	def _cost(self, xc, yc):
		if xc == yc:
			return 0 # match
		return 1 # substitution/deletion/insertion

	def _globalAlignment(self, x, y, s):
    	#Adapted from code provided in class and at http://bit.ly/CG_DP_Global. 
    	#Calculates global alignment value of sequences x and y using dynamic 
    	#programming.  Returns global alignment value.
	    D = numpy.zeros((len(x)+1, len(y)+1), dtype=int)
	    for j in range(1, len(y)+1):
	        D[0, j] = D[0, j-1] + s('-', y[j-1])
	    for i in range(1, len(x)+1):
	        D[i, 0] = D[i-1, 0] + s(x[i-1], '-')
	    for i in range(1, len(x)+1):
	        for j in range(1, len(y)+1):
	            D[i, j] = min(D[i-1, j-1] + s(x[i-1], y[j-1]), # diagonal
	                          D[i-1, j  ] + s(x[i-1], '-'),    # vertical
	                          D[i  , j-1] + s('-',    y[j-1])) # horizontal
	    return D

	def _edit_str(self, word, read):
		#create list of all edits by doing global alignment and traceback
		edits = []
		D = self._globalAlignment(word, read, self._cost) # get alignment matrix
		i = len(D)-1
		j = len(D[0])-1
		while i > 0 and j > 0: # traceback to get edit string
			min_val = min(D[i-1, j-1], D[i-1, j],  D[i, j-1])
			if D[i-1, j-1] == min_val: # substitutions/matches
				edits.insert(0, word[i-1])
				i -= 1
				j -= 1
			elif D[i-1, j] == min_val: # insertions
				edits[0] = word[i-1] + edits[0]
				i -= 1
			elif D[i, j-1] == min_val: # deletions
				edits.insert(0, '')
				j -= 1
		return edits

	def _findNeighbor(self, wlist, read, word, position):
		letters = ['A', 'C', 'G', 'T']
		for x in letters:
			word2 = word[0:position] + x + word[position + 1:] # create substitutions
			if word2 not in wlist:
				wlist.append(word2)

			word3 = word[0:position] + word[position + 1:] # create deletions
			if word3 not in wlist:
				wlist.append(word3)

			word4 = word[0:position] + x + word[position:] # create insertions
			if word4 not in wlist:
				wlist.append(word4)

	def _neighbor_control(self, read):
		wlist = []
		wlist.append(read)
		n = 1 # n = number of edits
		pos = -1 # pos = alignment position in reference genome
		word = read
		ind1 = 0
		while n < len(read) and pos < 0:
			ind2 = len(wlist)
			for i in range(ind1, len(wlist)): # generate neighbors within i edit distance
				for p in range(0, len(wlist[i])):
					self._findNeighbor(wlist, read, wlist[i], p)
			ind1 = ind2
			for x in range(ind2, len(wlist)): # check if neighbors are in FM index
				pos = self._query_fm(wlist[x])
				if pos > -1:
					return pos, wlist[x]
			n += 1 # if not found, add another edit
		return -1, "X" * len(read)

	def _align(self, read):
		pos = self._query_fm(read) #check if read is in FM index
		if pos > -1:
			edits = self._edit_str(read, read)
		else: # start checking for neighbor matches
			pos, word = self._neighbor_control(read)
			if pos > -1:
				edits = self._edit_str(word, read)
			else:
				edits = list(read)

		return pos, edits

	def _subBase(self, pos, char):
		fm._subBase(pos, char)

	def _insBase(self, pos, char):
		fm._insBase(pos, char)

	def _delBase(self, pos, base):
		fm._insBase(pos, char)