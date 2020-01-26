#!/bin/bash
set -xe

ankiHome=~/.local/share/Anki2/addons21/911568091

rm release_*.zip
./package.sh

rm $ankiHome/release_*.zip
cp release_*.zip $ankiHome
cd $ankiHome
unzip -o release_*.zip
cd -
