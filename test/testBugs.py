
from src.remote_decks.parseRemoteDeck import getRemoteDeck


def testImageMetadataCommentBug():

    # Load bug deck
    bugDeckUrl = "https://docs.google.com/document/d/e/2PACX-1vTnC8jh3p9rhuq46QrPToWl5HhcjoZt7t7giYrB0pSA834EmGXfautlO9GQsvNOR6lb6-PztfAj34o7/pub"
    deck = getRemoteDeck(bugDeckUrl)

    # Bug is tested by first question in the deck
    # Metadata was being added to multiple questions

    print(deck.getQuestions()[0].getAnswers())
    assert(deck.getQuestions()[0].getAnswers()[2] == "Some more answers")