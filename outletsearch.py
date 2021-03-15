from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

searchAgain = True

class NewsOutlet:
    def __init__(self, outletName, searchURL, resultCollectionSelector, searchResultHeadlineSelector, searchResultURLSelector, searchTermSpacer,resultPrepend,resultAppend):
        self.outletName = outletName
        self.searchURL = searchURL
        self.resultCollectionSelector = resultCollectionSelector
        self.searchResultURLSelector = searchResultURLSelector
        self.searchResultHeadlineSelector = searchResultHeadlineSelector
        self.searchTermSpacer = searchTermSpacer
        self.resultPrepend = resultPrepend
        self.resultAppend = resultAppend

    def searchThis(self, searchTerm):
        print('- - - - RESULTS FOR {0} - - - -'.format(self.outletName))
        site= self.buildSearchURLComplete(self.buildSearchTerm(searchTerm, self.searchTermSpacer), self.searchURL)
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site,headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page,features="html.parser")
        searchResults = self.doResultCollection(soup, self.resultCollectionSelector)
        if len(searchResults) == 0:
            print(' NO RESULTS FOUND ')
        else:
            for x in searchResults:
                print('-'*30)
                self.printHeadline(x, self.searchResultHeadlineSelector)
                self.printAllSearchResults(x.select((self.searchResultURLSelector)))
        print('')
        print('')

    def printHeadline(self, searchResult, searchResultHeadlineSelector):
        print(searchResult.select_one(searchResultHeadlineSelector).text)

    def doResultCollection(self, pageContent, resultCollectionSelector):
        return pageContent.select(resultCollectionSelector)

    def printAllSearchResults(self, resultsList):
        for i in resultsList:
            print(self.appendToResultURL(self.prependToResultURL(i['href'], self.resultPrepend),self.resultAppend))

    def buildSearchTerm(self,searchTerm, spacer):
        result = re.sub(r' ',spacer,searchTerm)
        return result

    def buildSearchURLComplete(self,searchTerm, searchURL):
        result = re.sub(r'rSearchHere',searchTerm, searchURL)
        return result

    def prependToResultURL(self, resultURL, prependTerm):
        return prependTerm + resultURL

    def appendToResultURL(self, resultURL, appendTerm):
        return resultURL + appendTerm



reuters = NewsOutlet(
            'Reuters',
            "https://www.reuters.com/search/news?blob=rSearchHere",
            '.search-result-indiv',
            '.search-result-title',
            'h3 > a',
            "+",
            'https://www.reuters.com/article',
            ''
        )

wsj = NewsOutlet(
        'Wallstreet Journal',
        "https://www.wsj.com/search?query=rSearchHere",
        '[class^="WSJTheme--search-result"]',
        '[class^="WSJTheme--headline"]',
        '[class^="WSJTheme--headline"] > h3 > a',
        "%20",
        '',
        ''
    )

bloomberg = NewsOutlet(
        'Bloomberg',
        "https://www.bloomberg.com/search?query=rSearchHere",
        '[class^="storyItem__"]',
        '[class^="headline__"]',
        'a',
        "%20",
        '',
        ''
    )

newsOutletList = [
    reuters,
    wsj,
    bloomberg
]

while searchAgain:
    searchTerm = input('Search: ')
    cls()
    for outlet in newsOutletList:
        outlet.searchThis(searchTerm)
