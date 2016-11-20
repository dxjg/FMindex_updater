# Computational Genomics Final Project
## December 11, 2015

### Ravi Gaddipati, Craig Hennessy, Gwen Hoffmann, David Gong

This program is an implementation of a self updating FM index.
The main parts of the code are:

fmindex.py : Implements the fmindex, and the 4 stage update algorithm. Also updates the suffix array.
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

A list of parameters above was used to see if there was any significant timing changes. Unfortunately we weren't able to find any trends. We will need to try larger datasets, which would be facilitated by a faster aligner. A sample set of data can be obtained with:

python driver.py ../test_data/testRef ../test_data/testReads_sub 5,10 1 2,3 50


The aligner can be tested with: python test_aligner.py

This confirms that the alignment position is correctly identified and runs
experiments to show the effects of increasing read length, genome length, and
number of edits on alignment time. The data from the experiments outputs to 
a file called test_aligner_data.txt.  

The FM index can be tested with the "name"_fm_test.py methods.  
The main test file, exhaust_fm_test.py accepts an integer on the command line returns the success and failure numbers. There are additional test files for singular insertion and deletion. 
Those files accept either a single string on the command line, or a string, 
a single characterto insert, and the index to insert

# References

[1] Chan, Ho-Leung, et al. "Compressed indexes for dynamic text collections." ACM Transactions on Algorithms (TALG) 3.2 (2007): 21.

[2] Gerlach, Wolfgang. "Dynamic FM-Index for a collection of texts with application to space-efficient construction of the compressed suffix array." Master's thesis, Universität Bielefeld, Germany (2007).

[3] Salson, Mikaël, et al. "Dynamic extended suffix arrays." Journal of Discrete Algorithms 8.2 (2010): 241-257.
