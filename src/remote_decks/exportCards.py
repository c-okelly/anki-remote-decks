
def exportDeckOfCards():

    deckName = "deck:Remote Decks::Example Anki Deck"

    # Get all remote decks from config
    ankiBridge = getAnkiPluginConnector("Test")

    deck = {"result":ankiBridge.getDeckNotes(deckName)}

    print(deck)
    return None