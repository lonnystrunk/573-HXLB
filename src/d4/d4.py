import re, pathlib
from lxml import etree
from lxml import html
from lexrank import STOPWORDS, LexRank
import nltk
from datetime import datetime as dt
from numpy import argmax
from takahe import takahe

# GLOBAL VARIABLES
LEXRANK_SUMM_SIZE = 5
LEXRANK_THRESHOLD = 0.1
STEMMING = True
COMPRESS = False


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

    @staticmethod
    def _preprocess(para):
        raw = para.text.strip()
        cleaned = raw.replace("\n", " ")
        cleaned = cleaned.replace("  ", " ")
        cleaned = cleaned.replace("  ", " ")
        return cleaned


    def _get_sentences(self):
        text_block = []
        if self.is_aquaint_two:
            f = open(self.file_path, 'r')
            new_doc = etree.parse(f)
            target_docs = new_doc.findall("DOC")
            for each in target_docs:
                if each.attrib["id"] == self.id:
                    # print(self.id+"\n")
                    # headline = each.find("HEADLINE")
                    text = each.find("TEXT")
                    try:
                        for paragraph in text.findall("P"):
                            cleaned = self._preprocess(paragraph)
                            sentences = nltk.sent_tokenize(cleaned)
                            for sent in sentences:
                                text_block.append(sent)
                    except AttributeError:
                        cleaned = self._preprocess(text)
                        sentences = nltk.sent_tokenize(cleaned)
                        for sent in sentences:
                            text_block.append(sent)
            f.close()
        else: # AQUAINT 1
            f = open(self.file_path, 'r')
            g = "<root>"+f.read().replace("\n", " ")+"</root>"
            new_doc = html.fromstring(g)
            for each in new_doc:
                if each.tag == "doc":
                    no = each.find("docno")
                    if no.text.strip() == self.id:
                        # print(self.id+"\n")
                        try:
                            for paragraph in each.find("text"):
                                if paragraph.tag == "p":
                                    cleaned = self._preprocess(paragraph)
                                    sentences = nltk.sent_tokenize(cleaned)
                                    for sent in sentences:
                                        text_block.append(sent)
                        except AttributeError:
                            text = each.find("text")
                            cleaned = self._preprocess(text)
                            sentences = nltk.sent_tokenize(cleaned)
                            for sent in sentences:
                                text_block.append(sent)
            f.close()
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

    def dump_firsts(self, weight):
        firsts = []
        first = False
        for doc in self.docs:
            first = True
            for sent in doc.sentences:
                if first:
                    firsts.append(weight)
                    first=False
                else:
                    firsts.append(1.0)
        return firsts


    def dump_chrono(self):
        return [doc.date for doc in self.docs for sent in doc.sentences]


class Summarizer:
    def __init__(self, topic_element):
        self.topic_element = topic_element #Topic to be processed
        self.topic = Topic(self.topic_element)

    #parses List of Sentences with lexrank to output summary
    def easy_summarize(self, lexrank_obj):
        lexrank_docs = self.topic.dump_sentences()
        if STEMMING:
            stemmed_decs = self._stemming(lexrank_docs)
            summary_idx = lexrank_obj.get_summary(stemmed_decs, summary_size=LEXRANK_SUMM_SIZE, threshold=LEXRANK_THRESHOLD)
        else:
            summary_idx = lexrank_obj.get_summary(lexrank_docs, summary_size=LEXRANK_SUMM_SIZE, threshold=LEXRANK_THRESHOLD)
        
        summary = [lexrank_docs[x] for x in summary_idx]
        summary_output = open("outputs/D4/" + self.topic.id[:-1] + "-A.M.100." + self.topic.id[-1] + ".8", 'w')

        word_count = 0
        word_count_total = 0
        while word_count <= 100:
            sent = summary[0]
            word_count += len(sent.split())
            if word_count <= 100:
                summary_output.write(sent + "\n")
                word_count_total += len(sent.split())
            summary.pop(0)
        summary_output.close()

    def ordered_summarize(self, lexrank_obj):
        lexrank_docs = self.topic.dump_sentences()
        if STEMMING:
            stemmed_docs = self._stemming(lexrank_docs)
            summary_idx = lexrank_obj.get_summary(stemmed_docs, summary_size=LEXRANK_SUMM_SIZE, threshold=LEXRANK_THRESHOLD)
        else:
            summary_idx = lexrank_obj.get_summary(lexrank_docs, summary_size=LEXRANK_SUMM_SIZE, threshold=LEXRANK_THRESHOLD)
        
        summary_idx = summary_idx.tolist()
        temp_summary = [lexrank_docs[x] for x in summary_idx]
        sent_set = set()
        for temp_sent in temp_summary:
            orig = len(sent_set)
            sent_set.add(temp_sent)
            if len(sent_set) == orig:
                position = temp_summary.index(temp_sent)
                summary_idx.pop(position)

        document = []
        for index in summary_idx:
            document = self.greedy_order(document,index,lexrank_obj,lexrank_docs)
        
        summary = [lexrank_docs[x] for x in document]
        header_pattern = re.compile(r'[A-Z][A-Z][A-Z]+.*[-_] ')
        for temp_sent in summary:
            if re.match(header_pattern, temp_sent) is not None:
                header_sent_position = summary.index(temp_sent)
                summary.insert(0, summary.pop(header_sent_position))
                new_sent = re.sub(header_pattern, "", summary[0])
                summary[0] = new_sent

        if COMPRESS:
            compressed_summary = []
            for i,k in zip(summary[0::2],summary[1::2]):
                if self.compress_sentences(i,k):
                    compressed_summary.append(self.compress_sentences(i,k))
                else:
                    compressed_summary.append(i)
                    compressed_summary.append(k)
            summary = compressed_summary  

        summary_output = open("outputs/D4/" + self.topic.id[:-1] + "-A.M.100." + self.topic.id[-1] + ".8", 'w')
        
        word_count = 0
        word_count_total = 0
        while word_count <= 100:
            if not summary:break
            sent = summary[0]
            word_count += len(sent.split())
            if word_count <= 100:
                summary_output.write(sent + "\n")
                word_count_total += len(sent.split())
            summary.pop(0)
        summary_output.close()

    def compress_sentences(self,sentence1,sentence2):
        sent1 = ' '.join([word + '/' + pos for word,pos in nltk.pos_tag(nltk.word_tokenize(sentence1))])
        sent2 = ' '.join([word + '/' + pos for word,pos in nltk.pos_tag(nltk.word_tokenize(sentence2))])
        sent1 = re.sub(r'/(\.|,)','/PUNCT',sent1)
        sent2 = re.sub(r'/(\.|,)','/PUNCT',sent2)

        compresser = takahe.word_graph([sent1,sent2], nb_words = 15, lang = 'en', punct_tag = "PUNCT" )
        candidates = compresser.get_compression(1)
        for cummulative_score, path in candidates:
            normalized_score = cummulative_score / len(path)
            #print(round(normalized_score, 3), ' '.join([u[0] for u in path]))
            return ' '.join([u[0] for u in path])

    def get_coherence(self,lexrank_obj,document,lexrank_docs):
        n = len(document)
        if n == 1:
            return 0
        else:
            denom = n-1
            sim_sum = 0
            for i in range(n-1):
                sim = lexrank_obj.sentences_similarity(lexrank_docs[document[i]],lexrank_docs[document[i+1]])
                sim_sum += sim
            return sim_sum/denom

    def greedy_order(self,document,index,lexrank_obj,lexrank_docs):
        doc_n = None
        t = 1
        coh_max = -1
        doc_tmp = document[:]
        doc_len = len(document)
        while t <= doc_len+1:
            doc_tmp.insert(t-1,index)
            coh_tmp = self.get_coherence(lexrank_obj,doc_tmp,lexrank_docs)
            if coh_tmp > coh_max:
                doc_n = doc_tmp[:]
                coh_max = coh_tmp
            del doc_tmp[t - 1]
            t += 1
        return doc_n

    # parses List of sentences with lexrank to output List of ranking scores
    def make_rank(self, lexrank_obj):
        lexrank_docs = self.topic.dump_sentences()
        return lexrank_obj.rank_sentences(lexrank_docs, threshold=None, fast_power_method=True)

    # parses List of rankings and List of sentences to return summary
    def chrono_summarize(self, lexrank_obj):
        lexrank_docs = self.topic.dump_sentences()
        chrono = self.topic.dump_chrono()

        if STEMMING:
            stemmed_decs = self._stemming(lexrank_docs)
            summary_idx = lexrank_obj.get_summary(stemmed_decs, summary_size=LEXRANK_SUMM_SIZE,
                                                  threshold=LEXRANK_THRESHOLD)
        else:
            summary_idx = lexrank_obj.get_summary(lexrank_docs, summary_size=LEXRANK_SUMM_SIZE,
                                                  threshold=LEXRANK_THRESHOLD)

        selections = [lexrank_docs[x] for x in summary_idx]
        chrono = [dt.strptime(chrono[x], "%Y%m%d") for x in summary_idx]
        sentences = [x for _, x in sorted(zip(chrono, selections))]
        summary_output = open("outputs/D4/" + self.topic.id[:-1] + "-A.M.100." + self.topic.id[-1] + ".8", 'w')

        word_count = 0
        word_count_total = 0
        while word_count <= 100:
            sent = selections[0]
            word_count += len(sent.split())
            if word_count <= 100:
                summary_output.write(sent + "\n")
                word_count_total += len(sent.split())
            selections.pop(0)
        summary_output.close()

    def test_firsts(self, lexrank_obj, weight, f):
        rankings = self.make_rank(lexrank_obj)
        sents = self.topic.dump_sentences()
        firsts = self.topic.dump_firsts(weight)
        reranked = [rankings[i]*firsts[i] for i in range(len(rankings))]
        word_count = 0
        idxs = []
        while word_count <= 100:
            best_idx = argmax(reranked)
            word_count += len(sents[best_idx].split())
            if word_count <= 100:
                idxs.append(best_idx)
                reranked[best_idx] = float("-inf")
        f.write("weight: {}\n\trankings: {}\n\tfirsts: {}\n\treranked: {}\n".format(weight, [rankings[i] for i in idxs], [firsts[i] for i in idxs], [rankings[i]*firsts[i] for i in idxs]))
        pathlib.Path("outputs/firsts/"+str(weight)).mkdir(parents=True, exist_ok=True)
        c = 0
        t = len(idxs)
        for idx in idxs:
            if firsts[idx] == 1.0:
                c+=1
        selections = [sents[x] for x in idxs]
        sumpath = "outputs/firsts/" + str(weight) + "/" + self.topic.id[:-1] + "-A.M.100." + self.topic.id[-1] + ".8"
        #summary_output = open(sumpath, 'w')
        summary_output = open("outputs/D4/" + self.topic.id[:-1] + "-A.M.100." + self.topic.id[-1] + ".8", 'w')
        summary_output.write('\n'.join(selections))
        summary_output.close()
        return(c,t)

    @staticmethod
    def _stemming(lexrank_docs):
        stemmer = nltk.stem.SnowballStemmer("english")
        stemmed_text = []
        for sent in lexrank_docs:
            tokens = nltk.word_tokenize(sent)
            output = [stemmer.stem(word) for word in tokens]
            stemmed_sent = " ".join(output)
            stemmed_text.append(stemmed_sent)
        return stemmed_text


class Conductor:
    def __init__(self, itinerary):
        self.itineraries = itinerary #path to .xml file with names of training documents
        self.summarizers = self._make_summarizers()
        self.lexrank_obj = self._make_lexrank_obj()

    #updates self.topics with Topic objects, using self.itinerary as guidance on how to group data
    def _make_summarizers(self):
        summarizers = []
        for itinerary in self.itineraries:
            doc = etree.parse(itinerary)
            list_of_topic_elements = doc.findall("topic")
            for topic_element in list_of_topic_elements:
                summarizers.append(Summarizer(topic_element))
        return summarizers

    def _make_lexrank_obj(self):
        idf_docs = [doc for summ in self.summarizers for doc in summ.topic.docs]
        if STEMMING:
            idf_docs = [Summarizer._stemming(doc) for doc in idf_docs]
        lxr = LexRank(idf_docs, stopwords=STOPWORDS['en'])
        # print(lxr._calculate_idf())
        return lxr
