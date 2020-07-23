import sys
sys.path.append('../remote-decks')

from bs4 import BeautifulSoup

from src.remote_decks.parseRemoteDeck import getRemoteDeck
from src.remote_decks.parseRemoteDeck import _download
from src.remote_decks.parseRemoteDeck import _generateOrgListFromHtmlPage
from src.remote_decks.parseRemoteDeck import _parseHtmlPageToAnkiDeck
from src.remote_decks.parseRemoteDeck import _determinePageType
from src.remote_decks.parseRemoteDeck import _extractSpanWithStyles
from src.remote_decks.parseRemoteDeck import _getCssStyles

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
    assert(data[0:15] == '<!doctype html>')


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

    expectedData = ['* Picture example!', '** Before  [image=https://lh6.googleusercontent.com/UqoTBxnML7twdpncSo8yjMSpD4hAHrxLy4qi0H8XUBUxzM22A48PmP3DhOlVgkJZ0e2tDGx6R_901NeRqQDry244HANqLAJl4dlFYihfTAdOmQ11Yd5tIszl5MtosTg7eMJPSLQI] after # height=95.70px, width=114.50px']
    orgPage = _generateOrgListFromHtmlPage(testFileData)["data"]
    print(orgPage)
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

    # print(orgData.get("data"))
    assert(orgData.get("data") == ['* Question', '** <b> Text 1 </b>', '**  [image=image-1] # height=215.04px, width=218.50px', '* Question 2', '** Text 2', '**  [image=image-2] # height=461.33px, width=624.00px', '**  [image=image-3] # height=461.33px, width=624.00px'])

def testCommentLineWithBulletPoint():

    testFile = "test/testData/commentBulletPointLine.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    orgData = _generateOrgListFromHtmlPage(testFileData)

    for i in orgData.get("data"):
        print(i)

    assert(orgData.get("data")[2] == "# type = Cloze") 


def testMultiLineComment():

    pass

def testImageParsing_multipleImagesPerAQuestion():

    testFile = "test/testData/double.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    orgData = _generateOrgListFromHtmlPage(testFileData)

    assert(orgData.get("data")[-2] == '**  [image=image-2] # height=461.33px, width=624.00px')
    assert(orgData.get("data")[-1] == '**  [image=image-3] # height=461.33px, width=624.00px')


def testParseCssInfo():

    testFile = "test/testData/formatting.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    orgData = _generateOrgListFromHtmlPage(testFileData)

    # TODO this is clearly nonsense
    expectedText = ['* Question with bold', '** one <span style="font-weight:700;"> Bold </span>one', '** <span style="font-weight:700;"> All bold </span>', '** One <span style="text-decoration:underline;"> Underlined </span>one', '** One <span style="font-weight:700;font-style:italic;"> Italics </span>one', '** One <span style="color:#ff0000;"> Red </span>one', '** One <span style="color:#0000ff;"> Blue </span>one', '** One <span style="color:#00ff00;"> Green </span>one', '** One <span style="color:#ff00ff;"> Pink </span>one',  '** One <span style="vertical-align:super;"> superscript </span> one', '** One <span style="vertical-align:sub;"> subscript </span> one']
    # print(orgData.get("data"))
    data = orgData.get("data")
    dataLength = len(expectedText)

    i = 0
    while True:
        if data[i] == expectedText[0]:
            break
        i += 1

    # print((orgData.get("data")[i:dataLength+i]))
    assert(orgData.get("data")[i:dataLength+i] == expectedText) 

def test_extractSpanWithStyles():

    listItemText = '<li class="c0"><span>O</span><span>ne </span><span class="c7">Pink </span><span>one</span></li>'
    soupSpan = BeautifulSoup(listItemText, 'html.parser').find_all("span")[2]
    cssStyle = {"c7":['color:#ff00ff', 'font-weight:700', 'text-decoration:underline']}

    text = _extractSpanWithStyles(soupSpan, cssStyle)

    expectedText = '<span style="color:#ff00ff;font-weight:700;text-decoration:underline;"> Pink </span>'
    assert(text == expectedText)


def testCssRegexParsing():

    class MockSoupObjectForCss:
        def __init__(self):
            text = None

    mockCss = MockSoupObjectForCss()
    mockCss.text = '.c11{-webkit-text-decoration-skip:none;color:#001000;font-weight:700;text-decoration:underline;vertical-align:baseline;text-decoration-skip-ink:none;font-size:11pt;font-family:"Arial";font-style:normal}'
    
    cssStyles = _getCssStyles(mockCss)

    assert(cssStyles.get("c11") != None)
    assert(cssStyles.get("c11") == ['color:#001000', 'font-weight:700', 'text-decoration:underline'])

def testCssRegexParsing_ignoresBackGroundColor():

    class MockSoupObjectForCss:
        def __init__(self):
            text = None

    mockCss = MockSoupObjectForCss()
    mockCss.text = '.c11{-webkit-text-decoration-skip:none;color:#001000;font-weight:700;text-decoration:underline;vertical-align:baseline;text-decoration-skip-ink:none;font-size:11pt;font-family:"Arial";font-style:normal;background-color:#fffffff;}'
    
    cssStyles = _getCssStyles(mockCss)

    assert(cssStyles.get("c11") != None)
    print(cssStyles.get("c11"))
    assert(cssStyles.get("c11") == ['color:#001000', 'font-weight:700', 'text-decoration:underline'])


def testEmptyBulletPoint():

    #this will break the cloze otherwise
    testFile = "test/testData/formatting.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    orgData = _generateOrgListFromHtmlPage(testFileData)
    # print(orgData.get("data")[-2:])

    i = 0
    for k in orgData.get("data"):
        if k == "* Empty question":
            break
        i += 1
    # print(orgData.get("data")[i:])
    assert(orgData.get("data")[i:] == ['* Empty question', '** '])

def testCssRegexParsing_getBothTypesOf_C_css():

    # Ensure both cXX and cX fromating is matched. Where is is 0-9
    class MockSoupObjectForCss:
        def __init__(self):
            text = None

    mockCss = MockSoupObjectForCss()
    mockCss.text = '.c11{color:#001000;}'
    cssStyles = _getCssStyles(mockCss)

    assert(cssStyles.get("c11") != None)

    mockCss = MockSoupObjectForCss()
    mockCss.text = '.c1{color:#001000;}'
    cssStyles = _getCssStyles(mockCss)
    assert(cssStyles.get("c1") != None)

def testUnicodeIsRespected():
    testFile = "test/testData/imageInQuestionBug.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    orgData = _generateOrgListFromHtmlPage(testFileData)
    assert(orgData.get("data")[1].strip() == "** Réponse 1")

def testSquareBracketsThrowingError():

    #this will break the cloze otherwise
    testFile = "test/testData/brackets.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    deck = _parseHtmlPageToAnkiDeck(testFileData)
    # print(deck.getQuestions()[0].get)

def testSquareBracketsThrowingError():

    #this will break the cloze otherwise
    testFile = "test/testData/spacesInFormatting.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    orgData = _parseHtmlPageToAnkiDeck(testFileData)
    expectedText = '<span style="font-weight:700;"> Disminuye </span> frecuencia cardiaca'
    actualText = orgData.getQuestions()[0].getAnswers()[0] 
    print(actualText)
    print(len(actualText))
    print(expectedText)
    print(len(expectedText))
    assert(actualText == expectedText)

def testParseWithTableOfContentsAndSections_bothTypes():

    testFile = "test/testData/tableOfContents.html"
    with open(testFile, "r") as f:
        testFileData = f.read()

    expectedData = ['# Section 1', '* subDeck 1', '** Question subDeck a', '*** Answer 1 updated!', '# Section 2', '* subDeck 2', '** Question of subDeck 2', '*** Answer 1 updated!']
    deck = _parseHtmlPageToAnkiDeck(testFileData)
    # for i in deck.getQuestions():
    #     print()
    #     print(i)

    questions = deck.getQuestions()
    assert(len(questions) == 5)
    assert(questions[0].getQuestions()[0] == "Section 1 question")
    assert(questions[1].getQuestions()[0] == "Section 2 question")
    assert(questions[2].getQuestions()[0] == "Section 3.1 question")
    assert(questions[3].getQuestions()[0] == "Section 3.2.1 question")
    assert(questions[4].getQuestions()[0] == "Section 3.2.2 question")

    for i in questions:
        assert(i.getAnswers()[0] == "Answer")

def testLiveRemoteDeck():

    # TODO better assertions on the questions
    deckUrl = "https://docs.google.com/document/d/e/2PACX-1vQawILe70vt1oZCLn9SdyF9Wo0i7-gQ2owGeghXHxhjx9e8_WclLotuU8mFLglZ1QQUDnmBnhRTabte/pub"
    deck = getRemoteDeck(deckUrl)

    questions = deck.getQuestions()

    for i in questions:
        print()
        print(i)

    assert(len(questions) == 11)

    # Question 1 - general
    assert(questions[0].getQuestions()[0] == "Question 1")

    # Question 2 - sublist
    assert(len(questions[1].getAnswers()) == 3)
    assert(len(questions[1].getAnswers()[2]) == 1)

    # Question 3 - tags
    assert(len(questions[2].getTags()) == 3)

    # Question 4 - Cloze question
    assert(questions[3].getParameter("type") == "Cloze")

    # Question 5 - general
    assert("<img src=" in questions[4].getAnswers()[0])

    # Question 6 - formatting
    assert("font-weight:700;" in questions[5].getAnswers()[0])
    assert("text-decoration:underline;" in questions[5].getAnswers()[2])
    assert("color:#ff0000" in questions[5].getAnswers()[4])

    # Question 7 - Special characters
    assert(questions[6].getAnswers()[0] == "å Ä ä Ả ả Ḁ ḁ Ấ ấ Ầ")

    # Question 8 - Special characters
    assert(questions[7].getAnswers()[0] == "你好")

    # Question 9 - image in question
    assert("<img src=" in questions[8].getQuestions()[1])

    # Question 10 - Multi part answer
    assert(len(questions[9].getQuestions()) == 2)

    # Question 10 - Multi part answer
    assert(questions[10].getParameter("type") == "Basic (and reversed card)")