import logging

class DynamicBitVector:
    def __init__(self, bit_vector):
        self._bit_vector = bit_vector

    def rank(self, index):
        count = 0
        for i in xrange(0, index+1):
            if self._bit_vector[i] == '1':
                count += 1
        return count

    def select(self, occurrence):
        count = 0
        for i in xrange(0, len(self._bit_vector)):
            if self._bit_vector[i] == '1':
                count += 1
            if count == occurrence:
                return i
        return (len(self._bit_vector)-1)

    def insert(self, bit, index):
        self._bit_vector = self._bit_vector[:index] + bit + self._bit_vector[index:]

    def delete(self, index):
        self._bit_vector = self._bit_vector[:index-1] + self.bit_vector[index:]

    def get_bit_vector(self):
        return self._bit_vector

class Node:
    ''' A Node contains: 1) parent 2) left child 3) right child 4) DynamicBitVector '''
    def __init__(self, bit_vector, left=None, right=None, parent=None):
        self._bit_vector = DynamicBitVector(bit_vector)
        self._left = left
        self._right = right
        self._parent = parent

    def get_bit_vector(self):
        return self._bit_vector

    def get_left(self):
        return self._left

    def get_right(self):
        return self._right

    def get_parent(self):
        return self._parent


class DynamicWaveletTree:
    ''' __init__ creates the wavelet tree; the other methods are rank, select, insert, delete '''
    def create_tree(self, sequence):
        return None

    def __init__(self, sequence):
        return None

    def rank(self, character, index):
        return None

    def select(self, character, occurence):
        return None

    def insert(self, character, index):
        return None

    def delete(self, index):
        return None

