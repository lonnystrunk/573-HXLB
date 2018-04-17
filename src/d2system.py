from lexrank import STOPWORDS, LexRank
from path import Path

class Document:
	def __init__(self, name, path=None, pub=None, headline=None, sentences=[]):
		self.name = name #String doc id
		self.path = path #String path
		self.pub = pub #String publish date
		self.sentences = sentences #List of String sentences
		self.headline = headline #String headline

	#adds line to self.sentences
	def addLine(self, sentence):
		self.sentences.append(sentence)

class Topic:
	def __init__(self, name, desc=None, inventory=[], docs=[]):
		self.name = name #String topic id
		self.desc = desc #String description
		self.inventory = inventory #List of String doc ids
		self.docs = docs #List of documents

	def getDocs(self):
		return self.docs

	def addDoc(self, document):
		self.docs.append(document)

class Summarizer:
	def __init__(self, top):
		self.top = top #Topic to be processed

	#return List of sentences of all docs in self.top.docs
	def getSentences(self):
		print("Not Yet Implemented")

	#parses List of Sentences with lexrank to output summary
	def easySummarize(self):
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
		self.tops = []

	#updates self.tops with Topic objects, using self.itinerary as guidance on how to group data
	def makeTopics(self):
		print("Not Yet Implemented")

	#returns text summary for each Topic object
	def makeSummaries(self):
		print("Not Yet Implemented")