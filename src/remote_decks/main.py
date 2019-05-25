
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
from .libs.org_to_anki.utils import getAnkiNoteBuilder

# TODO only for quick testing
from .libs.org_to_anki.org_parser.parseData import parse


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
    testDeckName = "remote_deck"
    rd= {"url": "https://docs.google.com/document/d/e/2PACX-1vRXWGu8WvCojrLqMKsf8dTOWstrO1yLy4-8x5nkauRnMyc4iXrwkwY3BThXHc3SlCYqv8ULxup3QiOX/pub", "deckName": "remote_deck"}
    rd["url"] = testUrl
    rd["deckName"] = testDeckName


    # Get Remote deck
    remoteDeck = getRemoteDeck(rd["url"])
    showInfo("{}".format(remoteDeck))
    remoteDeck.deckName = testDeckName # Remove

    # Get current deck
    deckName = baseDeck + deckJoiner + rd["deckName"]
    localDeck = {"result":ankiBridge.getDeckNotes(deckName)}

    # Local deck is missing
    # TODO check deck exists
    if localDeck == None:
        ankiBridge.uploadNewDeck(remoteDeck)
        return


    # Diff decks and sync
    deckDiff = diffAnkiDecks(remoteDeck, localDeck)
    _syncNewData(deckDiff)

def _syncNewData(deckDiff):

    ankiBridge = getAnkiPluginConnector()
    ankiNoteBuilder = getAnkiNoteBuilder()

    newQuestion = deckDiff["newQuestions"]
    updatedQuestion = deckDiff["questionsUpdated"]
    removedQuestion = deckDiff["removedQuestions"]

    # Add new question
    for i in newQuestion:
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
