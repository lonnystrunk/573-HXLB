import sys, re, os, xml.etree.ElementTree
import itertools
from xml.dom.minidom import parseString
from lxml import etree
from io import StringIO

# read in guidedSumm10_test_topics.xml as sys.argv[1]
e = xml.etree.ElementTree.parse(sys.argv[1]).getroot()
for atype in e.findall('topic'):
	topicid = atype.get('id')
	id_part1,id_part2 = topicid[:-1], topicid[-1]
	print(id_part1,id_part2)
	
	summary_output = open(id_part1+"-A.M.100."+id_part2+".c",'w')
	
	for a2type in atype.findall('docsetA'):
		for a3type in a2type.findall('doc'):
			docid = a3type.get('id')
			
			if "_" in docid: 
				# use AQUAINT2
				summary_output.write("\n" + docid)
				matchObj = re.match(r'(.{7}).(\d{4})(\d{2})(\d{2})', docid)
				filenm = matchObj.group(1).lower() + "_" + matchObj.group(2) + matchObj.group(3) + ".xml"
				curdir = os.getcwd() + "/AQUAINT-2/data/" + matchObj.group(1).lower() + "/" + filenm
				#print("\t",docid,"A2",curdir)
				
				g = xml.etree.ElementTree.parse(curdir).getroot()
				for d in g.findall('DOC'):
					if d.get('id') == docid:
						for h in d.findall('HEADLINE'):
							summary_output.write(" " + h.text + "\n")

			else: 
				# use AQUAINT
				summary_output.write("\n" + docid)
				matchObj = re.match(r'(\w{3})(\d{4})(\d{2})(\d{2})', docid)
				#print("\t",matchObj.group(1).lower(),matchObj.group(2),matchObj.group(3),matchObj.group(4))

				suffix = "_APW_ENG"
				if matchObj.group(1).replace(" ","") == "XIE": suffix = "_XIN_ENG"
				if matchObj.group(1).replace(" ","") == "NYT": suffix = "_NYT"
				filenm = matchObj.group(2) + matchObj.group(3) + matchObj.group(4) + suffix
				curdir = os.getcwd() + "/AQUAINT/" + matchObj.group(1).lower() + "/" + matchObj.group(2) + "/" + filenm
				
				with open(curdir) as f: 
					new_parser = etree.XMLParser(encoding='utf-8',recover=True)
					root = etree.parse(StringIO('<root>' + f.read().replace('\n', '') +'</root>'), new_parser)
				
				for d in root.findall('DOC'):
					for d2 in d.findall('DOCNO'):
						if d2.text.replace(" ","") == docid: 
							for body in d.findall('BODY'):
								for headline in body.findall('HEADLINE'):
									summary_output.write(" " + headline.text + "\n")


# for EACH topic id (e.g. Columbine Massacre) produce ONE summary file (if topicid is D1001A then filename is D1001-A.M.100.A.something)
# make sure it matches peer file names in ROGUE ???


#(ignore docsetB for testing. maybe use for training)

# evalaute EACH summary using ROGUE 