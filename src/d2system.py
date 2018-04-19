#from path import Path
import sys
from lxml import etree
from lxml import html
from lexrank import STOPWORDS, LexRank


class Document:
    def __init__(self, doc_element):
        self.doc_element = doc_element
        self.id = doc_element.attrib["id"]
        self.is_aquaint_two = '_' in self.id
        self.date = "" #String publish date, set in _create_file_path()
        self.file_path = self._create_file_path() #String path
        self.sentences = self._get_sentences() #List of String sentences

    def __iter__(self):
        return iter(self.sentences)

    def _create_file_path(self):
        if self.is_aquaint_two:
            # AQUAINT-2 reference
            affix, dateno = self.id.rsplit("_", 1)[0].lower(), self.id.rsplit("_", 1)[1]
            self.date, doc_no = dateno.split(".")[0], dateno.split(".")[1]
            file_name = affix+"_"+self.date[:-2]+".xml"
            file_path = "AQUAINT-2/data/"+affix+"/"+file_name
        else:
            # AQUAINT-1 reference
            src = self.id[:3]
            year = self.id[3:7]
            self.date = self.id.split(".")[0][3:]
            if src == "NYT":
                file_name = self.date+"_"+src
            elif src == "XIE":
                file_name = self.date + "_" + "XIN_ENG"
            else:
                file_name = self.date + "_" + src + "_ENG"
            file_path = "AQUAINT/"+src.lower()+"/"+year+"/"+file_name
        return file_path


    def _get_sentences(self):
        text_block = []
        if self.is_aquaint_two:
            with open(self.file_path, "r") as f:
                new_doc = etree.parse(f)
                target_docs = new_doc.findall("DOC")
                for each in target_docs:
                    if each.attrib["id"] == self.id:
                        # print(self.id+"\n")
                        # headline = each.find("HEADLINE")
                        text = each.find("TEXT")
                        try:
                            for paragraph in text.findall("P"):
                                text_block.append(paragraph.text.strip())
                        except AttributeError:
                            text_block.append(text.text.strip())
        else: # AQUAINT 1
            with open(self.file_path, "r") as f:
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
                                        text_block.append(paragraph.text.strip())
                            except AttributeError:
                                text = each.find("text")
                                text_block.append(text.text.strip())
        # TODO: separate block into sentences
        return text_block


class Topic:
    def __init__(self, topic_element):
        self.topic_element = topic_element
        self.id = topic_element.attrib["id"] #String topic id
        self.title = topic_element.find("title").text.strip() #String description
        self.doc_elements = topic_element.find("docsetA").findall("doc") #List of
        self.docs = self._add_docs() #List of documents

    def _add_docs(self):
        docs = []
        for doc_element in self.doc_elements:
            docs.append(Document(doc_element))
        return docs

    def dump_sentences(self):
        return [sent for doc in self.docs for sent in doc.sentences]


class Summarizer:
    def __init__(self, topic_element):
        self.topic_element = topic_element #Topic to be processed
        self.topic = Topic(self.topic_element)

    #parses List of Sentences with lexrank to output summary
    def easy_summarize(self, lexrank_obj):
        lexrank_docs = self.topic.dump_sentences()
        summary = lexrank_obj.get_summary(lexrank_docs, summary_size=2, threshold=.1)
        print(summary)
        # print("Not Yet Implemented")

    #parses List of sentences with lexrank to output List of ranking scores
    def make_rank(self):
        print("Not Yet Implemented")

    #parses List of rankings and List of sentences to return summary
    def rank_summarize(self):
        print("Not Yet Implemented")


class Conductor:
    def __init__(self, itinerary):
        self.itinerary = itinerary #path to .xml file with names of training documents
        self.summarizers = self._make_summarizers()
        self.lexrank_obj = self._make_lexrank_obj()

    #updates self.topics with Topic objects, using self.itinerary as guidance on how to group data
    def _make_summarizers(self):
        summarizers = []
        doc = etree.parse(self.itinerary)
        list_of_topic_elements = doc.findall("topic")
        for topic_element in list_of_topic_elements:
            summarizers.append(Summarizer(topic_element))
        return summarizers

    def _make_lexrank_obj(self):
        idf_docs = [doc for summ in self.summarizers for doc in summ.topic.docs]
        lxr = LexRank(idf_docs, stopwords=STOPWORDS['en'])
        return lxr


if __name__ == '__main__':
    # TODO: iterate over all xml files
    conductor = Conductor(sys.argv[1])
    # print(len(conductor.summarizers))
    for summ in conductor.summarizers:
        summ.easy_summarize(conductor.lexrank_obj)





