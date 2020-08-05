import urllib.request as requests

## Class to transform a given link into a ...
class Canonicalizer:
    
    ## check if a given url is absolute or relative
    def is_absolute(self, url):
        return bool(url.startswith("http") or url.startswith("https"))

    def clean_url(self, url):
        clean_url = url.lower
        clean_url = url
    
        #Remove port 80 from http URLs, and port 443 from HTTPS URLs
        if(clean_url.endswith(':80')):
            clean_url = clean_url[:-3]

        if(clean_url.endswith(":243")):
            clean_url= clean_url[:-4]
        
        ##Remove fragment such as:
        ## www.mywebsite.com/team#john-doe -> www.mywebsite.com/team
        clean_url = clean_url.split("#")[0]
        ##fix it
        ##Remove duplicate "/"
        clean_url = requests.urljoin(clean_url,requests.urlparse(clean_url).path.replace('//','/'))
        return clean_url
    

    def canonicalize(self, base, url):
        ## Check if the given url is relative or absolute. If the given url is relative then we would have to recronstruct it's absolute path. 
        if(not self.is_absolute(url)):
            url = requests.urljoin(base, url)
        return self.clean_url(url)
    
