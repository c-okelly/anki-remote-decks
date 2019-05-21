
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

from .ankiBridge import AnkiBridge
from .diffAnkiDecks import diffAnkiDecks
from .parseRemoteDeck import getRemoteDeck

# TODO only for quick testing
from .libs.org_to_anki.org_parser.parseData import parse


# TODO => need to get the correct file name

def getCards():

    ankiBridge = AnkiBridge()
    deckName = "0. ListNotes"

    data = ankiBridge.getDeckNotes(deckName)

    showInfo("{}".format(data))

def syncDecks():

    # Get all remote decks from config
    ankiBridge = AnkiBridge()
    deckName = "0. List Notes::test.file"

    # TODO this is nonsense
    currentAnkiDeck = {"result":ankiBridge.getDeckNotes(deckName)}
    orgDeck = parse("/Users/conorokelly/Desktop/Personal_Dev/anki-remote-decks/test/testData/multiple.org")

    # showInfo("currentDeck: {}".format(currentAnkiDeck))
    # showInfo("orgDeck: {}".format(orgDeck))

    deckDiff = diffAnkiDecks(orgDeck, currentAnkiDeck)

    showInfo("deckDiff: {}".format(deckDiff))

    for i in deckDiff["newQuestions"]:
        showInfo("{}".format(i["question"]))

    showInfo("Updated")
    for i in deckDiff["questionsUpdated"]:
        showInfo("{}".format(i["question"]))

    showInfo("Removed")
    for i in deckDiff["removedQuestions"]:
        showInfo("{}".format(i["question"]))




def addNewDeck(url):

    ankiBridge = AnkiBridge()

    showInfo("Getting remote data")
    deck = getRemoteDeck(url)
    showInfo("adding data to deck")

    # TODO Need to ensure the deck has been created
    for q in deck.getQuestions():
        ankiBridge.addNote(q)
