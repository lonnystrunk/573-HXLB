from lxml import etree
from lxml import html

'''
For each topic cluster, finds documents and prints the id and first paragraph of each one
For now, just taking the specs in Ryan's readme very very much for granted 
'''

#topic_cluster_file = sys.argv[1]
topic_cluster_file = "Data/Documents/devtest/GuidedSumm10_test_topics.xml"
# test_file = "test_file.xml"

doc = etree.parse(topic_cluster_file)
# doc = etree.parse(test_file)

list_of_topics = doc.findall("topic")
for topic_em in list_of_topics:
    topic_id = topic_em.attrib["id"]
    id_part2, id_part1 = topic_id[-1], topic_id[:-1]
    title = topic_em.find("title").text.strip()
    print(title+"\n")
    for doc in topic_em.find("docsetA").findall("doc"):
        doc_id = doc.attrib["id"]

        if "_" in doc_id:
            # AQUAINT-2 reference
            affix, dateno = doc_id.rsplit("_", 1)[0].lower(), doc_id.rsplit("_", 1)[1]
            date, doc_no = dateno.split(".")[0], dateno.split(".")[1]
            fn = affix+"_"+date[:-2]+".xml"
            file_path = "AQUAINT-2/data/"+affix+"/"+fn
            with open(file_path, "r") as f:
                new_doc = etree.parse(f)
                target_docs = new_doc.findall("DOC")
                for each in target_docs:
                    if each.attrib["id"] == doc_id:
                        print(doc_id+"\n")
                        headline = each.find("HEADLINE")
                        text = each.find("TEXT")
                        try:
                            first_para = text.findtext("P").strip()
                            print(first_para + "\n")
                        except AttributeError:
                            fp = text.text.strip()
                            print(fp+"\n")



        else:
            # AQUAINT-1 reference
            src = doc_id[:3]
            year = doc_id[3:7]
            date = doc_id.split(".")[0][3:]
            if src == "NYT":
                fn = date+"_"+src
            elif src == "XIE":
                fn = date + "_" + "XIN_ENG"
            else:
                fn = date + "_" + src + "_ENG"
            file_path = "AQUAINT/"+src.lower()+"/"+year+"/"+fn
            with open(file_path, "r") as f:
                g = "<root>"+f.read().replace("\n", "")+"</root>"
                new_doc = html.fromstring(g)
                for each in new_doc:
                    if each.tag == "doc":
                        no = each.find("docno")
                        if no.text.strip() == doc_id:
                            print(doc_id+"\n")
                            try:
                                first_para = each.find("text").findtext("p").strip()
                                print(first_para + "\n")
                            except AttributeError:
                                text = each.find("text")
                                fp = text.text.strip()
                                print(fp+"\n")

# TODO: output summary file, one per topic_id
# TODO: see new announcement for dates beyond 2006??
