#!/bin/sh

rm -rf app/html
mkdir app/html

# Markdown -> HTML
./convert.py markdown/bio.md -o app/html/bio.html --lang en --locale en_US --canonical bio
./convert.py markdown/bio.ja.md -o app/html/bio.ja.html --lang ja --locale ja_JP --canonical bio.ja

# Assets to app
cp -r assets/* app/html/
cp assets/.htaccess app/html/
