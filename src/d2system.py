#from lexrank import STOPWORDS, LexRank
#from path import Path
import sys
from lxml import etree
from lxml import html


class Document:
    def __init__(self, docElement):
        self.docElement = docElement
        self.id = docElement.attrib["id"]
        self.isAquaintTwo = '_' in self.id
        self.date = "" #String publish date
        self.filepath = self.createFilepath() #String path
        self.sentences = None #List of String sentences
        self.getSentences()


    def createFilepath(self):
        if self.isAquaintTwo:
            # AQUAINT-2 reference
            affix, dateno = self.id.rsplit("_", 1)[0].lower(), self.id.rsplit("_", 1)[1]
            self.date, doc_no = dateno.split(".")[0], dateno.split(".")[1]
            fn = affix+"_"+self.date[:-2]+".xml"
            self.filepath = "AQUAINT-2/data/"+affix+"/"+fn
        else:
            # AQUAINT-1 reference
            src = self.id[:3]
            year = self.id[3:7]
            self.date = self.id.split(".")[0][3:]
            if src == "NYT":
                fn = self.date+"_"+src
            elif src == "XIE":
                fn = self.date + "_" + "XIN_ENG"
            else:
                fn = self.date + "_" + src + "_ENG"
            self.filepath = "AQUAINT/"+src.lower()+"/"+year+"/"+fn
        return self.filepath


    def getSentences(self):
        textBlock = []
        if self.isAquaintTwo:
            with open(self.filepath, "r") as f:
                new_doc = etree.parse(f)
                target_docs = new_doc.findall("DOC")
                for each in target_docs:
                    if each.attrib["id"] == self.id:
                        # print(self.id+"\n")
                        headline = each.find("HEADLINE")
                        text = each.find("TEXT")
                        try:
                            for paragraph in text.findall("P"):
                                textBlock.append(paragraph.text.strip())
                        except AttributeError:
                            textBlock.append(text.text.strip())
        else: # AQUAINT 1
            with open(self.filepath, "r") as f:
                g = "<root>"+f.read().replace("\n", "")+"</root>"
                new_doc = html.fromstring(g)
                for each in new_doc:
                    if each.tag == "doc":
                        no = each.find("docno")
                        if no.text.strip() == self.id:
                            # print(self.id+"\n")
                            try:
                                for paragraph in each.find("text"):
                                    if paragraph.tag == "p":
                                        textBlock.append(paragraph.text.strip())
                            except AttributeError:
                                text = each.find("text")
                                textBlock.append(text.text.strip())
        # TODO: separate block into sentences                        
        self.sentences = textBlock

class Topic:
    def __init__(self, topicElement):
        self.topicElement = topicElement
        self.id = topicElement.attrib["id"] #String topic id
        self.title = topicElement.find("title").text.strip() #String description
        self.docElements = topicElement.find("docsetA").findall("doc") #List of
        self.docs = [] #List of documents
        self.addDocs()

    def addDocs(self):
        for docElement in self.docElements:
            self.docs.append(Document(docElement))

    def dumpSentences(self):
        return [sent for doc in self.docs for sent in doc.sentences]

class Summarizer:
    def __init__(self, topicElement):
        self.topicElement = topicElement #Topic to be processed
        self.topic = None
        self.makeTopic()

    def makeTopic(self):
        self.topic = Topic(self.topicElement)

    #parses List of Sentences with lexrank to output summary
    def easySummarize(self):
        lexrankDocs = self.topic.dumpSentences()
        print(len(lexrankDocs))
        print("Not Yet Implemented")

    #parses List of sentences with lexrank to output List of ranking scores
    def makeRank(self):
        print("Not Yet Implemented")

    #parses List of rankings and List of sentences to return summary
    def rankSummarize(self, ranking, sentences):
        print("Not Yet Implemented")


class Conductor:
    def __init__(self, itinerary):
        self.itinerary = itinerary #path to .xml file with names of training documents
        self.summarizers = []
        self.makeSummarizers()

    #updates self.topics with Topic objects, using self.itinerary as guidance on how to group data
    def makeSummarizers(self):
        doc = etree.parse(self.itinerary)
        list_of_topic_elements = doc.findall("topic")
        for topicElement in list_of_topic_elements:
            self.summarizers.append(Summarizer(topicElement))


if __name__ == '__main__':
    # TODO: iterate over all xml files
    conductor = Conductor(sys.argv[1])
    print(len(conductor.summarizers))
    for summ in conductor.summarizers:
        summ.easySummarize()





