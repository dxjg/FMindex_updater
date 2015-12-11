
import sys
from aligner import Aligner

string = "ACTCTGCTTTAG"
a = Aligner(string)

#test exact match
pos, edits = a._align("TCTGC")
assert pos == 2
print pos, edits

#test insertion
pos, edits = a._align("ACTTGC")
print pos, edits
assert pos == 0

#test replacement
pos, edits = a._align("TACTT")
print pos, edits
assert pos == 4

#test deletion
pos, edits = a._align("TCTTT")
print pos, edits
assert pos == 6

#test deletion and substitution
pos, edits = a._align("AAA")
print pos, edits
assert pos == 9

#test insert and delete
pos, edits = a._align("TCTGTTTC")
print pos, edits
assert pos == 2

#test 2 deletions and substitution
pos, edits = a._align("AAAA")
print pos, edits
assert pos == 9

string = "TCAGATTACG"
a = Aligner(string)
pos, edits = a._align("TCAGTACG")
print pos, edits
assert pos == 0

string = "TCAGATGACG"
a = Aligner(string)
pos, edits = a._align("TCAGGACG")
assert pos == 0
print pos, edits

