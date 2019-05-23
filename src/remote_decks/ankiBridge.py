
# try:
import aqt
from aqt.utils import showInfo
# except:
#     apt = None

from .libs.org_to_anki.ankiConnectWrapper.AnkiNoteBuilder import AnkiNoteBuilder
from .libs.org_to_anki.ankiConnectWrapper.AnkiBridge import AnkiBridge as org_AnkiBridge

class AnkiBridge:

    def __init__(self):
        # if (apt != None):
        self.collection = aqt.mw.col
        self.AnkiNoteBuilder = AnkiNoteBuilder()
        self.org_AnkiBridge = org_AnkiBridge()

    ### Helper functions ###
    def _collection():
        return aqt.mw.col
    # def startEditing(self):
    #     self.window().requireReset()
    # def stopEditing(self):
    #     if self.collection() is not None:
    #         self.window().maybeReset()

    ### Core functions
    def createDeck(self, deck):
        # try:
        #     self.startEditing()
        did = aqt.mw.col.decks.id(deck)
        # finally:
        #     self.stopEditing()

        return did

    def addNote(self, note):
        note = self.AnkiNoteBuilder.buildNote(note)
        return self.org_AnkiBridge.addNote(note)

    def deleteNotes(self, noteId):
        # self.startEditing()
        # try:
        aqt.mw.col.remNotes([noteId])

    def updateNoteFields(self, note):

        showInfo("{}".format(note['id']))

        ankiNote = aqt.mw.col.getNote(note['id'])
        showInfo("{}".format(ankiNote))
        if ankiNote is None:
            raise Exception('note was not found: {}'.format(note['id']))

        for name, value in note['fields'].items():
            if name in ankiNote:
                ankiNote[name] = value

        ankiNote.flush()

    # Core current method
    def getDeckNotes(self, deckName):

        cardIds = self._getAnkiCardIdsForDeck(deckName)
        # showInfo("{}".format(cardIds))

        cards = self._getCardsFromIds(cardIds)

        return cards

    def _getAnkiCardIdsForDeck(self, deckName):


        # TODO should check if deck name is in the correct format

        # Make query to Anki
        queryTemplate = "'deck:{}'"

        query = queryTemplate.format(deckName)
        # showInfo("{}".format(query))

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
