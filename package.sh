#!/bin/bash

source orgVersion.txt
if [ -z "${ORG_VERSION}" ]
    then
    echo "No org version found" && exit 1;
fi

GIT_HASH=`git rev-parse --short=7 HEAD`
FILE_NAME="release_${GIT_HASH}_ORG_${ORG_VERSION}.zip"

# Install org_to_anki
./installOrgToAnki.sh

# Remove pycache files and folder
find . -name "*.pyc" -type f -delete
find . -name "*__pycache__" -type d -delete

cd src
zip -r ../${FILE_NAME} __init__.py config.json remote_decks/

cd ..

echo "Relase zip created: $FILE_NAME"
