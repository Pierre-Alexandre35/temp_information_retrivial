from elasticsearch import Elasticsearch
global es
import os
from bs4 import BeautifulSoup
es = Elasticsearch()


# generating a new index in the elastic search instance. Default port for elastic search 9200 // kibana (GUI for elastic search): 5601
def initialize_es_instance():
    try:
        es.indices.create(index="ap_dataset_hw3",
                          body={
                              "settings": {
                                  "number_of_shards": 1,
                                  "number_of_replicas": 1,
                                  "analysis": {
                                      "filter": {
                                          "english_stop": {
                                                "type": "stop",
                                                "stopwords": "_english_"
                                          },
                                          "english_stemmer": {
                                              "type": "stemmer",
                                              "language": "english"
                                          },
                                      },
                                      "analyzer": {
                                                "rebuilt_english": {
                                                    "type": "custom",
                                                    "tokenizer": "standard",
                                                    "filter": [
                                                    "lowercase",
                                                    "english_stop",
                                                    "english_stemmer"
                                                    ]
                                                },
                                      }
                                  }
                              },
                              "mappings": {
                                  "properties": {
                                      "title": {
                                          "type": "text",
                                          "store": True
                                      },
                                      "url": {
                                          "type": "text",
                                          "store": True
                                      },
                                      "headers": {
                                          "type": "text",
                                          "index": False,
                                          "store": True
                                      },
                                      "text": {
                                          "type": "text",
                                          "fielddata": True,
                                          "analyzer": "rebuilt_english",
                                          "index_options": "positions"
                                      },
                                      "raw_html": {
                                          "type": "text",
                                          "fielddata": False,
                                          "index": False,
                                          "store": True
                                      },
                                      "in_links": {
                                          "type": "text",
                                          "index": False,
                                          "store": True
                                      },
                                      "out_links": {
                                          "type": "text",
                                          "index": False,
                                          "store": True
                                      }
                                  }
                              }
                          })
        print("index created with success")
    except Exception as e:
        print("index creation failed...", str(e))



def index_es():
    for filename in os.listdir("documents"):
        try: 
            file = open("documents"+ "/" + filename)
            page = file.read()
            validPage = "<root>" + page + "</root>"
            soup = BeautifulSoup(validPage, 'xml')
            doc_id = soup.find("DOCNO").text
            current_title = soup.find("TITLE").text
            current_url = soup.find("URL").text
            current_headers = soup.find("HEADERS").text
            outlinks = soup.find("OUTLINKS").text
            inlinks = soup.find("INLINKS").text
            current_text = soup.find("TEXT")
            converted_text  = current_text.text.replace('\n','')
            valid_text = "<TEXT>" + converted_text + "</TEXT>" ##
            current_raw = soup.find("RAW") ##
            current_raw = str(current_raw)

        
            jsonDoc = {
            'title': current_title,
            'url': current_url,
            'headers': current_headers,
            'text': valid_text,
            'raw_html': current_raw,
            'in_links': outlinks,
            'out_links': inlinks,
            }
        
            es.index(index="ap_dataset_hw3", doc_type='_doc', id=doc_id, body=jsonDoc)
        
        except Exception as e:
            print(str(e))
            pass