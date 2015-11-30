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
        C = self.count[self.bwt[index-1]]
        Occ = self.occ[self.bwt[index-1]][index-1]
        print C, Occ, self.bwt[C + Occ - 1]
        return C + Occ - 1

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
    #TODO Python strings are immutable, can't pop/insert. Instead we need to maybe 
    #make a new string that combines two halves of the original plus the moved character
    def _move(self, j, j_prime):
        self.bwt.insert(j_prime, bwt[j])
        if j < j_prime:
            bwt.pop([j])
        elif j > j_prime:
            bwt.pop([j+1])
        return 

    '''Stage Ib. Given the insertion index i and the character to insert c,
       Insert c into the bwt at i, overwriting the character there'''
    def _insertIntoBWT(self, i, c):
        print 0
        #TODO this
        

        


