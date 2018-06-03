#!/bin/sh

./convert.py markdown/cv.md -o cv.html --lang en --locale en_US
./convert.py markdown/cv.ja.md -o cv.ja.html --lang ja --locale ja_JP --canonical cv.ja.html
