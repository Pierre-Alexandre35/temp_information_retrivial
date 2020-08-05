import os
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import re
import pickle

es = Elasticsearch()


with open('dick_one.p', 'rb') as fp:
    inlinks_dic = pickle.load(fp)

with open('dick_two.p', 'rb') as fp:
    outlinks_dic = pickle.load(fp)
    
for item in outlinks_dic:
    print(outlinks_dic[item])
    
i = 0
path = "documents"
for filename in os.listdir(path):
    try: 
        file = open(path+ "/" + filename)
        page = file.read()
        validPage = "<root>" + page + "</root>"
        soup = BeautifulSoup(validPage, 'html.parser')
        doc_id = soup.find("docno").text
        current_title = soup.find("title").text
        current_url = soup.find("url").text
        current_headers = soup.find("headers").text
        current_text = soup.find("text")
        converted_text  = current_text.text.replace('\n','')
        valid_text = "<TEXT>" + converted_text + "</TEXT>" ##
        current_raw = soup.find("raw") ##
        current_raw = str(current_raw)
        out_links = outlinks_dic[current_url]
        in_links = inlinks_dic[current_url]
        
        jsonDoc = {
            'title': current_title,
            'url': current_url,
            'headers': current_headers,
            'text': valid_text,
            'raw_html': current_raw,
            'in_links': out_links,
            'out_links': in_links,
        }
        
        es.index(index="ap_dataset_hw3", doc_type='_doc', id=doc_id, body=jsonDoc)
        i = i + 1
        print(i)
        
    except Exception as e:
        print(str(e))
        pass
    