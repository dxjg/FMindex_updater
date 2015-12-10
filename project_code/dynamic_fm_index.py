# -*- coding: utf-8 -*-
import dynamic_wavelet_tree

def createFM(genome):
    return DynamicFMindex(genome)

class DynamicFMindex(object):
    def __init__(self, genome):
        genome += "$"
        #the BWT 
        self.L = self.createBWT(genome)
        #the count array: number of characters that come before this one in F
        self.count = self.createCount()
        #object called to get rank values
        self.rank = self.createOcc()
        #"IDLE", "INSERTING", "DELETING", "SUBSTITUTING" states which impact
        #some calculations like rank and count
        self.state = "IDLE"
        #The letter which is replaced in L during stage Ib
        self.letter_substituted = ""
        #The letter we are to introduce
        self.new_letter_L = ""
        #The position where the modification is taking place
        self.position_mod_bwt = 0
        #Tracks the "previous" cyclic shift (the 'next' one that LF would return)
        self.previous_cs = 0
        #The position of the first modification to the bwt
        self.pos_first_modif = 0
        #Number of modifications remaining when inserting/subbing k letters at once
        self.current_modif = 0
        #The suffix array, where sa[i] = the alphabetically ith suffix of the BWM
        #The inverse to the suffix array. Used to find the index that a letter in
        #L originally had in T
        self.sa, self.isa = self.createSA(genome)


    def countSymbolsBefore(self, c):
        if c == '$':
            return 0
        
        result = self.count[c]
        if self.state == "DELETING":
            if c > self.char:
                result -= 1
        return result
    
    def getRank(self, c, i):
        result = self.rank[c][i]
        if self.state == "DELETING":
            result -= 1
        return result

    #Insert a character c at position i in L, main algorithm
    def insBase(self, pos, c):
        if pos > self.getSize():
            pos = self.getSize()
        #Step Ib: Replace the letter in L at the position T^[i] with c
        bwt_pos = self.isa[pos]
        if self.getSize() > 0:
             self.letter_substituted = self.L[bwt_pos]
             rank_store = self.getRank(self.letter_substituted, bwt_pos)
             self.delete(bwt_pos)
        else:
            rank_store = 0
        self.insert(c, pos)
        print self.L
        self.position_mod_bwt = bwt_pos
        print "position_mod_bwt", self.position_mod_bwt

        self.new_letter_L = c
        self.state = "INSERTING"
 
        #Compute the position of T^[i-1]
        self.previous_cs = self.countSymbolsBefore(self.letter_substituted) + rank_store - 1
        print "previous first value:", self.previous_cs
        if self.letter_substituted > self.new_letter_L:
            self.previous_cs -= 1
            print "previous decreased because sub is greater:", self.previous_cs
        oldbwt_pos = self.position_mod_bwt
 
        #Step IIa: Insert the removed row back in
        #Computes the position to insert the new row
        self.position_mod_bwt = self.countSymbolsBefore(c) + self.getRank(c, oldbwt_pos)
        print "position_mod_bwt", self.position_mod_bwt 
        #a for loop would go here if we inserted multiple strings at once

        self.new_letter_L = self.letter_substituted
        self.insert(self.letter_substituted, self.position_mod_bwt)
        self.current_modif = 0

        if self.position_mod_bwt <= self.previous_cs:
            self.previous_cs += 1
            print "previous increased because mod_bwt is <=", self.previous_cs
        if self.position_mod_bwt <= self.pos_first_modif:
            self.pos_first_modif += 1
        #Try to update the SA and ISA for the row inserted
        #Values may be backwards
        self.updateSA(self.position_mod_bwt, pos)
        if self.position_mod_bwt <= oldbwt_pos:
            oldbwt_pos += 1
        numShifts = self.reorderCS()


    #Deletes the character at position i in L, main algorithm
    def delBase(self, i):
        lf_k = self.del_stageIb(i)
        self.del_stageIIa(i, lf_k)
        self.del_stageIIb(i, lf_k)

    def insert(self, c, i):
        #If doing multiple insertions at once, this matters
        if self.state in ["INSERTING", "SUBSTITUTING", "DELETING"]:
            if i <= self.previous_cs:
                self.previous_cs += 1
                print "previous increased because insert point <=", self.previous_cs
            if i <= self.pos_first_modif:
                self.pos_first_modif += 1

        #Actually insert into L
        self.L = self.L[:i] + c + self.L[i:]
        #Update the count
        self.updateCount()
        
    #Deletes the symbol at i from L
    def delete(self, i):
        #Actually delete the character
        self.L = self.L[:i] + self.L[i+1:]
        #Update the count
        self.updateCount()
        
        #If doing multiple insertions at once, this matters
        if self.state in ["INSERTING", "SUBSTITUTING", "DELETING"]:
            if self.previous_cs >= i:
                self.previous_cs -= 1
                print "previous decreased because its >= i", self.previous_cs
            if self.pos_first_modif >= i:
                self.pos_first_modif -= 1


    def updateCount(self):
        self.count = self.createCount()

    def reorderCS(self):
        self.state = "REORDERING"
        L_store = self.new_letter_L
        expected_position = self.countSymbolsBefore(L_store) + self.getRank(L_store, self.position_mod_bwt)
        smaller = self.countSymbolsBefore(L_store)
        shift = 0

        while expected_position != self.previous_cs:
            shift += 1
            print "next row to move", L_store
            print self.previous_cs
            L_store = self.L[self.previous_cs]
            smaller = self.countSymbolsBefore(L_store)
            tmp_previous_cs = self.getRank(L_store, self.previous_cs)+smaller

            self.delete(self.previous_cs)
            self.insert(L_store, expected_position)
            #SA and ISA should be updated, but they're not being used anyway...

            #go to the previous cyclic shift
            self.position_mod_bwt = expected_position
            self.previous_cs = tmp_previous_cs
            print "previous: has LF'd to this", self.previous_cs
            expected_position = smaller + self.getRank(L_store, self.position_mod_bwt)
        self.state = "IDLE"
        self.position_mod_bwt = expected_position
        return shift





    #Reorders rows of L until it is well sorted again
    def _move(self, j, j_prime):
        if j < j_prime:
            print "j < j'"
            self.L = self.L[:j] + self.L[j+1:j_prime + 1] + self.L[j] + self.L[j_prime + 1:]
            #Updating SA
            temp = self.sa[j]
            self.sa[j] = self.sa[j_prime]
            self.sa[j_prime] = temp
            #Updating ISA
            for value in range(j + 1, j_prime + 1):
                index = self.isa.index(value)
                print "Decrementing row:", index
                self.isa[index] -= 1
            self.isa[self.isa.index(j)] = j_prime
        else: #j > j_prime:
            print "j > j'"
            self.L = self.L[:j_prime] + self.L[j] + self.L[j_prime:j] + self.L[j+1:]
            #Updating SA
            temp = self.sa[j]
            self.sa[j] = self.sa[j_prime]
            self.sa[j_prime] = temp
            #Updating ISA
            for value in range(j_prime, j):
                index = self.isa.index(value)
                print "Incrementing row:", index
                self.isa[index] += 1
            self.isa[self.isa.index(j)] = j_prime
        print "Moving rows" , j, j_prime
        return 



################################################################################
#                  "Private" Methods Below, mostly init stuff                  #
################################################################################
    
    #Returns the size of L
    def getSize(self):
        return len(self.L)

    #Prints the Occurance table (Naive Rank)
    def printOcc(self):
        print '_|' + '|'.join(list(self.L)) + '|'
        for letter in self.rank.keys():
            result = []
            result.extend([letter, "|"])
            for count in self.rank[letter]:
                result.extend([str(self.rank[letter][count]), "|"])
            print ''.join(result)

    #Prints L in a formatted table with SA, ISA, F and L columns
    def printBWT(self):
        print 'S', 'I', 'F', 'L'
        for i in range(len(self.L)):
            if i >= len(self.sa):
                print " ", " ", sorted(self.L)[i], self.L[i]
            else:
                print self.sa[i], self.isa[i], sorted(self.L)[i], self.L[i]
   

    def createBWT(self, genome):
        L = [row[-1] for row in self.createBWM(genome)]
        return "".join(L)

    def createBWM(self, t):
        return sorted([t[i:] + t[:i] for i in range(len(t))])

    def createSA(self, t):
        bwm = self.createBWM(t)
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
    

    #See paper on dynamic suffix arrays for this algorithm
    def updateSA(self, k_prime, i):
        for j in range(len(self.sa)):
            if self.sa[j] >= i:
                self.sa[j] += 1
        self.sa.insert(k_prime, i)
        for j in range(len(self.isa)):
            if self.isa[j] >= k_prime:
                self.isa[j] += 1
        self.isa.insert(i, k_prime)


    #from the python fmindex github. TODO link here
    def createCount(self):
        A = {}
        #first pass we count all occurances
        for c in self.L:
            if A.get(c):
                A[c] += 1
            else:
                A[c] = 1
        B = {}
        sum = 0
        #now we rephrase count by number of characters to before it
        for c in sorted(A.keys()): 
            B[c] = sum
            sum += A[c]
        return B

    #Creates the Occurance table (Naive Rank)
    def createOcc(self):
        table = {}
        for c in sorted(self.count.keys()):
            table[c] = {}
        for i in sorted(self.count.keys()):
            prev = 0
            for j in range(len(self.L)):
                if i == self.L[j]:
                    table[i][j] = prev + 1
                    prev += 1
                else:
                    table[i][j] = prev
        return table
