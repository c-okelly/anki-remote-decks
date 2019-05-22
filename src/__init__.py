# Anki integration class

try:
# import the main window object (mw) from aqt
    from aqt import mw
    # import the "show info" tool from utils.py
    from aqt.utils import showInfo
    # import all of the Qt GUI library
    from aqt.qt import *
    from aqt.importing import ImportDialog
    from .remote_decks.main import addNewDeck
    from .remote_decks.main import syncDecks as sDecks
    from .remote_decks.main import getCards
except:
    QAction = None
    mw = None
    pass
    
def addDeck():

    addNewDeck()

def syncDecks():

    # showInfo("Sync")
    sDecks()


if (QAction != None and mw != None):
    # set it to call testFunction when it's clicked
    remoteDeckAction = QAction("Add new remote Deck", mw)
    remoteDeckAction.triggered.connect(addDeck)
    mw.form.menuTools.addAction(remoteDeckAction)

    # Sync remote decks
    syncDecksAction = QAction("Sync remote decks", mw)
    syncDecksAction.triggered.connect(syncDecks)
    mw.form.menuTools.addAction(syncDecksAction)