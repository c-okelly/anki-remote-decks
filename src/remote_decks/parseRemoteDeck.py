import requests
import codecs
from bs4 import BeautifulSoup
import re
from .libs.org_to_anki.org_parser.parseData import buildNamedDeck

# Should get the remote deck and return an Anki Deck
def getRemoteDeck(url):

    # Get remote page
    # TODO Validate url before getting data
    pageType = _determinePageType(url)
    deck = None
    if pageType == "html":
        data = _download(url)
        deck = _parseHtmlPageToAnkiDeck(data)

    elif pageType == "csv":
        pass
    else:
        raise Exception("url is not a Google doc or csv file")
        
    return deck

def _determinePageType(url):

    # TODO use url to determine page types
    csvString = "/spreadsheets/"
    documentString = "/document/"
    if (documentString in url):
        return "html"
    elif (csvString in url):
        return "csv"
    else:
        return None


def _parseHtmlPageToAnkiDeck(data):

    orgData = _generateOrgListFromHtmlPage(data)
    deckName = orgData["deckName"]
    data = orgData["data"]

    # TODO update org_to_anki to have function for this
    deck = buildNamedDeck(data, deckName)

    return deck

def _generateOrgListFromHtmlPage(data):

    orgStar = "*"
    imageTemplate = " [image={}]"
    soup = BeautifulSoup(data, 'html.parser')
    header = soup.find("div", {"id":"header"})
    deckName = header.text
    contents = soup.find("div", {"id":"contents"})

    ## Try and get CSS

    cssData = soup.find_all("style")
    if len(cssData) > 0:
        cssData = soup.find_all("style")[1]

        # Get .c sections
        cSectionRegexPattern = "\.c\d{1,2}\w\{[^\}]+}"
        cssSections = re.findall(cSectionRegexPattern, cssData.text)

        # for each c section extract critical data
        for section in cssSections:
            print(section)
            color = re.find()
            fontStyle = None
            fontWeight = None
            textDecoration = None







    orgFormattedFile = []
    for item in contents:
        # print(item)
        if item.name == "p":
            # print("p")
            lineText = item.text
            if len(lineText) > 0:
                orgFormattedFile.append(lineText)

        elif item.name == "ul":
            # print("ul")
            listItems = item.find_all("li")

            # Item class is in the format of "lst-kix_f64mhuyvzb86-1" with last numbers as the level
            classes = item["class"] #.split("-")[-1])
            regexSearch = "^[\w]{3}-[\w]{3,}-[\d]{1,}"
            indentation = -1
            for i in classes:
                if re.match(regexSearch, i) != None:
                    indentation = int(i.split("-")[-1])
            
            if (indentation == -1):
                raise Exception("Could not find the correct indentation")

            itemText = []
            for i in listItems:
                if (len(i.text.strip()) > 0):
                    itemText.append(i.text)

                # Check for single image and take first
                images = i.find_all("img")
                if len(images) >= 1:
                    imageText = imageTemplate.format(images[0]["src"])
                    itemText.append(imageText)

            indentation += 1
            orgStars = (orgStar * indentation)
            for line in itemText:
                formattedListItem = "{} {}".format(orgStars, line)
                orgFormattedFile.append(formattedListItem)


        else:
            pass
            # print("Unknown line type: {}".format(item.name))

    return {"deckName":deckName, "data":orgFormattedFile}

def _download(url):

    response = requests.get(url)
    if response.status_code == 200:
        data = response.content
    else:
        raise Exception("Failed to get url: {}".format(response.status_code))

    return data

if __name__ == "__main__":
    pass
