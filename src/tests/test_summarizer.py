import os
import pytest
from lxml import etree

from d3 import d3 as summarizer

VERSION = 'D3'

# Awesome intro documentation
# http://pythontesting.net/framework/pytest/pytest-introduction/


class TestDocument:
    def setup(self):
        self.doc_elements = etree.parse("src/tests/test_document.xml").findall("doc")
        self.doc0 = summarizer.Document(self.doc_elements[0])
        self.doc1 = summarizer.Document(self.doc_elements[1])

    def test_doc0_id(self):
        assert self.doc0.id == "XIN_ENG_20041019.0235"

    def test_doc0_aquaint_bool(self):
        assert self.doc0.is_aquaint_two is True

    def test_doc0_file_path(self):
        assert self.doc0.file_path == "AQUAINT-2/data/xin_eng/xin_eng_200410.xml"

    def test_doc0_sentence_size(self):
        assert len(self.doc0.sentences) == 6

    def test_doc0_sentence_first(self):
        assert self.doc0.sentences[0] == ("Three giant pandas living in Beijing Zoo will be sent to " \
            "Wolong of Sichuan Province, southwest China, Wednesday and three others in Sichuan will "\
            "fly to Beijing Friday, under an exchange program aimed to maintain the biodiversity of the "\
            "giant panda population.")

    def test_doc1_id(self):
        assert self.doc1.id == "XIE19980718.0080"

    def test_doc1_aquaint_bool(self):
        assert self.doc1.is_aquaint_two is False

    def test_doc1_file_path(self):
        assert self.doc1.file_path == "AQUAINT/xie/1998/19980718_XIN_ENG"

    def test_doc1_sentence_size(self):
        assert len(self.doc1.sentences) == 11

    def test_doc1_sentence_last(self):
        assert self.doc1.sentences[-1] == ("Meanwhile, Prime Minister Bill Skate, National Disaster Services "\
            "Chairman Colin Travertz and National Disaster Services Director-General Ludwig Kembu were reported "\
            "to inspect the affected areas Sunday.")


class TestTopic:
    def setup(self):
        self.topic_elements = etree.parse("src/tests/test_topic.xml").findall("topic")
        self.topic0 = summarizer.Topic(self.topic_elements[0])
        self.topic1 = summarizer.Topic(self.topic_elements[1])

    def test_topic0_id(self):
        assert self.topic0.id == "D0907B"

    def test_topic0_title(self):
        assert self.topic0.title == "John Yoo"

    def test_topic0_doc_size(self):
        assert len(self.topic0.doc_elements) == len(self.topic0.docs) == 2

    def test_topic0_dump_sentences(self):
        assert len(self.topic0.dump_sentences()) == 9 + 48

    def test_topic1_id(self):
        assert self.topic1.id == "D1015C"

    def test_topic1_title(self):
        assert self.topic1.title == "Rain Forest Destruction"

    def test_topic1_doc_size(self):
        assert len(self.topic1.doc_elements) == len(self.topic1.docs) == 3

    def test_topic1_dump_sentences(self):
        assert len(self.topic1.dump_sentences()) == 8 + 8 + 4


class TestSummarizer:
    def setup(self):
        self.topic_elements = etree.parse("src/tests/test_conductor.xml").findall("topic")
        self.summ0 = summarizer.Summarizer(self.topic_elements[0])
        self.summ1 = summarizer.Summarizer(self.topic_elements[1])
        self.lxr_obj = summarizer.Conductor(['src/tests/test_conductor.xml',]).lexrank_obj

    def test_summ0_easy_summarize(self):
        self.summ0.easy_summarize(self.lxr_obj)
        assert os.path.isfile('outputs/{0}/D1004-A.M.100.A.8'.format(VERSION))

    def test_summ1_easy_summarize(self):
        self.summ1.easy_summarize(self.lxr_obj)
        assert os.path.isfile('outputs/{0}/D1003-A.M.100.A.8'.format(VERSION))


class TestConductor:
    def setup(self):
        self.conduc0 = summarizer.Conductor(['src/tests/test_conductor.xml', 'src/tests/test_topic.xml'])

    def test_conduc0_summarizer_size(self):
        assert len(self.conduc0.summarizers) == 4
