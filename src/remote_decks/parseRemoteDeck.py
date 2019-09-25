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


def _getCssStyles(cssData):

    # Google docs used the following class for lists $c1
    cSectionRegexPattern = "\.c\d{1,2}\{[^\}]+}"
    cssSections = re.findall(cSectionRegexPattern, cssData.text)

    cssStyles = {}
    # for each c section extract critical data
    regexValuePattern = "[;{]:[^;^}\s]+[;}]"
    for section in cssSections:
        name = re.findall("c[\d]+", section)[0]
        color = re.findall("{}{}".format("color", regexValuePattern), section)
        fontStyle = re.findall("{}{}".format("font-style", regexValuePattern), section)
        fontWeight = re.findall("{}{}".format("font-weight", regexValuePattern), section)
        textDecoration = re.findall("{}{}".format("text-decoration", regexValuePattern), section)

        # Ignore default values
        if (len(color) >0 and "color:#000000" in color[0]):
            color = []
        if (len(fontWeight) >0 and "font-weight:400" in fontWeight[0]):
            fontWeight = []
        if (len(fontStyle) >0 and "font-style:normal" in fontStyle[0]):
            fontStyle = []
        if (len(textDecoration) >0 and "text-decoration:none" in textDecoration[0]):
            textDecoration = []

        d = [color, fontStyle, fontWeight, textDecoration]

        styleValues = []
        for i in d:
            if len(i) > 0:
                cleanedStyle = i[0][1:-1]
                styleValues.append(cleanedStyle)
        cssStyles[name] = styleValues

    return cssStyles


def _generateOrgListFromHtmlPage(data):

    orgStar = "*"
    imageTemplate = " [image={}]"
    soup = BeautifulSoup(data, 'html.parser')
    header = soup.find("div", {"id":"header"})
    deckName = header.text
    contents = soup.find("div", {"id":"contents"})

    ## Try and get CSS

    cssData = soup.find_all("style")
    cssStyles = {}
    for css in cssData:
        cssData = soup.find_all("style")[1]
        styleSection = _getCssStyles(cssData)
        cssStyles.update(styleSection)

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
                # Get all spans
                textSpans = i.find_all("span")
                lineOfText = ""
                for span in textSpans:
                    lineOfText += _extractSpanWithStyles(span, cssStyles)

                # Check for images and take first
                images = i.find_all("img")
                if len(images) >= 1:
                    imageText = imageTemplate.format(images[0]["src"])
                    lineOfText += imageText

                itemText.append(lineOfText)

            indentation += 1
            orgStars = (orgStar * indentation)
            for line in itemText:
                formattedListItem = "{} {}".format(orgStars, line)
                orgFormattedFile.append(formattedListItem)


        else:
            pass
            # print("Unknown line type: {}".format(item.name))

    return {"deckName":deckName, "data":orgFormattedFile}

def _extractSpanWithStyles(soupSpan, cssStyles):

    text = soupSpan.text
    classes = soupSpan.attrs.get("class")

    if classes == None:
        return text

    relevantStyles = []
    for clazz in classes:
        if cssStyles.get(clazz) != None:
            for style in cssStyles.get(clazz):
                relevantStyles.append(style)


    if len(relevantStyles) > 0:
        styleAttributes = ""
        for i in relevantStyles:
            styleAttributes += i + ";"
        styledText = '<span style="{}">{}</span>'.format(styleAttributes, text)
        return styledText
    else:
        return text

def _download(url):

    response = requests.get(url)
    if response.status_code == 200:
        data = response.content
    else:
        raise Exception("Failed to get url: {}".format(response.status_code))

    data = data.decode("utf-8")
    data = data.replace("\xa0","")
    return data

if __name__ == "__main__":
    pass
