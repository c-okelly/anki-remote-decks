
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

remoteDefaultDeck = "Remote Decks"

def syncDecks():

    # Get all remote decks from config
    ankiBridge = getAnkiPluginConnector(remoteDefaultDeck)

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
            showInfo("Deck has no cards. Uploading {}".format(deckName))
        else:
            # Diff decks and sync
            deckDiff = diffAnkiDecks(remoteDeck, localDeck)
            _syncNewData(deckDiff)

def _syncNewData(deckDiff):

    ankiBridge = getAnkiPluginConnector(remoteDefaultDeck)
    ankiNoteBuilder = getAnkiNoteBuilder()

    newQuestion = deckDiff["newQuestions"]
    updatedQuestion = deckDiff["questionsUpdated"]
    removedQuestion = deckDiff["removedQuestions"]

    # Add new question
    duplicateQuestion = 0
    for i in newQuestion:
        question = i["question"]
        try:
            ankiBridge.addNote(question)
        # Catch Duplicate card exceptions otherwise rethrow
        except Exception as e:
            if e.args[0] == "cannot create note because it is a duplicate":
                duplicateQuestion += 1
            else:
                raise e

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
    ankiBridge = getAnkiPluginConnector(remoteDefaultDeck)

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

def removeRemoteDeck():

    # Get current remote decks
    ankiBridge = getAnkiPluginConnector(remoteDefaultDeck)

    config = ankiBridge.getConfig()
    remoteDecks = config["remote-decks"]

    # Get all deck name
    deckNames = []
    for key in remoteDecks.keys():
        deckNames.append(remoteDecks[key]["deckName"])

    if len(deckNames) == 0:
        showInfo("Currently there are no remote decks".format())
        return

    # Ask user to choose a deck
    advBasicOptions = deckNames
    selection, okPressed = QInputDialog.getItem(mw, "Select Deck to Unlink", "Select a deck to Unlink", advBasicOptions, 0, False)

    # Remove desk
    if okPressed == True:

        newRemoteDeck =remoteDecks.copy()
        for k in remoteDecks.keys():
            if selection == remoteDecks[k]["deckName"]:
                newRemoteDeck.pop(k)

        config["remote-decks"] = newRemoteDeck
        # Update config on success
        ankiBridge.writeConfig(config)

    return


def exportCards(deckName):

    pass