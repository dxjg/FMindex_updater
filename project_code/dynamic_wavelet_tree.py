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
    def __init__(self, alphabet, sequence, parent=None, left=None, right=None):
        self._alphabet = alphabet
        self._left = left
        self._right = right
        self._parent = parent

        bit_vector_string = ''
        split = len(alphabet)/2
        for character in sequence:
            if alphabet.index(character) < split:
                bit_vector_string += '0'
            else:
                bit_vector_string += '1'
        self._bit_vector = DynamicBitVector(bit_vector_string)


    def rank(self, index):
        return self._bit_vector.rank(index)

    def select(self, occurrence):
        return self._bit_vector.select(occurence)

    def insert(self, bit, index):
        self._bit_vector.insert(bit, index)

    def delete(self, index):
        self._bit_vector.delete(index)

    def split_node(self, sequence):
        split = len(self._alphabet)/2
        left_sequence, right_sequence = '', ''
        left_alphabet, right_alphabet = self._alphabet[:split], self._alphabet[split:]
        for i in xrange(0, len(sequence)):
            if self._bit_vector.get_bit_vector()[i] == '0':
                left_sequence += sequence[i]
            else:
                right_sequence += sequence[i]
        left_node = Node(left_alphabet, left_sequence, self)
        right_node = Node(right_alphabet, right_sequence, self)
        return left_node, right_node, left_sequence, right_sequence

    def get_alphabet(self):
        return self._alphabet

    def get_bit_vector(self):
        return self._bit_vector

    def get_left(self):
        return self._left

    def set_left(self, node):
        self._left = node

    def get_right(self):
        return self._right

    def set_right(self, node):
        self._right = node

    def get_parent(self):
        return self._parent




class DynamicWaveletTree:
    @staticmethod
    def _create_wavelet_tree(node, sequence):
        left_node, right_node, left_sequence, right_sequence = node.split_node(sequence)
        node.set_left(left_node)
        node.set_right(right_node)
        if len(left_node.get_alphabet()) > 1:
            DynamicWaveletTree._create_wavelet_tree(left_node, left_sequence)
        if len(right_node.get_alphabet()) > 1:
            DynamicWaveletTree._create_wavelet_tree(right_node, right_sequence)

    @staticmethod
    def _rank(node, character, index):
        alphabet = node.get_alphabet()
        if (len(alphabet) == 1):
            return index
        split = len(alphabet)/2
        if alphabet.index(character) < split:
            new_index = index - node.rank(index)
            return DynamicWaveletTree._rank(node.get_left(), character, new_index)
        else:
            new_index = node.rank(index)
            return DynamicWaveletTree._rank(node.get_right(), character, new_index)

    def __init__(self, sequence):
        self._head = Node('$ACGT', sequence)
        DynamicWaveletTree._create_wavelet_tree(self._head, sequence)
        return None

    def rank(self, character, index):
        return DynamicWaveletTree._rank(self._head, character, index)

    def select(self, character, occurence):
        return None

    def insert(self, character, index):
        return None

    def delete(self, index):
        return None

