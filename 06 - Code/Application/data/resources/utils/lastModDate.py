import re
import requests
from bs4 import BeautifulSoup

def getLastModDate():
    # UNIWebConfigs = settings.getUNIWebConfigs()
    url = "http://uniweb.uottawa.ca/sitemap.xml"
    # url = UNIWebConfigs['base_URL']
    requestedUrl = requests.get(url)
    soup = BeautifulSoup(requestedUrl.content,"html.parser")

    # Find all parent object
    urls =  soup.find_all("url")
    IdsAndDates = dict()

    # Iterate through urls list
    for url in urls:
        # for each url look at children
        if 'profile' in url.loc.string:
            #get userId from location element
            userId = re.search('\d+', url.loc.string).group(0)
            #get the lastModification date from lastMod element
            lastModificationDate = url.lastmod.string
            # Add ids and date in a dictionary
            IdsAndDates[userId] = lastModificationDate
    return IdsAndDates
    