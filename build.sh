#!/bin/sh

# Clean up the app directory
rm -rf app/static app/templates
mkdir app/static
mkdir app/templates

# Generation: Markdown -> HTML
./convert.py markdown/bio.md -o app/templates/bio.html --lang en --locale en_US --canonical bio
./convert.py markdown/bio.ja.md -o app/templates/bio.ja.html --lang ja --locale ja_JP --canonical bio.ja

# Move assets to the app
cp -r assets/* app/
cp requirements.txt app/
