
from .libs.org_to_anki.ankiConnectWrapper.AnkiNoteBuilder import AnkiNoteBuilder
from aqt.utils import showInfo

def diffAnkiDecks(orgAnkiDeck, ankiBaseDeck):

    if not isinstance(ankiBaseDeck, dict):
        raise Exception("AnkiBaseDeck, 2nd param, is not dict")

    # Sort 
    storedNotes = {}
    potentialKeys = set()
    for question in ankiBaseDeck.get("result"):
        keyField = _determineKeyField(question)
        potentialKeys.add(keyField)
        key = question.get("fields").get(keyField).get("value")
        storedNotes[key] = question

    # Determine diff
    newQuestions = []
    questionsUpdated = []
    removedQuestions = []

    # Get note Builder
    noteBuilder = AnkiNoteBuilder()
    for question in orgAnkiDeck.getQuestions():
        builtQuestion = noteBuilder.buildNote(question)
        # TODO in future maybe have to different key fields
        keyField = _determineKeyField(builtQuestion)
        key = builtQuestion.get("fields").get(keyField)

        # Check if question exist
        savedQuestion = storedNotes.get(key, None)
        questionAdded = False
        if savedQuestion == None:
            noteId = -1
            newQuestions.append({"question":question, "noteId":noteId})
            questionAdded = True

        if (questionAdded):
            pass
        else:
            # Updated question
            for fields in savedQuestion.get("fields").keys():
                if not (savedQuestion.get("fields").get(fields).get("value") == builtQuestion.get("fields").get(fields)):
                    noteId = savedQuestion["noteId"]
                    questionsUpdated.append({"question":question, "noteId":noteId}) 

    # Find question in Anki that have been deleted from remote source
    for note in storedNotes:
        storedNote = storedNotes.get(note)
        keyField = _determineKeyField(builtQuestion)
        key = storedNote.get("fields").get(keyField)["value"]

        storedQuestionFound = False
        for question in orgAnkiDeck.getQuestions():
            builtQuestion = noteBuilder.buildNote(question)

            if key == builtQuestion["fields"].get(keyField, None):
                storedQuestionFound = True

        if storedQuestionFound == False:
            noteId = storedNote["noteId"]
            removedQuestions.append({"question":storedNote, "noteId":noteId})


    return {"newQuestions": newQuestions, "questionsUpdated": questionsUpdated, "removedQuestions": removedQuestions}



def _determineKeyField(jsonDeck):

    # TODO in future the Front my not be the key field for a note
    return "Front"
