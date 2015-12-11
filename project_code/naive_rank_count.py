class NaiveRankCount:
    """ This class is a naive implementation of rank and count methods. """

    @staticmethod
    def _create_count_table(alphabet, sequence):
        character_counts, count_table = {}, {}
        count_accumulation = 0
        for character in sequence:
            if character not in count_table.keys():
                character_counts[character] = 1
            else:
                character_counts[character] += 1
        for character in alphabet:
            count_table[character] = count_accumulation
            count_accumulation += character_counts[character]
        return count_table

    def __init__(self, sequence):
        self._alphabet = '$ACGT'
        self._sequence = sequence
        self._count_table = NaiveRankCount._create_count_table(self._alphabet, sequence)
        print self._count_table

