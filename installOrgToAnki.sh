#!/bin/bash
set -xe

source orgVersion.txt
if [ -z "${ORG_VERSION}" ]
    then
    echo "No Version found" && exit 1;
fi

orgToAnkiUrl="https://github.com/c-okelly/org_to_anki/archive/${ORG_VERSION}.zip"

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
