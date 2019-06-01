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
    from .remote_decks.main import removeRemoteDeck as rDecks
except:
    QAction = None
    mw = None
    pass
    
def addDeck():

    addNewDeck()

def syncDecks():

    # showInfo("Sync")
    sDecks()

def removeRemote():

    rDecks()

if (QAction != None and mw != None):
    remoteDecksSubMenu = QMenu("Manage remote deck", mw)
    mw.form.menuTools.addMenu(remoteDecksSubMenu)

    # set it to call testFunction when it's clicked
    remoteDeckAction = QAction("Add new remote Deck", mw)
    remoteDeckAction.triggered.connect(addDeck)
    remoteDecksSubMenu.addAction(remoteDeckAction)

    # Sync remote decks
    syncDecksAction = QAction("Sync remote decks", mw)
    syncDecksAction.triggered.connect(syncDecks)
    remoteDecksSubMenu.addAction(syncDecksAction)

    # Remove remote deck
    removeRemoteDeck = QAction("Remove remote deck", mw)
    removeRemoteDeck.triggered.connect(removeRemote)
    remoteDecksSubMenu.addAction(removeRemoteDeck)
