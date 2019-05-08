import sys
sys.path.append('../remote-decks')


from src.remote_decks.parseRemoteDeck import getRemoteDeck
from src.remote_decks.parseRemoteDeck import _download
from src.remote_decks.parseRemoteDeck import _generateOrgListFromHtmlPage
from src.remote_decks.parseRemoteDeck import _parseHtmlPageToOrgFile

def testDownloadWebPage():
    url = "https://www.example.com"
    data = _download(url)
    assert(data[0:15] == b'<!doctype html>')


def testParseGoogleDocToOrgFile():

    testFile = "test/testData/remote_deck_test.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    expectedData = ['Test', '# Test', '* Level 1', '** Level 2', '*** Level 3', '**** Level 4', '[./remote_deck_test_files/Screenshot 2019-05-01 at 08.27.07.png]', '* Level 1.1', '** Level 2.1']
    orgPage = _generateOrgListFromHtmlPage(testFileData)
    assert(orgPage == expectedData)


def testDetermineFileType():

    # TODO
    pass

# def testDataReturnFromTestDoc():

#     url = "https://docs.google.com/document/d/e/2PACX-1vRmD3Um10Qvfb2JU0jtPOPXde2RCKPmh3mIMD3aXOZ7T4TfU6CWyPQAHNdrCB8Bo6kuLFplJAOQcbL5/pub"
#     data = getRemoteDeck(url)
#     print(data)
#     assert(False)

