# Anki integration class

try:
# import the main window object (mw) from aqt
    from aqt import mw
    # import the "show info" tool from utils.py
    from aqt.utils import showInfo
    from aqt.utils import shortcut
    # import all of the Qt GUI library
    from aqt.qt import *
    from aqt.importing import ImportDialog
    from .remote_decks.main import addNewDeck
    from .remote_decks.main import syncDecks as sDecks
    from .remote_decks.main import removeRemoteDeck as rDecks
    from .remote_decks.libs.org_to_anki.utils import getAnkiPluginConnector as getConnector
except:
    QAction = None
    mw = None
    pass
    
errorTemplate = """
Hey there! It seems an error has occurred while running.

The error was {}.

If you would like me to fix it please report it here: https://github.com/c-okelly/anki-remote-decks/issues

Please be sure to provide as much information as possible. Specifically the file the caused the error.
"""

def addDeck():

    try:
        ankiBridge = getConnector()
        ankiBridge.startEditing()

        addNewDeck()
    # General exception
    except Exception as e:
        errorMessage = str(e)
        showInfo(errorTemplate.format(errorMessage))
        if ankiBridge.getConfig().get("debug",False) == True:
            trace = traceback.format_exc()
            showInfo(str(trace))

    finally:
        ankiBridge.stopEditing()

def syncDecks():

    try:
        ankiBridge = getConnector()
        ankiBridge.startEditing()
        sDecks()
    # General exception
    except Exception as e:
        errorMessage = str(e)
        showInfo(errorTemplate.format(errorMessage))
        if ankiBridge.getConfig().get("debug",False) == True:
            trace = traceback.format_exc()
            showInfo(str(trace))

    finally:
        showInfo("Sync completed")
        ankiBridge.stopEditing()

def removeRemote():

    try:
        ankiBridge = getConnector()
        ankiBridge.startEditing()

        rDecks()
    # General exception
    except Exception as e:
        errorMessage = str(e)
        showInfo(errorTemplate.format(errorMessage))
        if ankiBridge.getConfig().get("debug",False) == True:
            trace = traceback.format_exc()
            showInfo(str(trace))

    finally:
        ankiBridge.stopEditing()

if (QAction != None and mw != None):
    remoteDecksSubMenu = QMenu("Manage remote deck", mw)
    mw.form.menuTools.addMenu(remoteDecksSubMenu)

    # set it to call testFunction when it's clicked
    remoteDeckAction = QAction("Add new remote Deck", mw)
    remoteDeckAction.setShortcut(QKeySequence("Ctrl+Shift+V"))
    remoteDeckAction.triggered.connect(addDeck)
    remoteDecksSubMenu.addAction(remoteDeckAction)

    # Sync remote decks
    syncDecksAction = QAction("Sync remote decks", mw)
    syncDecksAction.setShortcut(QKeySequence("Ctrl+Shift+S"))
    syncDecksAction.triggered.connect(syncDecks)
    remoteDecksSubMenu.addAction(syncDecksAction)

    # Remove remote deck
    removeRemoteDeck = QAction("Remove remote deck", mw)
    removeRemoteDeck.setShortcut(QKeySequence("Ctrl+Shift+D"))
    removeRemoteDeck.triggered.connect(removeRemote)
    remoteDecksSubMenu.addAction(removeRemoteDeck)
