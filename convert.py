#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from BeautifulSoup import BeautifulSoup, Tag
import codecs
import ConfigParser
from markdown import markdown


# Command line args
parser = argparse.ArgumentParser(description='CV Generator')
parser.add_argument('input', nargs=None, default=None, type=str,
                    help='Input Markdown file')
parser.add_argument('--output', '-o', default=None, type=str,
                    help='Output HTML file')
parser.add_argument('--lang', '-l', default='en', type=str,
                    help='Page language')
parser.add_argument('--locale', '-lc', default='en_US', type=str,
                    help='Page locale')
parser.add_argument('--canonical', '-c', default='', type=str,
                    help='Canonical')
args = parser.parse_args()

# Config file
conf = ConfigParser.SafeConfigParser()
conf.read('./cv.conf')

if __name__ == '__main__':

    # markdown -> html
    fin = codecs.open(args.input, mode='r', encoding='utf-8')
    mdtext = fin.read()

    html_md = markdown(text=mdtext, output_format='html5')
    soup_md = BeautifulSoup(html_md)

    # Pre-processing: Wrap <h2> and its followings with <section>
    first_h2 = True
    html_md = soup_md.prettify()
    html_sec = ''
    for line in html_md.split('\n'):
        if '<h2>' in line:
            if first_h2:
                line = line.replace('<h2>', '<section class="block--ends container"><h2>')
                first_h2 = False
            else:
                line = line.replace('<h2>', '</section><section class="block container"><h2>')
        html_sec += line

    # Pre-processing: Add <main> & photo
    html_sec = '<main class="site-main" role="main">' \
             + '<div class="container"><div class="photo-wrap">' \
             + '<img src="photo.jpg" width="240" height="320"></div></div>' \
             + html_sec \
             + '</main>'

    # Into BeautifulSoup
    soup_sec = BeautifulSoup(html_sec)

    # Add "id" in <h2> & Create list of sections for TOC
    sections = []
    for h in soup_sec.findAll('h2'):
        header = h.string.strip()
        id = header.lower().replace(' ', '-')
        h['id'] = id
        sections.append((id, header))

    # Add "id" in <h3>
    for h in soup_sec.findAll('h3'):
        header = h.string.strip()
        id = header.lower().replace(' ', '-')
        h['id'] = id

    # Add TOC at the top and bottom
    html_toc = str(soup_sec).decode('utf-8')
    html_toc = '<header class="site-header" role="banner">' \
             + '<div class="container">' \
             + '<a class="branding" href="./">' \
             + '<h1 class="branding__wordmark">' + conf.get('cv', 'name').decode('utf-8') + '</h1>' \
             + '</a>' \
             + '<nav class="site-nav">' \
             + ''.join(['<a href="#' + s[0] + '">' + s[1] + '</a>' for s in sections]) \
             + '<a href="/">' + conf.get('page', 'homename').decode('utf-8') + '</a>' \
             + '</nav></div></header>' \
             + html_toc \
             + '<footer class="site-footer">' \
             + '<div class="container">' \
             + '<nav class="site-nav">' \
             + ''.join(['<a href="#' + s[0] + '">' + s[1] + '</a>' for s in sections]) \
             + '<a href="/">' + conf.get('page', 'homename').decode('utf-8') + '</a>' \
             + '</nav>' \
             + '<small class="site-credits">' + conf.get('page', 'copyright').decode('utf-8') \
             + '<br>This page is generated using <a href="https://github.com/kotarot/cv-generator">CV Generator</a></small>' \
             + '</div></footer>'

    # Into BeautifulSoup
    soup_toc = BeautifulSoup(html_toc)

    # HTML for <head>
    head_html = '<head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# article: http://ogp.me/ns/article#">' \
              + '<meta charset="UTF-8">' \
              + '<meta http-equiv="X-UA-Compatible" content="IE=Edge">' \
              + '<meta name="viewport" content="width=device-width, initial-scale=1.0">' \
              + '<title>' + conf.get('page', 'title').decode('utf-8') + '</title>' \
              + '<link rel="stylesheet" href="css/screen.css">' \
              + '<link rel="stylesheet" href="style.css">' \
              + '<link rel="canonical" href="' + conf.get('page', 'rooturl').decode('utf-8') + args.canonical + '">' \
              + '<!--[if lt IE 9]>' \
              + '<script src="//oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>' \
              + '<script src="//oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>' \
              + '<![endif]-->' \
              + '<meta name="description" content="' + conf.get('page', 'description').decode('utf-8') + '">' \
              + '<meta name="keywords" content="' + conf.get('page', 'keywords').decode('utf-8') + '">' \
              + '<meta property="og:locale" content="' + args.locale + '">' \
              + '<meta property="og:type" content="website">' \
              + '<meta property="og:title" content="' + conf.get('ogp', 'title').decode('utf-8') + '">' \
              + '<meta property="og:url" content="' + conf.get('page', 'rooturl').decode('utf-8') + args.canonical + '">' \
              + '<meta property="og:description" content="' + conf.get('page', 'description').decode('utf-8') + '">' \
              + '<meta property="og:site_name" content="' + conf.get('ogp', 'sitename').decode('utf-8') + '">' \
              + '<meta property="og:image" content="' + conf.get('page', 'rooturl').decode('utf-8') + 'photo.jpg">' \
              + '</head>'

    # Merge
    soup_html = BeautifulSoup('<!DOCTYPE html><html lang="' + args.lang + '">' + head_html + '<body><div class="site"></div></body></html>')
    soup_html.html.body.div.insert(0, soup_toc)

    # Output html
    html = ''
    # Convert
    #   - "&gt;&lt;script" to ">\n  <script"
    #   - "&gt;&lt;/script" to "></script"
    #   - "&gt;&lt;!" to ">\n  <!"
    # in comments
    for line in soup_html.prettify().split('\n'):
        line = line.replace('&gt;&lt;script', '>\n  <script').replace('&gt;&lt;/script', '></script').replace('&gt;&lt;!', '>\n  <!')
        html += line + '\n'

    # Print or Save to file
    if args.output is None:
        print html
    else:
        fout = codecs.open(args.output, 'w', encoding='utf-8', errors='xmlcharrefreplace')
        fout.write(html.decode('utf-8'))
        print 'Converted: %s -> %s' % (args.input, args.output)
