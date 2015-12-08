# -*- coding: utf-8 -*-


def createFM(genome):
    return FMindex(genome)

class FMindex(object):
    def __init__(self, genome):
        genome += "$"
        self.bwt = self._createBWT(genome)
        self.count = self._createCount()
        self.occ = self._createOcc()
        self.sa = self._createSA(genome)

    def _lf(self, index):
        C = self.count[self.bwt[index]]
        Occ = self.occ[self.bwt[index]][index]
        return C + Occ - 1

    def insBase(self, i, c):
        overwritten, k = self.ins_stageIb(i, c)
        self.ins_stageIIa(overwritten, k, i)
        self.ins_stageIIb(i, k)

    def delBase(self, i):
        k = self.del_stageIb(i)
        self.del_stageIIa(i)
        self.del_stageIIb(i, k)

    def printBWT(self):
        for i in range(len(self.bwt)):
            print self.bwt[i]


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
        for i, row in enumerate(unsorted):
            indexSA[row] = i
        for row in sorted(indexSA.keys()):
            sa.append(indexSA[row])
        return sa
    
    #Find the row corresponding to the ith rotation
    def _index(self, i):
        return self.sa.index(i)

    #See paper on dynamic suffix arrays for this algorithm
    def _updateSA(self, k_prime, i):
        if len(self.sa) < len(self.bwt):
            for j in range(len(self.sa)):
                if self.sa[j] >= i:
                    self.sa[j] += 1
            self.sa.insert(k_prime, i)
        else:
            for j in range(len(self.sa)):
                if self.sa[j] >= i:
                    self.sa[j] -= 1
            del self.sa[k_prime]


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
            print self.bwt[:j], self.bwt[j+1:j_prime+1], self.bwt[j], self.bwt[j_prime + 1:]
            temp = self.bwt[:j] + self.bwt[j+1:j_prime + 1] + self.bwt[j] + self.bwt[j_prime + 1:]
        elif j > j_prime:
            print self.bwt[:j_prime], self.bwt[j], self.bwt[j_prime:j], self.bwt[j:]
            temp = self.bwt[:j_prime] + self.bwt[j] + self.bwt[j_prime:j] + self.bwt[j:]
        self.bwt = temp
        print "Moving rows" , j, j_prime
        tempSA = self.sa.pop(j)
        print self.sa, tempSA
        self.sa.insert(j_prime, tempSA)
        return 

####################################################################################
#                              Insertion of 1 element                              #
####################################################################################

    '''Stage Ib. Given the insertion index i and the character to insert c,
       Insert c into the bwt at i, overwriting the character there'''
    def ins_stageIb(self, i, c):
        #TODO right now count is rebuilt entirely (time consuming)
        #Waiting on implementing navarro
        k = self.sa.index(i)
        overwritten = self.bwt[k]
        overwritten_k = self._lf(k)
        print "INS: Beginning stage Ib"
        print "INS: Overwritten index:", k, "; LF of Overwritten index:", overwritten_k
        self.bwt = self.bwt[:k] + c + self.bwt[k+1:]
        print "INS: After stage Ib:", self.bwt
        self.count = self._createCount()
        self.occ = self._createOcc()
        return overwritten, overwritten_k

    def ins_stageIIa(self, overwritten, k, i): 
        print "inserting T at row:", k
        temp = self.bwt[:k] + overwritten + self.bwt[k:]
        self.bwt = temp
        print "INS: After stage IIa", self.bwt
        self.count = self._createCount()
        print self.count
        self._updateSA(k, i)
        self.occ = self._createOcc()

    def ins_stageIIb(self, i, k):
        j = self.sa.index(i-1)
        j_prime = self._lf(k)
        while j!= j_prime:
            print "INS: j= ", j, ", j' = ", j_prime
            new_j = self._lf(j)
            self._move(j, j_prime)
            print "INS: Loop of Stage IIb", self.bwt
            j = new_j
            j_prime = self._lf(j_prime)
            print j, j_prime
        print "INS: After Stage IIb", self.bwt


####################################################################################
#                              Deletion of 1 element                               #
####################################################################################
        

    '''Stage Ib. Given the deletion index i, overwrite the character at Ti with Ti-1'''
    def  del_stageIb(self, i):
        #TODO right now count is rebuilt entirely (time consuming)
        #Waiting on implementing navarro
        T = "CTGCTGC$"
        print T[i], T[i-1]
        k = self.sa.index(i)
        overwritten = self.bwt[k]
        j = self._lf(k)
        print k, j, self.bwt[k], self.bwt[j]
        overwritten_k = self._lf(k)
        print i, k, overwritten_k, j, self.sa[k], self.sa[overwritten_k], self.sa[j]
        print "Should be T:", self.bwt[k]
        c = self.bwt[k]
        print "DEL: Beginning stage Ib"
        print "DEL: Overwritten index:", k, "; LF of Overwritten index:", overwritten_k
        self.bwt = self.bwt[:k] + self.bwt[j] + self.bwt[k+1:]
        print "DEL: After stage Ib:"
        self.printBWT()
        return j

    def del_stageIIa(self, i):
        k = self.sa.index(i)
        F = sorted(self.bwt)
        print "Want to delete row:", F[k], ":", self.bwt[k]
        deletionPoint = k
        print "DEL: Deleting at row:", deletionPoint
        temp = self.bwt[:deletionPoint] + self.bwt[deletionPoint + 1:]
        self.bwt = temp
        print "DEL: After stage IIa", self.bwt, len(self.bwt)
        self.printBWT()
        self.count = self._createCount()
        print self.count
        self._updateSA(deletionPoint, i)
        self.occ = self._createOcc()

    def del_stageIIb(self, i, k):
        j = k + 1
        j_prime = self._lf(k)
        while j!= j_prime:
            print "DEL: j= ", j, ", j' = ", j_prime
            new_j = self._lf(j)
            self._move(j, j_prime)
            print "DEL: Loop of Stage IIb", self.bwt
            j = new_j
            j_prime = self._lf(j_prime)
        print "DEL: After Stage IIb"
        self.printBWT()
        

