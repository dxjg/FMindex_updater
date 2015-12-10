
import sys
from aligner import Aligner

string = "ACTCTGCTTTAG"
a = Aligner(string)

#test insertion
pos, edits = a._align("ACTTGC")
print pos, edits
assert pos == 0
#assert edits == "MMMIMM"

#test replacement
pos, edits = a._align("TACTT")
print pos, edits
assert pos == 4
#assert edits == "MRMMM"

#test deletion
pos, edits = a._align("TCTTT")
print pos, edits
assert pos == 6
#assert edits == "DMMMM"

pos, edits = a._align("AAA")
print pos, edits
assert pos == 9

pos, edits = a._align("TCTGTTTC")
print pos, edits
assert pos == 2

pos, edits = a._align("AAAA")
print pos, edits
assert pos == 9