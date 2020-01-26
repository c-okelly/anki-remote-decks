#!/bin/bash
set -xe

ankiHome=~/.local/share/Anki2/addons21/911568091

rm release_*.zip || true

./package.sh

rm $ankiHome/release_*.zip || true
cp release_*.zip $ankiHome

cd $ankiHome
unzip -o release_*.zip
cd -
