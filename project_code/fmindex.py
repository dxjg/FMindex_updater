# -*- coding: utf-8 -*-


def createFM(genome):
    return FMindex(genome)

class FMindex(object):
    def __init__(self, genome):
        genome += "$"
        self.bwt = self._createBWT(genome)
        self.count = self._createCount()
        self.occ = self._createOcc()

    def _createBWM(self, t):
        return sorted([t[i:] + t[:i] for i in range(len(t))])

    def _createBWT(self, genome):
        L = [row[-1] for row in self._createBWM(genome)]
        return "".join(L)

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

    '''A sigma by len(bwt) table  '''
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


    def _lf(self, index):
        C = self.count[self.bwt[index-1]]
        Occ = self.occ[self.bwt[index-1]][index-1]
        print C, Occ, self.bwt[C + Occ - 1]
        return C + Occ - 1

        
        

        


