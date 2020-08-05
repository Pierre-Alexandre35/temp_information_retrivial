import csv
import string
from urllib.parse import urlparse


## This method is only called once. Based on the csv file that ranks the top 100,000 domains from the web based Domain Authority (DA). This method is going to read that csv file and store in in the dictionnary domain_ranking
domain_ranking = {}
def store_domains_ranking():
    with open('domain-ranking.csv', 'r') as rf:
        reader = csv.reader(rf, delimiter=',')
        rank = 1
        for row in reader:
            ## the csv file only stores domains names such as (google.com) since our model is returning urls with the prefix 'www' we must add it to our dictionnary
            domain_ranking["www." + row[1]] = rank
            rank =  rank + 1
    print(rank, "domains indexed")


##List of keywords related to our topics: plurial, synonyms, names
keywords = ["katrina", "hurricane", "hurricanes", "cyclogenesis", "saffir–simpson", "storm", "camille", " pressure", " wind-speed", "harvey", "cyclone", "atlantic", "winds", "wind", "eyewall", "alma", "dennis", "emily", "alice", "otto", "colin", "danielle", "mbar"];

## Check if the anchor description of a given link matches with the context-based keywords 
def keywords_match(url, anchor_description):
    url_words = anchor_description.lower().split(" ")
    count = len([word for word in url_words if word in keywords])
    
    for word in keywords:
        if word in url:
            count = count + 1
            
    if(count == 0):
        return 0
    if(count == 1):
        return 0.7
    if(count == 2):
        return 0.8
    if(count == 3):
        return 0.85
    else:
        return 1

def domain_score(url):
    domain = urlparse(url).netloc
    if not domain.startswith("www"):
        domain = "www." + domain
    domain_authority = 0
    if domain in domain_ranking:
        domain_authority = 1 - (domain_ranking[domain] / 50000)
    if(domain_authority < 0):
        return 0
    return domain_authority



## giving a href link and it's text description, the get_score method is returning a score from 0 (low relevance) to 1 (high relevance)           
def get_score(url, url_description):
    keywords_weighted = 0.95
    domain_weighted = 0.05
    keywords_scr = keywords_match(url, url_description)
    domain_scr = domain_score(url)
    final_score = (keywords_scr * keywords_weighted) + (domain_weighted * domain_scr)
    return round(final_score,2)

