
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

from .diffAnkiDecks import diffAnkiDecks
from .parseRemoteDeck import getRemoteDeck

# TODO replace all imports with external ones
from .libs.org_to_anki.utils import getAnkiPluginConnector

# TODO only for quick testing
from .libs.org_to_anki.org_parser.parseData import parse
from .libs.org_to_anki.ankiConnectWrapper.AnkiNoteBuilder import AnkiNoteBuilder


# TODO => need to get the correct file name

def getCards():

    ankiBridge = getAnkiPluginConnector()
    deckName = "0. ListNotes"

    data = ankiBridge.getDeckNotes(deckName)

    showInfo("{}".format(data))

def syncDecks():

    # Get all remote decks from config
    ankiBridge = getAnkiPluginConnector()
    baseDeck = ankiBridge.defaultDeck
    deckJoiner = "::"

    # TODO replace with a for loop over remotedecks
    testUrl = "https://docs.google.com/document/d/e/2PACX-1vSCONQrUf_aMe79f1D-EKTJ9FJUpirSJAa5EZe2vWFu9dSnBPZzzkYjUYhUZ6oW2I63s5tkFHOEnE5g/pub"
    remoteDeck = {"url": "https://docs.google.com/document/d/e/2PACX-1vRXWGu8WvCojrLqMKsf8dTOWstrO1yLy4-8x5nkauRnMyc4iXrwkwY3BThXHc3SlCYqv8ULxup3QiOX/pub", "deckName": "remote_deck"}
    remoteDeck["url"] = testUrl

    # Main part
    # Get current deck
    deckName = baseDeck + deckJoiner + remoteDeck["deckName"]
    localDeck = {"result":ankiBridge.getDeckNotes(deckName)}

    # Get Remote deck
    remoteDeck = getRemoteDeck(remoteDeck["url"])

    # Diff decks and sync
    deckDiff = diffAnkiDecks(remoteDeck, localDeck)
    _syncNewData(deckDiff)

    # orgDeck = parse("/Users/conorokelly/Desktop/Personal_Dev/anki-remote-decks/test/testData/multiple.org")
    # For testing


def _syncNewData(deckDiff):

    ankiBridge = getAnkiPluginConnector()
    ankiNoteBuilder = AnkiNoteBuilder()

    newQuestion = deckDiff["newQuestions"]
    updatedQuestion = deckDiff["questionsUpdated"]
    removedQuestion = deckDiff["removedQuestions"]

    # Add new question
    for i in newQuestion:
        showInfo("{}".format(i))
        showInfo("{}".format(i["question"]))

        question = i["question"]
        # Need to build question before adding to deck
        builtQuestion = ankiNoteBuilder.buildNote(question)
        ankiBridge.addNote(builtQuestion)
    
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
    # TODO remove hardcoded url
    url = "https://docs.google.com/document/d/e/2PACX-1vRXWGu8WvCojrLqMKsf8dTOWstrO1yLy4-8x5nkauRnMyc4iXrwkwY3BThXHc3SlCYqv8ULxup3QiOX/pub"
    url, okPressed = QInputDialog.getText(mw, "Get Remote Deck url","Remote Deck url:", QLineEdit.Normal, "")
    if okPressed == False:
        return

    # Get data and build deck
    ankiBridge = getAnkiPluginConnector()
    deck = getRemoteDeck(url)
    deckName = deck.deckName

    # Add url to user data
    config = ankiBridge.getConfig()

    if config["remote-decks"].get(url, None) != None:
        showInfo("Decks has already been added for: {}".format(url))
        return
    
    config["remote-decks"][url] = {"url": url, "deckName": deckName}

    # Upload new deck
    ankiBridge.uploadNewDeck(deck)

    # Update config on success
    ankiBridge.writeConfig(config)
