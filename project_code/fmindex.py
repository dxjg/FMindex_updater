# -*- coding: utf-8 -*-
import sys

def createFM(genome):
    return FMindex(genome)

class FMindex(object):
    def __init__(self, genome):
        genome += "$"
        self.bwt = self._createBWT(genome)
        self.count = self._createCount()
        self.occ = self._createOcc()
        self.sa, self.isa = self._createSA(genome)

    def _lf(self, index):
        c = self.bwt[index]
        C = self.count[c]
        Occ = self.occ[c][index]
        print "LF(", index, ") =", C, "+", Occ, "-1 =", C + Occ - 1
        return C + Occ - 1

    def insBase(self, i, c):
        print "Original"
        self.printBWT()
        overwritten, k = self.ins_stageIb(i, c)
        print "After stageIb"
        self.printBWT()
        lf_k = self.ins_stageIIa(overwritten, k, i)
        print "After stageIIa"
        self.printBWT()
        self.ins_stageIIb(i, lf_k, k)
        print "After stageIIb"
        self.printBWT()

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
        for j in range(len(self.sa)):
            if self.sa[j] >= i:
                self.sa[j] += 1
        self.sa.insert(k_prime, i)
        for j in range(len(self.isa)):
            if self.isa[j] >= k_prime:
                self.isa[j] += 1
        self.isa.insert(i, k_prime)


    #from the python fmindex github. TODO link here
    def _createCount(self):
        A = {}
        #first pass we count all occurances
        for c in self.bwt:
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
        del A
        return B

    '''A Sigma-by-len(bwt) table'''
    def _createOcc(self):
        table = {}
        for c in sorted(self.count.keys()):
            table[c] = {}
        for i in sorted(self.count.keys()):
            prev = 0
            for j in range(len(self.bwt)):
                if i == self.bwt[j]:
                    table[i][j] = prev + 1
                    prev += 1
                else:
                    table[i][j] = prev
        return table

    #Part of insBase, subBase, and delBase
    def _move(self, j, j_prime):
        if j < j_prime:
            self.bwt = self.bwt[:j] + self.bwt[j+1:j_prime + 1] + self.bwt[j] + self.bwt[j_prime + 1:]
            #Updating SA
            temp = self.sa[j]
            self.sa[j] = self.sa[j_prime]
            self.sa[j_prime] = temp
            #Updating ISA
            for value in range(j + 1, j_prime + 1):
                index = self.isa.index(value)
                print "Decrementing row:", index, ", Containing:", value
                self.isa[index] -= 1
            print "Setting row", self._index(j), "to", j_prime
            self.isa[self.isa.index(j)] = j_prime
            print "Moving rows" , j, j_prime
        else:
            self.bwt = self.bwt[:j_prime] + self.bwt[j] + self.bwt[j_prime:j] + self.bwt[j+1:]
            #Updating SA
            temp = self.sa[j]
            self.sa[j] = self.sa[j_prime]
            self.sa[j_prime] = temp
            #Updating ISA
            for value in range(j_prime, j):
                index = self.isa.index(value)
                print "Incrementing row:", index
                self.isa[index] += 1
            self.isa[self.sa[j]] = j_prime
            print "Moving rows" , j, j_prime



####################################################################################
#                              Insertion of 1 element                              #
####################################################################################

    '''Stage Ib. Given the insertion index i and the character to insert c,
       Insert c into the bwt at i, overwriting the character there'''
    def ins_stageIb(self, i, c):
        #TODO right now count is rebuilt entirely (time consuming)
        #Waiting on implementing navarro
        k = self.isa[i]
        print self.count
        overwritten = self.bwt[k]
        self.overwritten = overwritten
        self.c = c
        self.lf_k = self._lf(k)
        self.pos = self.lf_k
        print "overwriting the character at index", k
        self.bwt = self.bwt[:k] + self.bwt[k+1:]
        self.bwt = self.bwt[:k] + c + self.bwt[k:]
        return overwritten, k

    def ins_stageIIa(self, overwritten, k, i): 
        self.count = self._createCount()
        self.occ = self._createOcc()
        #The letter clearly matters, A vs C vs G vs T  
        lf_k = self.lf_k
        print "INS: k=", k, "; LF(k)=:", lf_k
        print "inserting", overwritten, "at row:", lf_k 
        self.bwt = self.bwt[:lf_k] + overwritten + self.bwt[lf_k:]
        self._updateSA(lf_k, i)
        self.pos += 1
        self.count = self._createCount()
        self.occ = self._createOcc()
        return lf_k

    def ins_stageIIb(self, i, lf_k, k): 
        j = lf_k + 1
        j_prime = self._lf(lf_k)
        if self.c > self.overwritten: 
            j_prime += 1
        print j, j_prime
        while j != j_prime:
            new_j = self._lf(j)
            self._move(j, j_prime)
            j = new_j
            self.count = self._createCount()
            self.occ = self._createOcc()
            j_prime = self._lf(j_prime) 
            


####################################################################################
#                              Deletion of 1 element                               #
####################################################################################
        

    '''Stage Ib. Given the deletion index i, overwrite the character at Ti with Ti-1'''
    def  del_stageIb(self, i):
        #TODO right now count is rebuilt entirely (time consuming)
        #Waiting on implementing navarro
        k = self._index(i)
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
        j = lf_k + 1
        j_prime = self._lf(lf_k)
        while j!= j_prime:
            new_j = self._lf(j)
            self._move(j, j_prime)
            j = new_j
            self.count = self._createCount()
            self.occ = self._createOcc()
            j_prime = self._lf(j_prime)
        

