#!/bin/bash
set -xe


version="master"
orgToAnkiUrl="https://github.com/c-okelly/org_to_anki/archive/{$version}.zip"

mkdir temp || true
rm -rf temp/*
curl -L ${orgToAnkiUrl} -o temp/temp_org_to_anki.zip

# Unzip
unzip temp/temp_org_to_anki -d temp

# Remove current deck and move org_to_anki
rm -rf src/remote_decks/libs/org_to_anki
mv temp/*/src/org_to_anki/ src/remote_decks/libs

# Clean up
rm -rf temp
