
import sys
from aligner import Aligner

string = "ACTCTGCTTTAG"
a = Aligner(string)

#test exact match
pos, edits = a.align("TCTGC")
assert pos == 2
print pos, edits

#test insertion
pos, edits = a.align("ACTTGC")
print pos, edits
assert pos == 0

#test replacement
pos, edits = a.align("TACTT")
print pos, edits
assert pos == 4

#test deletion
pos, edits = a.align("TCTTT")
print pos, edits
assert pos == 6

#test deletion and substitution
pos, edits = a.align("AAA")
print pos, edits
assert pos == 9

#test insert and delete
pos, edits = a.align("TCTGTTTC")
print pos, edits
assert pos == 2

#test 2 deletions and substitution
pos, edits = a.align("AAAA")
print pos, edits
assert pos == 9

string = "TCAGATTACG"
a = Aligner(string)
pos, edits = a.align("TCAGTACG")
print pos, edits
assert pos == 0

string = "TCAGATGACG"
a = Aligner(string)
pos, edits = a.align("TCAGGACG")
assert pos == 0
print pos, edits

