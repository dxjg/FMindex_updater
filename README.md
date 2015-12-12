December 11, 2015
Computational Genomics Final Project
Ravi Gaddipati
Craig Hennessy
Gwen Hoffmann
David Gong

This program is an implementation of a self updating FM index.
The main parts of the code are:

fmindex.py : Implements the fmindex, and the 4 stage update alogrithm. Also updates the suffix array.
dynamic_wavelet_tree.py : Implements a dynamic rank/count data structure. Used by fmindex.py
hashTracker.py : Tracks alignments and finds the changes that need to be made to the index.
rangeTracker.py: A first implementation, not currently used.
aligner.py : Aligns a read to the FMindex/
driver.py: Main driving program. Takes a reference, reads, and parameters.

Tests:



Usage of the program is done through the driver.py. A basic test is:

python driver.py ../test_data/testRef ../test_data/testReads_sub 10 1 3 50

The output is timing information as well the modified reference as recovered from the FM index.

Parameters are:
python driver.py [reference] <reads> <Interval> <MinReads> <TriggerPoint> <confidence>

reference is the template sequence and reads is a list of reads (one per line). Interval defines what size block to split the reference in for the purposes of alignment tracking. Minimum reads specifies the minimum number of reads before considering an index update. Trigger point specifies when a blocks changes should be dumped for update. Confidence is the minimum percentage that a change needs to appear before an update. E.g. if 100 reads are aligned and 50 have an alternate allele, the index will update if confidence is <50 but not for >50.

A list of parameters above was used to see if there was any significant timing changes. Unfortunately we weren't able to find any trends. We will need to try larger datasets, which would be facilitated by a faster aligner.