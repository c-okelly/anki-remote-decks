import sys
sys.path.append('../remote-decks')

from bs4 import BeautifulSoup

from src.remote_decks.parseRemoteDeck import getRemoteDeck
from src.remote_decks.parseRemoteDeck import _download
from src.remote_decks.parseRemoteDeck import _generateOrgListFromHtmlPage
from src.remote_decks.parseRemoteDeck import _parseHtmlPageToAnkiDeck
from src.remote_decks.parseRemoteDeck import _determinePageType
from src.remote_decks.parseRemoteDeck import _extractSpanWithStyles

def testDetermineFileType():

    url = "https://docs.google.com/document/d/e/2PACX-1vRmD3Um10Qvfb2JU0jtPOPXde2RCKPmh3mIMD3aXOZ7T4TfU6CWyPQAHNdrCB8Bo6kuLFplJAOQcbL5/pub"
    urlType = _determinePageType(url)
    assert(urlType == "html")

    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSC0YQI1jw4cNxvMVQl5JsQku-sG7vT-cCr5DDntcoDF7SIo_A7z90Ri5iY9R4V6ngbLsTs-IC0hT_-/pub?output=csv"
    urlType = _determinePageType(url)
    assert(urlType == "csv")

def testGetDeckName():

    testFile = "test/testData/remote_deck_test.html"
    with open(testFile, "r") as f:
        testFileData = f.read()
    
    deck = _parseHtmlPageToAnkiDeck(testFileData)

    assert(deck.deckName == "remote_deck_test")

def testDownloadWebPage():
    url = "https://www.example.com"
    data = _download(url)
    assert(data[0:15] == b'<!doctype html>')


def testParseGoogleDocToOrgFile():

    testFile = "test/testData/remote_deck_test.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    expectedData = ['Test', '# Test', '* Level 1', '** Level 2', '*** Level 3', '**** Level 4', '* Level 1.1', '** Level 2.1']
    orgPage = _generateOrgListFromHtmlPage(testFileData)["data"]
    assert(orgPage == expectedData)



def testParseImagesInGoogleDocs():
    testFile = "test/testData/image_data.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    expectedData = ['* Picture example!', '**  [image=https://lh3.googleusercontent.com/gdEMfGtrSRTvbTiXwysYJ_5XxqieWt0Z9vtFw0jQxOlbjo43_PJYa4kCusZjmkbe_euwGa4KAWEo2xJvEzHkwIpVN3H-XvCxVXCpQNOcH9_tERcVodYf75t18hYlargfKgYtHYvM]']
    orgPage = _generateOrgListFromHtmlPage(testFileData)["data"]
    assert(orgPage == expectedData)

def testParseGoogleDocToAnkiDeck():

    testFile = "test/testData/remote_deck_test.html"
    with open(testFile, "r") as f:
        testFileData = f.read()
    
    deck = _parseHtmlPageToAnkiDeck(testFileData)

    assert(len(deck.getQuestions()) == 2)
    assert(deck.getQuestions()[0].getQuestions() == ["Level 1"])
    assert(deck.getQuestions()[0].getAnswers() == ['Level 2', ['Level 3', ['Level 4']]])
    assert(deck.getQuestions()[1].getQuestions() == ["Level 1.1"])


def testConvertingUrlIntoAnkiDeck():

    url = "https://docs.google.com/document/d/e/2PACX-1vRmD3Um10Qvfb2JU0jtPOPXde2RCKPmh3mIMD3aXOZ7T4TfU6CWyPQAHNdrCB8Bo6kuLFplJAOQcbL5/pub"
    deck = getRemoteDeck(url)

    assert(len(deck.getQuestions()) == 2)
    assert(deck.getQuestions()[0].getQuestions() == ["Level 1"])
    assert(deck.getQuestions()[0].getAnswers() == ['Level 2', ['Level 3', ['Level 4']]])
    assert(deck.getQuestions()[1].getQuestions() == ["Level 1.1"])


def testImageParsing_bugWhereImageIsInsertedTwice():

    testFile = "test/testData/double.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    orgData = _generateOrgListFromHtmlPage(testFileData)

    print(orgData.get("data"))
    assert(orgData.get("data") ==  ['* Question', '** <b> Text 1 </b>', '**  [image=image-1]', '* Question 2', '** Text 2', '**  [image=image-2]', '**  [image=image-3]'])

def testImageParsing_multipleImagesPerAQuestion():

    testFile = "test/testData/double.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    orgData = _generateOrgListFromHtmlPage(testFileData)

    assert(orgData.get("data")[-2] == '**  [image=image-2]')
    assert(orgData.get("data")[-1] == '**  [image=image-3]')


def testParseCssInfo():


    testFile = "test/testData/formatting.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    orgData = _generateOrgListFromHtmlPage(testFileData)
    print(orgData.get("data")[-9:])

    assert(orgData.get("data")[-9:] == ['* Question with bold', '** one <span style="font-weight:700;">Bold </span>one', '** <span style="font-weight:700;">All bold</span>', '** One <span style="text-decoration:underline;">Underlined </span>one', '** One <span style="font-weight:700;font-style:italic;">Italics </span>one', '** One <span style="color:#ff0000;">Red </span>one', '** One <span style="color:#0000ff;">Blue </span>one', '** One <span style="color:#00ff00;">Green </span>one', '** One <span style="color:#ff00ff;">Pink </span>one'])

def test_extractSpanWithStyles():

    listItemText = '<li class="c0"><span>O</span><span>ne </span><span class="c7">Pink </span><span>one</span></li>'
    soupSpan = BeautifulSoup(listItemText, 'html.parser').find_all("span")[2]
    cssStyle = {"c7":['color:#ff00ff;', 'font-weight:700', 'text-decoration:underline']}

    text = _extractSpanWithStyles(soupSpan, cssStyle)

    assert(text == '<span style="color:#ff00ff;;font-weight:700;text-decoration:underline;">Pink </span>')


def testCssRegexParsing():

    css = '.c11{-webkit-text-decoration-skip:none;color:#000000;font-weight:400;text-decoration:underline;vertical-align:baseline;text-decoration-skip-ink:none;font-size:11pt;font-family:"Arial";font-style:normal}'
    
    #TODO finish

def testEmptyBulletPoint():


    #TODO => this will break the cloze for all usecase otherwise
    assert(True)


# TODO write test for C4 and C14 one vs two digites bug