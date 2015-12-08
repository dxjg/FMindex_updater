
from fmindex import FMindex
import fmindex
import sys
import copy


class Aligner(object):
	def __init__(self, genome):
		self.fm = fmindex.createFM(genome)

	def _setTemplate(self, genome):
		self.fm = fmindex.createFM(genome) #also fm.count, fm.occ, fm.sa

	def _recurse_query_fm(self, word, word_index, fm_index):
		prev_index = self.fm._lf(fm_index)
		word_index -= 1
		#print "query:", word, "w_index", word_index, "fm_ind", fm_index, "w[ind]", word[word_index],"bwt[ind]", self.fm.bwt[prev_index]
		if word[word_index] == self.fm.bwt[fm_index]:
			if word_index > 0:
				return self._recurse_query_fm(word, word_index, prev_index)
			else:
				return self.fm.sa[fm_index] - 1
		else:
			#print "not found", word, word_index, fm_index, word[word_index], self.fm.bwt[prev_index]
			return -1

	def _query_fm(self, word):
		word_index = len(word) - 1
		char = word[word_index]
		chars = ['A', 'C', 'G', 'T'] # because count gets # chars before and including
		char_ind = chars.index(char)
		ch = len(self.fm.bwt)
		if char_ind < 3:
			ch = self.fm.count[chars[char_ind + 1]]
		fm_start =  self.fm.count[char]
		fm_end =  ch
		#print fm_start, fm_end, word
		pos = -1
		i = fm_start
		while (pos == -1) and (i < fm_end):
			#print "i", i
			pos = self._recurse_query_fm(word, word_index, i)
			i += 1
		return pos #returns -1 if not found

	def _edit_str(self, edit_list, word, read):
		#TODO
		edits = []
		for x in range(0, len(read)):
			if x in edit_list:
				edits.append(edit_list[x])
			else:
				edits.append(read[x])
		return edits

	def _findNeighbor(self, wlist, read, word, d, n, position, edit_list):
		letters = ['A', 'C', 'G', 'T']
		for x in letters:
			word2 = word[0:position] + x + word[position + 1:] # create substitutions
			edit_list2 = copy.deepcopy(edit_list)
			if word2 not in wlist:
				wlist.append(word2)
				pos = self._query_fm(word2)
				edit_list2[position] = x
 				if pos > -1:
 					#print pos, word2, "R"
					return pos, word2, edit_list2
			if (n <= d):
				#print n
				return self._findNeighbor(wlist, read, word2, d, n + 1, 0, edit_list2)

			word3 = word[0:position] + word[position + 1:] # create deletions
			edit_list3 = copy.deepcopy(edit_list)
			if word3 not in wlist:
				wlist.append(word3)
				pos = self._query_fm(word3)
				edit_list3[position] = None
				if pos > -1:
					#edit_list[position] = "D"
					#print pos, word3, "D"
					return pos, word3, edit_list3
			if (n <= d):
				return self._findNeighbor(wlist, read, word3, d, n + 1, 0, edit_list3)

			word4 = word[0:position] + x + word[position:] # create insertions
			edit_list4 = copy.deepcopy(edit_list)
			if word4 not in wlist:
				wlist.append(word4)
				#print word4
				pos = self._query_fm(word4)
				edit_list4[position] = x + word[position]
				if pos > -1:
					#edit_list[position] = "I"
					#print pos, word4, "I"
					return pos, word4, edit_list4
			if (n <= d):
				return self._findNeighbor(wlist, read, word4, d, n + 1, 0, edit_list4)
		if (position < len(word)):
			return self._findNeighbor(wlist, read, read, d, n, position + 1, edit_list)		
		return -1, '', {}

	def _align(self, read):
		pos = self._query_fm(read)
		if pos > -1:
			edits = self._edit_str({}, read, read)
		else:
			wlist = []
			wlist.append(read)
			edit_list = {}
			pos, word, edit_list = self._findNeighbor(wlist, read, read, len(read), 1, 0, edit_list)
			if pos > -1:
				edits = self._edit_str(edit_list, word, read)
			else:
				edits = list(read)

		return pos, edits

	def _subBase(self, pos, char):
		#TODO
		pos = pos #get rid of indent error

	def _insBase(self, pos, char):
		fm._insertIntoBWT(pos, char)

	def _delBase(self, pos, base):
		#TODO
		pos = pos