import sys
sys.path.append('../remote-decks')


from src.remote_decks.parseRemoteDeck import getRemoteDeck
from src.remote_decks.parseRemoteDeck import _download
from src.remote_decks.parseRemoteDeck import _generateOrgListFromHtmlPage
from src.remote_decks.parseRemoteDeck import _parseHtmlPageToAnkiDeck
from src.remote_decks.parseRemoteDeck import _determinePageType

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
