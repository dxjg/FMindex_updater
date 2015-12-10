import logging

class DynamicBitVector:
    def __init__(self, bit_vector):
        self._bit_vector = bit_vector

    def rank_0(self, index):
        count = 0
        for i in xrange(0, index+1):
            if i == len(self._bit_vector):
                break
            if self._bit_vector[i] == '0':
                count += 1
        return count

    def rank_1(self, index):
        count = 0
        for i in xrange(0, index+1):
            if i == len(self._bit_vector):
                break
            if self._bit_vector[i] == '1':
                count += 1
        return count

    def select_0(self, occurrence):
        if len(self._bit_vector) == 0:
            return -1
        count = 0
        last_occurrence = 0
        for i in xrange(0, len(self._bit_vector)):
            if self._bit_vector[i] == '0':
                count += 1
                last_occurrence = i
            if count == occurrence:
                return i
        return last_occurrence

    def select_1(self, occurrence):
        if len(self._bit_vector) == 0:
            return -1
        count = 0
        last_occurrence = 0
        for i in xrange(0, len(self._bit_vector)):
            if self._bit_vector[i] == '1':
                count += 1
                last_occurrence = i
            if count == occurrence:
                return i
        return last_occurrence

    def insert(self, bit, index):
        self._bit_vector = self._bit_vector[:index] + bit + self._bit_vector[index:]

    def delete(self, index):
        self._bit_vector = self._bit_vector[:index] + self._bit_vector[index+1:]

    def get_bit_vector(self):
        return self._bit_vector

class Node:
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

    def rank_0(self, index):
        return self._bit_vector.rank_0(index)

    def rank_1(self, index):
        return self._bit_vector.rank_1(index)

    def select_0(self, occurrence):
        return self._bit_vector.select_0(occurrence)

    def select_1(self, occurrence):
        return self._bit_vector.select_1(occurrence)

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

    def get_size(self):
        return len(self._bit_vector.get_bit_vector())

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
            return node.rank_1(index)
        split = len(alphabet)/2
        if alphabet.index(character) < split:
            count = node.rank_0(index)
            if count == 0:
                return 0
            return DynamicWaveletTree._rank(node.get_left(), character, count-1)
        else:
            count = node.rank_1(index)
            if count == 0:
                return 0
            return DynamicWaveletTree._rank(node.get_right(), character, count-1)

    @staticmethod
    def _select(node, previous, occurrence):
        parent = node.get_parent()
        if previous == 'left':
            next_index = node.select_0(occurrence)
        elif previous == 'right':
            next_index = node.select_1(occurrence)
        if parent is None:
            return next_index
        if next_index < 0:
            return -1
        if parent.get_left() == node:
            return DynamicWaveletTree._select(parent, 'left', next_index+1)
        else:
            return DynamicWaveletTree._select(parent, 'right', next_index+1)

    @staticmethod
    def _count(node, character):
        alphabet = node.get_alphabet()
        if len(alphabet) == 1:
            if alphabet < character: return node.get_size()
            else: return 0
        return DynamicWaveletTree._count(node.get_left(), character) + \
               DynamicWaveletTree._count(node.get_right(), character)

    @staticmethod
    def _insert(node, character, index):
        bit_vector = node.get_bit_vector()
        alphabet = node.get_alphabet()
        split = len(alphabet)/2
        if alphabet.index(character) < split:
            bit_vector.insert('0', index)
            next_index = bit_vector.rank_0(index) - 1
            if len(alphabet) != 1:
                DynamicWaveletTree._insert(node.get_left(), character, next_index)
        else:
            bit_vector.insert('1', index)
            next_index = bit_vector.rank_1(index) - 1
            if len(alphabet) != 1:
                DynamicWaveletTree._insert(node.get_right(), character, next_index)

    @staticmethod
    def _delete(node, index):
        bit_vector = node.get_bit_vector()
        alphabet = node.get_alphabet()
        if bit_vector.get_bit_vector()[index] == '0':
            next_index = bit_vector.rank_0(index) - 1
            if len(alphabet) != 1:
                DynamicWaveletTree._delete(node.get_left(), next_index)
        else:
            next_index = bit_vector.rank_1(index) - 1
            if len(alphabet) != 1:
                DynamicWaveletTree._delete(node.get_right(), next_index)
        bit_vector.delete(index)

    def __init__(self, sequence):
        self._head = Node('$ACGT', sequence)
        DynamicWaveletTree._create_wavelet_tree(self._head, sequence)
        return None

    def rank(self, character, index):
        return DynamicWaveletTree._rank(self._head, character, index)

    def select(self, character, occurrence):
        if occurrence <= 0:
            return -1
        node = self._head
        while True:
            alphabet = node.get_alphabet()
            if len(alphabet) == 1:
                break
            split = len(alphabet)/2
            if alphabet.index(character) < split:
                node = node.get_left()
            else:
                node = node.get_right()
        return DynamicWaveletTree._select(node, 'right', occurrence)


    def count(self, character):
        return DynamicWaveletTree._count(self._head, character)

    def insert(self, character, index):
        DynamicWaveletTree._insert(self._head, character, index)

    def delete(self, index):
        DynamicWaveletTree._delete(self._head, index)

    def print_sequence(self):
        print self._head.get_bit_vector().get_bit_vector()
