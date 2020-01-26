#!/bin/bash
set -xe

ankiHome=~/.local/share/Anki2/addons21/911568091

./package.sh
cp release_*.zip $ankiHome
cd $ankiHome
unzip -o release_*.zip
cd -
