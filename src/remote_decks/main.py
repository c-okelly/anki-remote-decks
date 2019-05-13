
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

def getCards():

    ankiBridge = AnkiBridge()
    deckName = "0. ListNotes"

    data = ankiBridge.getDeckNotes(deckName)

    showInfo("{}".format(data))

def syncDecks():

    # Get all remote decks from config

    #
    pass



def addNewDeck(url):

    # add new deck to config
    pass