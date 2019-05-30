
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

# Project deps
from .diffAnkiDecks import diffAnkiDecks
from .parseRemoteDeck import getRemoteDeck

# Install 3rd party library deps
from .libs.org_to_anki.utils import getAnkiPluginConnector
from .libs.org_to_anki.utils import getAnkiNoteBuilder



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

    # Get config data
    remoteData = ankiBridge.getConfig()

    for deckKey in remoteData["remote-decks"].keys():
        currentRemoteInfo = remoteData["remote-decks"][deckKey]

        # Get Remote deck
        deckName = currentRemoteInfo["deckName"]
        remoteDeck = getRemoteDeck(currentRemoteInfo["url"])

        # Update deckname to one specificed in stored data
        remoteDeck.deckName = deckName

        # Get current deck
        deckName = baseDeck + deckJoiner + deckName
        localDeck = {"result":ankiBridge.getDeckNotes(deckName)}

        # Local deck has no cards
        if localDeck["result"] == []:
            ankiBridge.uploadNewDeck(remoteDeck)
            showInfo("{}".format("Uploading new deck"))
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
    # url = "https://docs.google.com/document/d/e/2PACX-1vRXWGu8WvCojrLqMKsf8dTOWstrO1yLy4-8x5nkauRnMyc4iXrwkwY3BThXHc3SlCYqv8ULxup3QiOX/pub"
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
