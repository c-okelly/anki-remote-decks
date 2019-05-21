# Anki integration class

try:
    # import the main window object (mw) from aqt
    from aqt import mw
    # import the "show info" tool from utils.py
    from aqt.utils import showInfo
    # import all of the Qt GUI library
    from aqt.qt import *
    from aqt.importing import ImportDialog
    from .remote_decks.main import addNewDeck as mainAddNewDeck
    from .remote_decks.main import syncDecks
    from .remote_decks.main import getCards
except:
    QAction = None
    mw = None
    pass
    
def addNewDeck():

    showInfo("addNewDeck")
    url = "https://docs.google.com/document/d/e/2PACX-1vRXWGu8WvCojrLqMKsf8dTOWstrO1yLy4-8x5nkauRnMyc4iXrwkwY3BThXHc3SlCYqv8ULxup3QiOX/pub"

    mainAddNewDeck(url)



def syncDecks():

    showInfo("Sync")



if (QAction != None and mw != None):
    # set it to call testFunction when it's clicked
    remoteDeckAction = QAction("Add new remote Deck", mw)
    remoteDeckAction.triggered.connect(addNewDeck)
    mw.form.menuTools.addAction(remoteDeckAction)

    # Sync remote decks
    syncDecksAction = QAction("Sync remote decks", mw)
    syncDecksAction.triggered.connect(syncDecks)
    mw.form.menuTools.addAction(syncDecksAction)