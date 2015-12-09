# -*- coding: utf-8 -*-


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
        C = self.count[self.bwt[index]]
        
        Occ = self.occ[self.bwt[index]][index]
        print "LF(", index, ") =", C, "+", Occ, - 1, "=", C + Occ - 1
        return C + Occ - 1

    def insBase(self, i, c):
        print "Original"
        self.printOcc()
        self.printBWT()
        overwritten, lf_k = self.ins_stageIb(i, c)
        print "After stageIb"
        self.printOcc()
        self.printBWT()
        self.ins_stageIIa(overwritten, lf_k, i)
        print "After stageIIa"
        self.printOcc()
        self.printBWT()
        self.ins_stageIIb(i, lf_k)
        print "After stageIIb"
        self.printOcc()
        self.printBWT()

    def delBase(self, i):
        lf_k = self.del_stageIb(i)
        self.del_stageIIa(i, lf_k)
        self.del_stageIIb(i, lf_k)

    def printOcc(self):
        bwt = list()
        bwt.append("_|")
        btm = list()
        btm.append("--")
        for i in range(len(self.bwt)):
            bwt.append(self.bwt[i])
            bwt.append("|")
            btm.append("--")
        print ''.join(btm)
        print ''.join(bwt)
        for letter in sorted(self.count.keys()):
            sum = 0
            result = list()
            result.append(letter)
            result.append("|")
            for i in range(len(self.bwt)):
                if letter == self.bwt[i]:
                    result.append(str(sum + 1))
                    result.append("|")
                    sum += 1
                else:
                    result.append(str(sum))
                    result.append("|")
            result[len(result)-1] = result[len(result)-1][-1:]
            print ''.join(result) 
        print ''.join(btm)
                    


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
            print "j < j'"
            self.bwt = self.bwt[:j] + self.bwt[j+1:j_prime + 1] + self.bwt[j] + self.bwt[j_prime + 1:]
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
            self.isa[self.isa.index(j)] = j_prime
        print "Moving rows" , j, j_prime
        return 


####################################################################################
#                              Insertion of 1 element                              #
####################################################################################

    '''Stage Ib. Given the insertion index i and the character to insert c,
       Insert c into the bwt at i, overwriting the character there'''
    def ins_stageIb(self, i, c):
        #TODO right now count is rebuilt entirely (time consuming)
        #Waiting on implementing navarro
        k = self._index(i)
        overwritten = self.bwt[k]
        lf_k = self._lf(k)
        self.bwt = self.bwt[:k] + c + self.bwt[k+1:]
        print "INS: k=", k, "; LF(k)=:", lf_k
        return overwritten, lf_k

    def ins_stageIIa(self, overwritten, lf_k, i): 
        print "inserting", overwritten, "at row:", lf_k
        self.bwt = self.bwt[:lf_k] + overwritten + self.bwt[lf_k:]
        self.count = self._createCount()
        self.occ = self._createOcc()
        self._updateSA(lf_k, i)

    def ins_stageIIb(self, i, lf_k):
        j = lf_k + 1
        j_prime = self._lf(lf_k)
        print "j= ", j, ", j' = ", j_prime
        while j != j_prime | j_prime != -1:
            new_j = self._lf(j)
            self._move(j, j_prime)
            print "Loop of Stage IIb", self.bwt
            self.printBWT()
            j = new_j
            self.count = self._createCount()
            self.occ = self._createOcc()
            j_prime = self._lf(j_prime)
            print "j= ", j, ", j' = ", j_prime
            


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
        

