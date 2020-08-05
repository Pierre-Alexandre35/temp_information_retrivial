## list of seeds urls provided by the professor for this assignment
import urllib.request as requests
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




seedUrls = [ 
"https://en.wikipedia.org/wiki/Hurricane_Katrina",       
"http://www.livescience.com/22522-hurricane-katrina-facts.html",
"https://www.history.com/news/category-5-storms-hurricanes-united-states"
]


import signal
from contextlib import contextmanager

        
##A visited document is a document that has been scored but not yet crawled. The document is stored in one of the buckets. 
visited = set()
crawled = set()
inlinks_dic = defaultdict(list)
outlink_dic = defaultdict(list)
total_crawled = 0

pQueue  = pQueue()

next_buckets = bucket()


## method to check if a given url is returning a 200 server response. If yes, return true otherwise false. 
def urlErrorFree(url):
    try:
        resp = req.head(url)
        if "text/html" in resp.headers["content-type"]:
            if resp.status_code == 200: 
                return True
            else:
                return False
        else:
            return False
        
    except KeyError:
        print(url + " - key error")
        return False
          
    except Exception as e:
        print(str(e))
        return False
    return True


def update_inlink_dic(from_urls, to_url):
    for from_url in from_urls:
            inlinks_dic[from_url.url].append(to_url)

def update_outlink_dic(from_url, to_urls):
    for to_url in to_urls:
        outlink_dic[from_url].append(to_url)
        
def is_crawl_allowed(url):
        robotParser = urllib.robotparser.RobotFileParser()
    if robotParser.set_url(canon.get_domain(url) + "/robots.txt") != None:
        robotParser.read()
        crawlDelay = robotParser.crawl_delay("*")
        if crawlDelay == None:
            crawlDelay = 1
        checkURL = robotParser.can_fetch(canonicalURL, "*")
    else:
        crawlDelay = 1
        checkURL = True
    return checkURL, crawlDelay

            
def retrieve_outlinks(base_node):
    ##The outgoing urls dictionnary is going to store the href of a given link as a key and it's description as a value
    outgoing_nodes = set()
    base_wave = base_node.wave
    base_url = base_node.url
    
    resp = requests.urlopen(base_url)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    
    for link in soup.find_all('a', href=True):
        clean_url = canonical.Canonicalizer().canonicalize(base_url, link['href'])
        if clean_url not in visited and is_crawl_allowed(clean_url):
            visited.add(clean_url)
            score_outgoing_url = get_score(clean_url, link.text)
            current_node = Node(clean_url, base_wave + 1, score_outgoing_url)
            outgoing_nodes.add(current_node)
            outlink_dic[base_url].append(clean_url)
    return outgoing_nodes
        

def insertToQueue(currentBatch):
    for nodes in currentBatch:
        pQueue.insert(nodes)
    
def hash_id(url):
    return str(uuid.uuid3(uuid.NAMESPACE_URL, url))

def ap89_format(hashed_id, url, raw, text, title, headers, outlinks, inlinks):
    
    return f"{os.linesep}".join([
        "<DOC>",
        f"<DOCNO>{hashed_id}</DOCNO>",
        f"<TITLE>{title}</TITLE>",
        f"<URL>{url}</URL>",
        f"<HEADERS>{headers}</HEADERS>",
        f"<OUTLINKS>{outlinks}</OUTLINKS>",
        f"<INLINKS>{inlinks}</INLINKS>",
        "<TEXT>",
        f"{text}",
        "</TEXT>",
        "<RAW>",
        f"{raw}",
        "</RAW>",
        f"</DOC>"
    ])
    
def process(current_node, next_buckets):
    print("ee")
    global total_crawled
    try: 
        outgoing_nodes = retrieve_outlinks(current_node)
        update_inlink_dic(outgoing_nodes, current_node.url)
        next_buckets.insert_nodes(outgoing_nodes)
        total_crawled = total_crawled + 1
        crawled.add(current_node.url)
        with open("crawled.txt", "a") as f:
                f.write(current_node.url + "\n")
        print(total_crawled)
    except Exception as e:
        print(str(e) + " " + current_node.url)
    
    
##  We first start with the seed urls. Then crawl highest scores url's from the queue until the limit is reached.
def crawl(seeds, limit):
    global total_crawled
    with open('crawled.txt') as f:
        content = f.readlines()
        content = [x.strip() for x in content] 
    for item in content:
        crawled.add(item)
    print(len(crawled))
        
    ##A crawled document is a document that has been selected from the queue, processed and stored. Each url visited will be stored in that set in order to avoid to visit the same document > 1. 
    current_bucket = bucket()

    ## explore error-free seed urls first. 
    for seed in seeds:
        if urlErrorFree(seed):
            crawled.add(seed)
            with open("crawled.txt", "a") as f:
                f.write(seed + "\n")
            seed_node = Node(seed, 0, 1)
            nodes = retrieve_outlinks(seed_node)
            update_inlink_dic(nodes, seed)
            current_bucket.insert_nodes(nodes)
            total_crawled = total_crawled + 1

    
    while(total_crawled < 40000):
        global next_buckets 
        next_buckets = bucket()
        while(not current_bucket.isEmpty()):
            current_set = current_bucket.pop_nodes(100)
            pQueue.insert_list(current_set)
            while(pQueue.size() > 0):
                current_node = pQueue.pop()
                time.sleep(1)
                if(total_crawled == 40000):
                    index_documents()
                    break()               
                if urlErrorFree(current_node.url) and (current_node.url not in crawled):
                    process(current_node, next_buckets)
                        
        current_bucket = next_buckets


   
@timeout(1)    
def generateDoc(doc):
    global count
    count= count + 1
    document = Document.Document(doc)
    hashed_id = hash_id(doc)   
    (raw, text, title) = document.getHtml()
    headers = document.getHeader()
    outlinks = outlink_dic[doc]
    inlinks = inlinks_dic[doc]
        
    txt_doc = ap89_format(hashed_id, document.url, raw, text, title, headers, outlinks, inlinks)
        
    doc_txt_location = "documents/" + str(hashed_id) + ".txt" 
         
    with open(doc_txt_location, 'w') as f:
      f.write(txt_doc)
     
    

def index_documents(crawled):
    for doc in crawled[]:
        try: 
            generateDoc(doc[0])
            crawled.remove(doc)
            print("ok")
        except Exception as e:
            print(str(e))
        

        

## Main method that is running the program 
def main():
    ##initialize_es_instance()
    ##store_domains_ranking()
    ##crawl(seedUrls, 40000)


  


## Run the main() method auto 
if __name__== "__main__":
  main()