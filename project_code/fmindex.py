# -*- coding: utf-8 -*-
import sys
import dynamic_wavelet_tree

def createFM(genome):
    return FMindex(genome)

class FMindex(object):
    def __init__(self, genome):
        genome += "$"
        self.bwt = self._createBWT(genome)
        self.wave = dynamic_wavelet_tree.DynamicWaveletTree(self.bwt)
        self.sa, self.isa = self._createSA(genome)
        self.state = "IDLE"

    #recreate the genome (minus $) from the bwt
    def getInverse(self):
        #Find the row in L with '$'. We'll LF backwards to get the genome
        result = []
        lf = 0
        while self.bwt[lf] != '$':
            result.append(self.bwt[lf])
            lf = self._lf(lf)
        return ''.join(reversed(result))


    #Perform the standard LF mapping
    def _lf(self, i):
        #if in the middle of editing, use the computed lf value
        #if the index happens to be lf_after, which is normally just ahead
        if self.state != "IDLE" and i == self.lf_after:
            return self.lf_before
        s = self.bwt[i]
        c = self.count(s)
        r = self.rank(s, i)
        #Modifying the bwt otherwise
        if self.state != "IDLE":
            #if are reordering or just about to:
            if self.state == "REORDERING" or (self.state == "INSERTING" and self.current_modif == 0):
                s2 = self.bwt[self.lf_after]
                templf = self.count(s2) + self.rank(s2, self.lf_after)
                result = c + r
                #handle the case where result is between two real lfs
                if result <= templf and result >= self.lf_before:
                    result += 1
                elif result >= templf and result <= self.lf_before:
                    result -= 1
                return result
            elif self.state == "INSERTING":
                s2 = self.bwt[self.lf_after]
                #mentioned in section 3.3, page 10, [1] (algorithm paper
                if s == self.overwritten and i > self.pos_first_modif:
                    r += 1
                if s > self.c:
                    c -= 1
                if s2 == s and i > self.lf_after:
                    r -= 1

        return c + r

    #Return the 1-based index of ranks
    def rank(self, c, i):
        #The minus 1 seems to be necessary because the implemented
        #rank function is 1 limited. So the first occurance has value 1
        result = self.wave.rank(c, i) - 1
        if self.state == "DELETING" and self.pos_first_modif < i and self.overwritten == c:
            result -= 1
        return result

    def count(self, c):
        result = self.wave.count(c)
        if self.state == "DELETING":
            if c > this.overwritten:
                result -= 1
        return self.wave.count(c)

    def insBase(self, i, c):
        print "Original"
        self.ins_stageIb(i, c)
        print "After stageIb"
        self.ins_stageIIa(i)
        print "After stageIIa"
        self.ins_stageIIb(i)
        print "After stageIIb"

    def delBase(self, i):
        lf_k = self.del_stageIb(i)
        self.del_stageIIa(i)
        self.del_stageIIb(i, lf_k)


    def printBWT(self):
        print 'S', 'I', 'F', 'L'
        for i in range(len(self.bwt)):
            if i >= len(self.sa):
                print " ", " ", sorted(self.bwt)[i], self.bwt[i]
            else:
                print self.sa[i], self.isa[i], sorted(self.bwt)[i], self.bwt[i]



################################################################################
#                           "Private" Methods Below                            #
################################################################################


    def _createBWM(self, t):
        return sorted([t[i:] + t[:i] for i in range(len(t))])

    def _createBWT(self, genome):
        L = [row[-1] for row in self._createBWM(genome)]
        return "".join(L)

    def _createSA(self, t):
        bwm = self._createBWM(t)
        unsorted = [t[i:] for i in range(len(t))]
        indexSA = {}
        sa = []
        isa = []
        for i, row in enumerate(unsorted):
            indexSA[row] = i
        for row in sorted(indexSA.keys()):
            sa.append(indexSA[row])
        for i in range(len(sa)):
            isa.append(sa.index(i))
        return sa, isa

    #Find the row corresponding to the ith rotation
    def _index(self, i):
        return self.isa[i]

    #See paper on dynamic suffix arrays for this algorithm
    def _updateSA(self, k_prime, i):
        for x in range(len(self.sa)):
            if self.sa[x] >= i:
                self.sa[x] += 1
        self.sa.insert(k_prime, i)
        for x in range(len(self.isa)):
            if self.isa[x] >= k_prime:
                self.isa[x] += 1
        self.isa.insert(i, k_prime)

    def printRank(self):
        print '_|' + '|'.join(list(self.bwt))
        for letter in sorted(set(list(self.bwt))):
            result = []
            for j in range(len(self.bwt)):
                result.extend([str(self.rank(letter, j) + 1)])
            print letter +'|'+ '|'.join(result)

    def _move(self, j, j_prime):
        #Remove the self.lf_beforeth value
        self.delete(j)

        #Insert into the self.lf_after index
        self.insert(self.L_store, j_prime)

        #Updating SA
        temp = self.sa[j]
        self.sa[j] = self.sa[j_prime]
        self.sa[j_prime] = temp

        #Updating ISA
        for value in range(j + 1, j_prime + 1):
            index = self.isa.index(value)
            self.isa[index] -= 1
        self.isa[self.isa.index(j)] = j_prime



####################################################################################
#                              Insertion of 1 element                              #
####################################################################################

    def insert(self, c, i):
        self.bwt = self.bwt[:i] + c + self.bwt[i:]
        self.wave.insert(c, i)
        #post insert modifications
        if self.state in ["INSERTING", "DELETING", "SUBSTITUTING"]:
            if i <= self.lf_before:
                self.lf_before += 1
                print "increasing lf_before because of insert:", self.lf_before
            if i <= self.pos_first_modif:
                self.pos_first_modif += 1

    def delete(self, i):
        self.bwt = self.bwt[:i] + self.bwt[i + 1:]
        self.wave.delete(i)

        if self.state in ["INSERTING", "DELETING", "SUBSTITUTING"]:
            #post delete modifications
            if self.lf_before >= i:
                self.lf_before -= 1
                print "decreasing lf_before because greater than delete:", self.lf_before

            if self.pos_first_modif >= i:
                self.pos_first_modif -= 1

    '''Stage Ib. Given the insertion index i and the character to insert c,
       Insert c into the bwt at i, overwriting the character there'''
    def ins_stageIb(self, i, c):
        self.lf_before = None
        self.lf_after = None

        #the character to be inserted
        self.c = c

        #Find the index of the ith sorted cyclic shift
        self.pos_first_modif = self.isa[i]

        #Needed by lf_after later, since pos_first_modif can be changed by then
        k = self.pos_first_modif

        #Track this original k because it'll be changing soon

        #The character to be overwritten by Stage Ib
        self.overwritten = self.bwt[self.pos_first_modif]

        #Rank of the overwritten character, used in both lf_before after the sub
        rank = self.rank(self.overwritten, self.pos_first_modif)

        print "Overwriting the character in L at index", self.pos_first_modif
        #Perform the substitution of overwritten in L with c
        self.delete(self.pos_first_modif)
        self.insert(c, self.pos_first_modif)
        #Changes state of the algorithm. impacts behavior of self.insert and self.delete
        self.state = "INSERTING"

        #The LF of the overwritten character before being replaced
        self.lf_before = self.count(self.overwritten) + rank

        #Modify this LF based on the qualities of the inserted character
        if self.overwritten > self.c:
            self.lf_before -= 1
            print "decreasing lf_before because overwritten > c:", self.lf_before

        #The LF of the newly subbed in character (may be different than the _before one)
        self.lf_after = self.count(self.c) + self.rank(self.c, k)
        print "lf_before:", self.lf_before, "lf_after:", self.lf_after

    def ins_stageIIa(self, i):
        #The letter being subbed in heavily impacts the location of insert
        print "inserting", self.overwritten, "at row:", self.lf_after
        #Perform the insertion of the row corresponding to c in F and overwritten in L
        #code has direct manipulation, not this insert call?
        #self.insert(self.overwritten, self.lf_after)
        self.bwt = self.bwt[:self.lf_after] + self.overwritten + self.bwt[self.lf_after:]
        self.wave.insert(self.overwritten, self.lf_after)
        self.current_modif = 0
        #Update the SA and ISA
        self._updateSA(self.lf_after, i)


    def ins_stageIIb(self, i):
        #Prepare the two LFs for stage IIb
        #This handles most of the effects varying i and c can have on the process
        print "Current state of before/after:", self.lf_before, self.lf_after
        if self.lf_after <= self.lf_before:
            self.lf_before += 1
            print "increasing lf_before because after is <=:", self.lf_before
        if self.lf_after <= self.pos_first_modif:
            self.pos_first_modif += 1

        self.state = "REORDERING"
        #store the letter currently in the lf_before slot (the new character)
        self.L_store = self.overwritten

        #the count for this letter
        smaller = self.count(self.L_store)

        #self.lf_before = i -1, corresponding to the T[i-1] cyclic shift

        #expected/computed index of T'[i-1] self.lf_before' in algorithm
        expected = smaller + self.rank(self.L_store, self.lf_after)
        print "Start of while: j:", self.lf_before, "j_prime:", expected
        while self.lf_before != expected:
            #Store temporary values needed throughout the loop
            self.L_store = self.bwt[self.lf_before]
            smaller = self.count(self.L_store)
            temp_lf_before = smaller + self.rank(self.L_store, self.lf_before)
            print "Moving rows" , self.lf_before, expected
            print "which affects", self.L_store, self.bwt[expected]
            self._move(self.lf_before, expected)

            #Perform the round of LFs to progress to next while
            self.lf_after = expected
            self.lf_before = temp_lf_before
            expected = smaller + self.rank(self.L_store, self.lf_after)
            print "Loop of Step IIb"
            print "j =", self.lf_before, "j_prime =", expected
        #end while
        self.state = "IDLE"
        self.lf_after = expected


####################################################################################
#                              Deletion of 1 element                               #
####################################################################################


    '''Stage Ib. Given the deletion index i, overwrite the character at Ti with Ti-1'''
    def  del_stageIb(self, i):
        #TODO right now count is rebuilt entirely (time consuming)
        #Waiting on implementing navarro
        k = self.isa[i]
        overwritten = self.bwt[k]
        lf_k = self._lf(k)
        c = self.bwt[k]
        self.bwt = self.bwt[:k] + self.bwt[lf_k] + self.bwt[k+1:]
        return lf_k

    def del_stageIIa(self, i):
        k = self._index(i)
        deletionPoint = k
        self.bwt = self.bwt[:deletionPoint] + self.bwt[deletionPoint + 1:]
        self.count = self._createCount()
        self.occ = self._createOcc()
        self._updateSA(deletionPoint, i)

    def del_stageIIb(self, i, lf_k):
        self.lf_before = lf_k + 1
        self.lf_after = self._lf(lf_k)
        while self.lf_before!= self.lf_after:
            new_self.lf_before = self._lf(self.lf_before)
            self._move(self.lf_before, self.lf_after)
            self.lf_before = new_self.lf_before
            self.count = self._createCount()
            self.occ = self._createOcc()
            self.lf_after = self._lf(self.lf_after)


