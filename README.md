# 573-HXLB
LING 573 Spring 2018

Deliverable #4

Group 8: Harita Kannan, Xiaopei Wu, Lonny Strunk, Ben McCready


To run the code on Patas, enter into the base level of the directory: `$condor_submit src/D4.cmd`

The implementation of our system is in the file `src/d4/d4.py`. For this deliverable, we made improvements towards readability of summaries, and experimented with a sentence compression algorithm proposed in [Filippova (2010)](https://aclanthology.info/pdf/C/C10/C10-1037.pdf).
added a stemmer function to customize the LexRank content selection, and experimented with two information ordering approaches: chronological ordering and greedy algorithm ordering proposed in [Nayeem and Chali (2017)](www.aclweb.org/anthology/W17-2407).
