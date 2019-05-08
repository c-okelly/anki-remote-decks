import sys
sys.path.append('../remote-decks')


from src.remote_decks.extractAndTransform.parseRemoteDeck import getRemoteDeck

def testDataReturnFromTestDoc():

    url = "https://docs.google.com/document/d/1vPooPaIh8jS8lfnogewFW4KmRAJf40O5kr5iLP5qCYM/edit"
    data = getRemoteDeck(url)
    print(data)
    assert(False)

