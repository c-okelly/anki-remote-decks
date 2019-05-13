
# try:
import aqt
from aqt.utils import showInfo
# except:
#     apt = None

class AnkiBridge:

    def __init__(self):
        # if (apt != None):
        self.collection = aqt.mw.col

    # Core current method
    def getDeckNotes(self, deckName):

        cardIds = self._getAnkiCardIdsForDeck(deckName)
        showInfo("{}".format(cardIds))

        cards = self._getCardsFromIds(cardIds)

        return cards

    def _getAnkiCardIdsForDeck(self, deckName):


        # TODO should check if deck name is in the correct format

        # Make query to Anki
        queryTemplate = "deck:'{}'"
        query = queryTemplate.format(deckName)
        ids = self.collection.findNotes(query)

        return ids


    def _getCardsFromIds(self, AnkiCardsIds):

        result = []
        for nid in AnkiCardsIds:
            # TODO possible error handling
            note = self.collection.getNote(nid)
            model = note.model()

            fields = {}
            for info in model['flds']:
                order = info['ord']
                name = info['name']
                fields[name] = {'value': note.fields[order], 'order': order}

            result.append({
                'noteId': note.id,
                'tags' : note.tags,
                'fields': fields,
                'modelName': model['name'],
                'cards': self.collection.db.list('select id from cards where nid = ? order by ord', note.id)
            })

        return result
