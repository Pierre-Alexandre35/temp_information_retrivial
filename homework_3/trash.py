## list of seeds urls provided by the professor for this assignment
import requests

from urllib.parse import urlparse
from bs4 import BeautifulSoup
import Canonicalization as canonical
from scoring import get_score 
from scoring import store_domains_ranking
import requests as req
from Node import Node
from collections import defaultdict
from Buckets import Buckets as bucket
from Pqueue import PriorityQueue as pQueue
import time
import os
import Document
import uuid
from elastic import initialize_es_instance
from elastic import es
import signal
from contextlib import contextmanager
from timeout import timeout


inlinks_dic = defaultdict(list)
outlink_dic = defaultdict(list)

import re

count = 0

        
        
def extract_outlinks(file):
    try: 
        page = file.read()
        matches = re.findall(r'<a[^>]* href="([^"]*)"', page)
        for match in matches:
            clean_url = canonical.Canonicalizer().canonicalize(file, match)
            inlinks_dic[file].append(clean_url)
    except Exception as e:
        print(str(e))



    
    
def crawl():
    count = 0
    for filename in os.listdir("documents"):
        try:
            file = open(os.path.join("documents" + "/" + filename), 'r')
            page = file.read()
            matches = re.findall(r'<a[^>]* href="([^"]*)"', page)
            
            validPage = "<root>" + page + "</root>"
            soup = BeautifulSoup(validPage, 'xml')
            doc_url = soup.find("URL")
            clean_from_url = doc_url.text
            for match in matches:
                clean_outgoing_url = canonical.Canonicalizer().canonicalize(clean_from_url, match)
            inlinks_dic[clean_outgoing_url].append(clean_from_url)
            outlink_dic[clean_from_url].append(clean_outgoing_url)
            count = count + 1
            print(count)
        except Exception as e:
            print(str(e))
            pass
        




crawl()
try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle

with open('dick_one.p', 'wb') as fp:
    pickle.dump(inlinks_dic, fp, protocol=pickle.HIGHEST_PROTOCOL)

with open('dick_two.p', 'wb') as fp:
    pickle.dump(outlink_dic, fp, protocol=pickle.HIGHEST_PROTOCOL)