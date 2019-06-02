# anki-remote-decks

[![Build Status](https://travis-ci.org/c-okelly/anki-remote-decks.svg?branch=master)](https://travis-ci.org/c-okelly/anki-remote-deck)

Anki Addon to allow users to create decks in Google docs that can then be synced with Anki. The remote deck acts as the source of truth. When a user syncs their local deck to a remote cards are added / updated / deleted. When cards are updated (excluding the primary field) their history is preserved.

Official Addon => [Anki Remote Decks](https://ankiweb.net/shared/info/911568091)

# This Addon is in Alpha so might easily break but the basic api should remain stable going forward.

# Overview

* This addon is still in beta and so only currenlty supports very basic functionality
* Only Basic cards are currently supported
* More features will come in the future

GIF of adding a new deck
![Basic Example using Google Docs](assets/newDeck.gif)

# Create a new deck

There arre two parts:
* Creating a Google Doc
* Sharing the Google Doc


## Creating Google doc

* Create a new Google Docs page
* Write you Question and Answers in the following format using bullet points

```markdown
# Some comment you don't want included
* Question 1
  * Answer 1
* Question 2
  * Answer 2
```

An example is shown below:

![Google Docs image](assets/exampleDoc.png)

This would produce the following:

  * A deck named test_deck
  * Two basic notes with the assocaited question and answers

## Sharing the Google docs

The Google drive page must be published in order to be publically accessilbe. This is done as follows.

* File > Publish to Web
* Click on the publish button


* The link provided is your key for syncing new decks\

An example published deck [Example Google docs deck](https://docs.google.com/document/d/e/2PACX-1vRXWGu8WvCojrLqMKsf8dTOWstrO1yLy4-8x5nkauRnMyc4iXrwkwY3BThXHc3SlCYqv8ULxup3QiOX/pub)


# Adding the deck to Anki


To add a new remote deck do the following:

* Click on Tools => Manage Remote Decks => Add new remote deck
* Add the url of your remote Deck
* Click ok

New deck will be added to Anki locally

# Adding new content and syncng decks to update with changes

First step is to go to your original Google doc and make the changes you wish to see.
Once saved this can take up to 5 minutes to be published to the public version. Keep checking this until you see you changes

To sync all all current remote decks

* Click on Tools => Manage Remote Decks => Remove remote deck

Gif of adding new content and syncing
![Syncing new content](assets/newQuestion.gif)

# Remove a remote deck

Removed decks are only unlinked to the remote one. The local copy is not deleated.

* Click on Tools => Manage Remote Decks => Add new remote deck

# How does the addon manage changes with note history?

* New notes are added without any history
* Notes removed from the Google docs are removed from the local deck
* If the answer section of a note changes this is update and the history is preserved
* If the question line (primary field) is changed this is regarded as an delate and add new note
  * History is lost for the note

# Contributing

The repo is not really setup up currenty for contributing. 

In order to package the repository run the following scripts. This will generate a zip with the required files for an Anki Addon

```
./installOrgToAnki.sh
./package.sh
```

# Issues

If you have an issue please file a github issues! Thanks

# Future development

No long term road path currently
Image support would be nice though!


