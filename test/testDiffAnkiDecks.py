
from src.remote_decks.libs.org_to_anki.org_parser.parseData import parse
from src.remote_decks.libs.org_to_anki.ankiClasses.AnkiQuestion import AnkiQuestion
from src.remote_decks.diffAnkiDecks import diffAnkiDecks

import json

def testNoChanges():

    jsonData = _getAnkiData()
    ankiDeck = parse("test/testData/basic.org")

    deckDiffs = diffAnkiDecks(ankiDeck, jsonData)

    emptyDeckDiff = _getEmtpyDeckDiff()
    assert(deckDiffs == emptyDeckDiff)



def testNoteAdded():

    jsonData = _getAnkiData()
    ankiDeck = parse("test/testData/basic.org")

    # Third note added to deck
    newQuestion = AnkiQuestion("Third Question")
    newQuestion.addAnswer("Third answer")
    ankiDeck.addQuestion(newQuestion)

    deckDiffs = diffAnkiDecks(ankiDeck, jsonData)

    assert(len(deckDiffs.get("newQuestions")) == 1)
    assert(deckDiffs.get("newQuestions")[0]["question"] == newQuestion)

def testNoteRemoved():

    jsonData = _getAnkiData()
    ankiDeck = parse("test/testData/basic.org")
    # Second note missing org data
    ankiDeck._ankiQuestions.pop(1)

    deckDiffs = diffAnkiDecks(ankiDeck, jsonData)

    print(deckDiffs)
    assert(deckDiffs["removedQuestions"][0]["noteId"] == 1502298033751)

def testNoteUpdated():

    jsonData = _getAnkiData()
    ankiDeck = parse("test/testData/basic.org")

    jsonData["result"][1]["fields"]["Back"]["value"] = "changedValue"

    # Second note has been updated
    deckDiffs = diffAnkiDecks(ankiDeck, jsonData)

    deckToBeUpdated = deckDiffs["questionsUpdated"][0]

    assert(deckToBeUpdated["noteId"] == 1502298033751)
    assert(deckToBeUpdated["question"].getAnswers() == ["Second answer"])

def testAllThreeUseCases():

    # First question has been deleted
    # Second question has been updated
    # Third question has been added

    jsonData = _getAnkiData()
    ankiDeck = parse("test/testData/multiple.org")

    deckDiffs = diffAnkiDecks(ankiDeck, jsonData)

    assert(len(deckDiffs["newQuestions"]) == 2)
    assert(len(deckDiffs["questionsUpdated"]) == 1)
    assert(len(deckDiffs["removedQuestions"]) == 1)


def _getAnkiData():

    with open('test/testData/returnAnkiData.json') as json_file:  
        jsonData = json.load(json_file)

    return jsonData

def _getEmtpyDeckDiff():

    return {"newQuestions": [], "questionsUpdated": [], "removedQuestions": []}