
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
from .libs.org_to_anki.ankiConnectWrapper.AnkiNoteBuilder import AnkiNoteBuilder


# TODO => need to get the correct file name

def getCards():

    ankiBridge = AnkiBridge()
    deckName = "0. ListNotes"

    data = ankiBridge.getDeckNotes(deckName)

    showInfo("{}".format(data))

def syncDecks():

    # Get all remote decks from config
    ankiBridge = AnkiBridge()
    deckName = "0. List Notes::multiple"

    # TODO this is nonsense
    currentAnkiDeck = {"result":ankiBridge.getDeckNotes(deckName)}

    orgDeck = parse("/Users/conorokelly/Desktop/Personal_Dev/anki-remote-decks/test/testData/multiple.org")
    # TODO deck name issues
    # orgDeck.deckName = "0. List Notes::multiple"

    # showInfo("currentDeck: {}".format(currentAnkiDeck))
    # showInfo("orgDeck: {}".format(orgDeck))

    deckDiff = diffAnkiDecks(orgDeck, currentAnkiDeck)

    _syncNewData(deckDiff)

    # showInfo("deckDiff: {}".format(deckDiff))


    # showInfo("New question")
    # for i in deckDiff["newQuestions"]:
    #     showInfo("{}".format(i["question"]))

    # showInfo("Updated")
    # for i in deckDiff["questionsUpdated"]:
    #     showInfo("{}".format(i["question"]))

    # showInfo("Removed")
    # for i in deckDiff["removedQuestions"]:
    #     showInfo("{}".format(i["question"]))


def _syncNewData(deckDiff):

    ankiBridge = AnkiBridge()
    ankiNoteBuilder = AnkiNoteBuilder()

    newQuestion = deckDiff["newQuestions"]
    updatedQuestion = deckDiff["questionsUpdated"]
    removedQuestion = deckDiff["removedQuestions"]

    # Add new question
    for i in newQuestion:
        showInfo("{}".format(i))
        showInfo("{}".format(i["question"]))

        question = i["question"]
        ankiBridge.addNote(question)
    
    # Update existing questions
    for i in updatedQuestion:
        question = i["question"]
        noteId = i["noteId"]

        builtQuestion = ankiNoteBuilder.buildNote(question)
        fields = builtQuestion["fields"]
        note = {"id": noteId, "fields": fields}

        ankiBridge.updateNoteFields(note)

    # Remove questions
    for i in removedQuestion:
        noteId = i["noteId"]
        ankiBridge.deleteNotes(noteId)




def addNewDeck():

    
    # Get url from user
    url = "https://docs.google.com/document/d/e/2PACX-1vRXWGu8WvCojrLqMKsf8dTOWstrO1yLy4-8x5nkauRnMyc4iXrwkwY3BThXHc3SlCYqv8ULxup3QiOX/pub"

    # Add url to user data


    # Get data and build deck
    ankiBridge = AnkiBridge()

    showInfo("Getting remote data")
    deck = getRemoteDeck(url)
    showInfo("adding data to deck")

    # TODO Need to ensure the deck has been created
    deck.deckName = "multiple"
    ankiBridge.createDeck("0. List Notes::multiple")

    for q in deck.getQuestions():
        # TODO needs to be able to handle duplicate cards
        showInfo("{}".format(q))
        ankiBridge.addNote(q)
