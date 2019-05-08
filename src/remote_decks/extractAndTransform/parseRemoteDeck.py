import requests
import codecs
from bs4 import BeautifulSoup

def getRemoteDeck(url):


    # Get remote page
    # TODO Validate url before getting data
    pageType = _determinePageType(url)
    if pageType == "html":
        data = _download(url)
        orgPage = _parseHtmlPage(data)

    elif pageType == "csv":
        pass
    else:
        raise Exception("url is not a Google doc or csv file")
        
    return deck

def _determinePageType(url):

    # TODO use url to determine page types
    if (True):
        return "html"
    elif (False):
        return "csv"
    else:
        return None


def _parseHtmlPage(data):

    # htmlFile = codecs.open(data, 'r', "utf-8")
    soup = BeautifulSoup(data, 'html.parser')

    print("soup")
    # print(soup)

def _download(url):

    response = requests.get(url)
    if response.status_code == 200:
        data = response.content
    else:
        raise Exception("Failed to get url: {}".format(response.status_code))

    return data

if __name__ == "__main__":
    pass
