try:
    # import the main window object (mw) from aqt
    from aqt import mw
    # import the "show info" tool from utils.py
    from aqt.utils import showInfo
    # import all of the Qt GUI library
    from aqt.qt import *
except:
    QAction = None
    mw = None
    pass

import requests
import codecs
from bs4 import BeautifulSoup
import re
from .libs.org_to_anki.org_parser.parseData import buildNamedDeck
from .libs.org_to_anki import config

# Should get the remote deck and return an Anki Deck
def getRemoteDeck(url, type):

    # Get remote page
    # TODO Validate url before getting data
    if url.startswith('https://docs.google.com/') and not _UrlEndingIsValid(url):
        raise Exception("Use the Publish link, not the Sharing link")
    pageType = _determinePageType(url)
    deck = None
    if pageType == "html":
        data = _download(url)
        deck = _parseHtmlPageToAnkiDeck(data)

    elif pageType == "csv":

        # TODO need more data from the user about which sheet to get

        # Start with single page usecase
        data = _downloadCSV(url)
        # Get data and ask the user what they want done with it
        _parseCSVFileToDeck(data)

    else:
        raise Exception("url is not a Google doc or csv file")
        
    return deck

def _UrlEndingIsValid(url):

    print(url)
    if url.endswith('pub'):
        return True
    elif url.endswith('pubhtml'):
        return True
    elif url.split("?")[0].endswith('pubhtml'): #TODO Single page usecase remove after
        return True

    return False

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


def _parseCSVFileToDeck(data):

    soup = BeautifulSoup(data, 'html.parser')
    title = soup.find("div", {"id":"doc-title"})
    deckName = title.text

    tableBody = soup.find("tbody")
    tableRows = tableBody.findAll("tr")
    # Get all rows
    allRows = []
    for htmlRow in tableRows:
        row = []
        columns = htmlRow.findAll("td")
        for cell in columns:
            # TODO do we care about formatting?
            cellContents = str(cell.text)
            row.append(cellContents)
        allRows.append(row)

    # TODO does user select the card type?
    
    # Determine card type
    # Check for field name
    for row in allRows:
        if _isSettingsRow(row):
            # Get settings data
            pass
        if _emptyRow(row):
            continue
        print(row)

def _isSettingsRow(row):

    if (len(row) > 0 and len(row[0]) > 0) and row[0].strip()[0] == "#":
        return True
    return False

def _emptyRow(row):

    for i in row:
        if len(i) > 0:
            return False
    return True

def _parseHtmlPageToAnkiDeck(data, lazyLoadImages=False):

    orgData = _generateOrgListFromHtmlPage(data)
    deckName = orgData["deckName"]
    data = orgData["data"]

    # TODO update org_to_anki to have function for this
    # Ensure images are lazy loaded to reduce load
    config.lazyLoadImages = True
    deck = buildNamedDeck(data, deckName)

    return deck


def _getCssStyles(cssData):

    # Google docs used the following class for lists $c1
    cSectionRegexPattern = "\.c\d{1,2}\{[^\}]+}"
    cssSections = re.findall(cSectionRegexPattern, cssData.text)

    cssStyles = {}
    # for each c section extract critical data
    regexValuePattern = ":[^;^}\s]+[;}]"
    startSectionRegex = "[;{]"
    for section in cssSections:
        name = re.findall("c[\d]+", section)[0]
        color = re.findall("{}{}{}".format(startSectionRegex, "color", regexValuePattern), section)
        fontStyle = re.findall("{}{}{}".format(startSectionRegex, "font-style", regexValuePattern), section)
        fontWeight = re.findall("{}{}{}".format(startSectionRegex, "font-weight", regexValuePattern), section)
        textDecoration = re.findall("{}{}{}".format(startSectionRegex, "text-decoration", regexValuePattern), section)
        verticalAlign = re.findall("{}{}{}".format(startSectionRegex, "vertical-align", regexValuePattern), section)

        # Ignore default values
        if (len(color) >0 and "color:#000000" in color[0]):
            color = []
        if (len(fontWeight) >0 and "font-weight:400" in fontWeight[0]):
            fontWeight = []
        if (len(fontStyle) >0 and "font-style:normal" in fontStyle[0]):
            fontStyle = []
        if (len(textDecoration) >0 and "text-decoration:none" in textDecoration[0]):
            textDecoration = []
        if (len(verticalAlign) >0 and "vertical-align:baseline" in verticalAlign[0]):
            verticalAlign = []

        d = [color, fontStyle, fontWeight, textDecoration, verticalAlign]

        styleValues = []
        for i in d:
            if len(i) > 0:
                cleanedStyle = i[0][1:-1]
                styleValues.append(cleanedStyle)
        cssStyles[name] = styleValues

    return cssStyles


def _generateOrgListFromHtmlPage(data):

    orgStar = "*"
    soup = BeautifulSoup(data, 'html.parser')
    title = soup.find("div", {"id":"title"})
    deckName = title.text
    contents = soup.find("div", {"id":"contents"})

    ## Try and get CSS

    cssData = soup.find_all("style")
    cssStyles = {}
    for css in cssData:
        cssData = soup.find_all("style")[1]
        styleSection = _getCssStyles(cssData)
        cssStyles.update(styleSection)

    multiCommentSection = False
    orgFormattedFile = []
    for item in contents:
        # Handle multiLine comment section
        if _startOfMultiLineComment(item):
            multiCommentSection = True
            continue
        elif multiCommentSection and _endOfMultiLineComment(item):
            multiCommentSection = False
            continue
        elif multiCommentSection:
            continue

        # Handle normal line
        if item.name == "p":
            # Get span text
            line = ""
            textSpans = item.find_all("span")
            # print(textSpans)
            for span in textSpans:
                line += span.text

            # Get link text
            linkText = ""
            allLinks = item.find_all("a")
            for link in allLinks:
                text = link.contents
                for t in text:
                    linkText += t

            # Ignore line if span and link text are the same
            if len(line) > 0 and linkText != line:
                orgFormattedFile.append(line)

        # Hanlde list line
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
            imageConfig = ""
            for i in listItems:
                # Get all spans
                textSpans = i.find_all("span")
                lineOfText = ""
                for span in textSpans:
                    lineOfText += _extractSpanWithStyles(span, cssStyles)

                    # Check for images and take first
                    images = span.find_all("img")
                    if len(images) >= 1:
                        imageTemplate = " [image={}]"  # height={}, width={}
                        # Get image styles
                        styles = images[0]["style"]
                        searchRegex = "{}:\s[^;]*;"
                        height = re.findall(searchRegex.format("height"), styles)[0].split(":")[1].replace(";", "").strip()
                        width = re.findall(searchRegex.format("width"), styles)[0].split(":")[1].replace(";", "").strip()
                        imageConfig = " # height={}, width={}".format(height, width)

                        # Build image line
                        imageText = imageTemplate.format(images[0]["src"])
                        lineOfText += imageText

                # Add image metadata at end of line once
                if len(imageConfig) > 0:
                    lineOfText += imageConfig
                    imageConfig = ""

                itemText.append(lineOfText)


            indentation += 1
            orgStars = (orgStar * indentation)
            for line in itemText:
                if (_closeLineBreak(line)):
                    orgFormattedFile.append(line)
                else:
                    formattedListItem = "{} {}".format(orgStars, line)
                    orgFormattedFile.append(formattedListItem)



        else:
            pass
            # print("Unknown line type: {}".format(item.name))

    return {"deckName":deckName, "data":orgFormattedFile}

### Special cases ###
def _closeLineBreak(line):
    # Case to support Cloze cards
    if ("#type=cloze" == line.replace(" ", "").lower()):
        return True 
    return False 
    
def _startOfMultiLineComment(item):
    
    # Get span text
    if item.name == "p":
        line = ""
        sections = item.find_all("span")
        for span in sections:
            line += span.text
        if ("#multilinecommentstart" == line.replace(" ", "").lower()):
            return True 
    return False

def _endOfMultiLineComment(item):
    
    # Get span text
    if item.name == "p":
        line = ""
        sections = item.find_all("span")
        for span in sections:
            line += span.text
        if ("#multilinecommentend" == line.replace(" ", "").lower()):
            return True 
    return False

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
        # Added whitespace around the text. The whitespace is getting stripped somewhere
        text = text.strip()
        styledText = '<span style="{}"> {} </span>'.format(styleAttributes, text)
        return styledText
    else:
        return text

def _downloadCSV(url):

    # TODO Validate that we have a single pace format and html format
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content
    else:
        raise Exception("Failed to get url: {}".format(response.status_code))

    # TODO do we still need this?
    data = data.decode("utf-8")
    # data = data.replace("\xa0"," ")

    return data

def _download(url):

    response = requests.get(url)
    if response.status_code == 200:
        data = response.content
    else:
        raise Exception("Failed to get url: {}".format(response.status_code))

    data = data.decode("utf-8")
    data = data.replace("\xa0"," ")
    return data

if __name__ == "__main__":
    pass
