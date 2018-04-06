#docid in format: (A-Z of source)(YYYYMMDD).(0-9 paragraph ID) for aquaint
#dataloc/AQUAINT/(A-Z of source).lower/(YYYY)/(YYYYMMDD)_(A-Z of source)_ENG
#text is between <TEXT> </TEXT> tags after <DOCNO> docid </DOCNO>

#for aquaint2: (A-Z of source)_ENG_(YYYMMDD).(0-9 paragraph ID)
#dataloc/AQUAINT-2/data/"(A-Z of source)_ENG".lower()/"(A-Z of source)_ENG_(YYYYMM)".lower().xml
#text is located similarly, with paragraph tags to be removed

import re, sys

dataloc = "/dropbox/17-18/573/"
