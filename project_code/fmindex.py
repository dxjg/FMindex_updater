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

    def _insertIntoBWT(self, i, c):
        overwritten, k = self._stageIb(i, c)
        self._stageIIa(overwritten, i)
        self._stageIIb(i, k)

    #Find the row corresponding to the ith rotation
    def _index(self, i):
        return self.sa.index(i)


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
    
    #See paper on dynamic suffix arrays for this algorithm
    def _updateSA(self, k_prime, i):
        for j in range(len(self.sa)):
            if self.sa[j] >= i:
                self.sa[j] += 1
        self.sa.insert(k_prime, i)

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

    def _move(self, j, j_prime):
        if j < j_prime:
            print self.bwt[:j], self.bwt[j+1:j_prime+1], self.bwt[j], self.bwt[j_prime + 1:]
            temp = self.bwt[:j] + self.bwt[j+1:j_prime + 1] + self.bwt[j] + self.bwt[j_prime + 1:]
        elif j > j_prime:
            print self.bwt[:j_prime], self.bwt[j], self.bwt[j_prime:j], self.bwt[j:]
            temp = self.bwt[:j_prime] + self.bwt[j] + self.bwt[j_prime:j] + self.bwt[j:]
        self.bwt = temp
        tempSA = self.sa.pop(j)
        self.sa.insert(j_prime, tempSA)
        return 

    '''Stage Ib. Given the insertion index i and the character to insert c,
       Insert c into the bwt at i, overwriting the character there'''
    def _stageIb(self, i, c):
        #TODO right now count is rebuilt entirely (time consuming)
        #Waiting on implementing navarro
        k = self.sa.index(i)
        overwritten = self.bwt[k]
        overwritten_k = self._lf(k)
        print k, overwritten_k
        self.bwt = self.bwt[:k] + c + self.bwt[k+1:]
        print "After stage Ib:"
        self._printBWT()
        return overwritten, overwritten_k

    def _stageIIa(self, overwritten, i):
        k = self.sa.index(i)
        insertPoint = self._lf(k) + 1
        print "inserting T at row ", insertPoint, i, k
        temp = self.bwt[:insertPoint] + overwritten + self.bwt[insertPoint:]
        self.bwt = temp
        print "After stage IIa", self.bwt, len(self.bwt)
        self._printBWT()
        self.count = self._createCount()
        print self.count
        self._updateSA(insertPoint, i)
        self.occ = self._createOcc()

    def _stageIIb(self, i, k):
        j = k + 1
        j_prime = self._lf(k)
        while j!= j_prime:
            print "j= ", j, ", j' = ", j_prime
            new_j = self._lf(j)
            self._move(j, j_prime)
            print "One loop of Stage IIb", self.bwt
            j = new_j
            j_prime = self._lf(j_prime)
        print "After Stage IIb"
        self._printBWT()

        
    def _printBWT(self):
        for i in range(len(self.bwt)):
            print self.bwt[i]

        

        


