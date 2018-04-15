#docid in format: (A-Z of source)(YYYYMMDD).(0-9 paragraph ID) for aquaint
#dataloc/AQUAINT/(A-Z of source).lower/(YYYY)/(YYYYMMDD)_(A-Z of source)_ENG
#text is between <TEXT> </TEXT> tags after <DOCNO> docid </DOCNO>

#for aquaint2: (A-Z of source)_ENG_(YYYMMDD).(0-9 paragraph ID)
#dataloc/AQUAINT-2/data/"(A-Z of source)_ENG".lower()/"(A-Z of source)_ENG_(YYYYMM)".lower().xml
#text is located similarly, with paragraph tags to be removed

import re, sys, xml.etree.ElementTree as ET


def create_index(root):
        cur = None
        idxes = {}
        for x in range(len(trainroot)):
                cur = str(root[x][2].attrib['id'])
                idxes[cur] = [root[x][2][y].attrib['id'] for y in range(len(root[x][2]))]
        return(idxes)

def dump_train_docs():
        for each in traindocs:
                print("{};{}".format(each,traindocs[each]))

def iter_index(idxes):
        for docset in idxes:
                print("doc set: {}".format(docset))
                for each in idxes[docset]:
                        print(each)

#def apw_2_art(file, 

def return_doc_lines(title):
        path = dataloc + "AQUAINT-2/data/{}/{}.xml".format(title[:7].lower(), title[:-7].lower())
        doc_data = ""
        month_file = open(path, 'r')
        call = False
        collect = False
        art = []
        tag = re.compile('<.*>')
        for line in month_file:
                if "</TEXT>" in line and collect:
                        break
                if collect:
                        if "<P>" in line:
                                art.append([""])
                        #art[-1][-1]+=line.strip()
                        if not tag.match(line):
                                art[-1][-1]+=(" "+line.strip())
                        if ".\n" in line:
                                art[-1].append("")
                        doc_data = doc_data + " {}".format(line.strip())
                if title in line:
                        call = True
                if call and "<TEXT>" in line:
                        collect = True
        month_file.close()
        for paragraph in art:
                print('new paragraph')
                for sentence in paragraph:
                        print('new sentence')
                        print(sentence)
        print(art)
        return(doc_data)

def structure_article(text):
        print(text)
        text = text.replace('</P>',"").split("<P>")
        art = [x.strip().split(". ") for x in text]
        #for each in art:
        #        print(each)

dataloc = "/dropbox/17-18/573/"

training_file = "/dropbox/17-18/573/Data/Documents/training/2009/UpdateSumm09_test_topics.xml"

traintree = ET.parse(training_file)
trainroot = traintree.getroot()

trainidx = create_index(trainroot)
#dump_train_docs()
#iter_index(trainidx)
structure_article(return_doc_lines("APW_ENG_20041001.0331"))
