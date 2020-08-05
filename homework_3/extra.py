import urllib.parse
import urllib.robotparser
from urllib.parse import urlparse
import time

def extract_domain(url):
    domain = urlparse(url).netloc
    return domain

    

def parse_robot(url):
    robotParser = urllib.robotparser.RobotFileParser()
    
    if robotParser.set_url(extract_domain(url) + "/robots.txt") != None:
        robotParser.read()
        crawlDelay = robotParser.crawl_delay("*")
        if crawlDelay == None:
            crawlDelay = 1
        checkURL = robotParser.can_fetch(url, "*")
    else:
        crawlDelay = 1
        checkURL = True
    return checkURL, crawlDelay


tmp =  [ 
"https://en.wikipedia.org/wiki/Hurricane_Katrina",       
"http://www.livescience.com/22522-hurricane-katrina-facts.html",
"https://www.history.com/news/category-5-storms-hurricanes-united-states",
"https://www.facebook.com",
"https://www.google.com"
]