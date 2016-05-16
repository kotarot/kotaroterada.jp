#!/bin/sh

./convert.py index.md -o index.html --lang en --locale en_US
./convert.py index.ja.md -o index.ja.html --lang ja --locale ja_JP --canonical index.ja.html
