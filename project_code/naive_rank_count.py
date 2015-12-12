class NaiveRankCount:
    """ This class is a naive implementation of rank and count methods. """

    @staticmethod
    def _create_count_table(alphabet, sequence):
        character_counts = {'$': 0, 'A': 0, 'C': 0, 'G': 0, 'T': 0}
        count_table = {}
        count_accumulation = 0
        for character in sequence:
            character_counts[character] += 1
        for character in alphabet:
            count_table[character] = count_accumulation
            count_accumulation += character_counts[character]
        return count_table

    def __init__(self, sequence):
        self._alphabet = '$ACGT'
        self._sequence = sequence
        self._count_table = NaiveRankCount._create_count_table(self._alphabet, sequence)

    def rank(self, character, index):
        count = 0
        for i in xrange(0, index+1):
            if self._sequence[i] == character:
                count += 1
        return count

    def count(self, character):
        return self._count_table[character]

    def insert(self, character, index):
        self._sequence = self._sequence[:index] + character + self._sequence[index:]

    def delete(self, index):
        self._sequence = self._sequence[:index] + self._sequence[index+1:]

    def print_sequence(self):
        print self._sequence
