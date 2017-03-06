#!/bin/sh

./convert.py sample/index.md -o index.html --lang en --locale en_US
./convert.py sample/index.ja.md -o index.ja.html --lang ja --locale ja_JP --canonical index.ja.html
