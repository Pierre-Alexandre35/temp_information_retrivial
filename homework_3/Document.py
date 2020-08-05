import re
import urllib.request
from bs4 import BeautifulSoup
import os
from scraping import scrap

class Document:
    def __init__(self, url):
        self.url = url
        self.request = urllib.request.urlopen(self.url)
    
    def getDocId(self):
        if self.url.startswith('http'):
            title = re.sub(r'http://', '', self.url)
        if self.url.startswith('https'):
            title = re.sub(r'https://', '', self.url)
        return title or self.url
    
    def getHeader(self):
        return self.request.headers;
    
    
    def getHtml(self):
        html_doc = self.request.read()
        if : 
            title = str(html_doc).split('<title>')[1].split('</title>')[0]
        except Exception:
            title = ""
        text_doc = scrap(html_doc)
        
        return (html_doc, text_doc, title)
    



        
        








    
    