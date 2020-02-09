#!/bin/sh

rm -rf app/html
mkdir app/html

# Markdown -> HTML
./convert.py markdown/cv.md -o app/html/cv.html --lang en --locale en_US --canonical cv
./convert.py markdown/cv.ja.md -o app/html/cv.ja.html --lang ja --locale ja_JP --canonical cv.ja

# Assets to app
cp -pr assets/* app/html/
