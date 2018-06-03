#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from BeautifulSoup import BeautifulSoup, Tag
import codecs
import ConfigParser
from jinja2 import Environment, FileSystemLoader
from markdown import markdown

# This is bad technique, but easy to use
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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

    # If the first element is <p>, wrap it with class="block--end container"
    html_md = soup_md.prettify()
    html_md_lines = html_md.split('\n')
    first_section = True
    if '<p>' in html_md_lines[0]:
        html_md_lines[0] = html_md_lines[0].replace('<p>', '<section class="block--ends container"><p>')
        first_section = False

    # Pre-processing: Wrap <h2> and its followings with <section>
    html_sec = ''
    for line in html_md_lines:
        if '<h2>' in line:
            if first_section:
                line = line.replace('<h2>', '<section class="block--ends container"><h2>')
                first_section = False
            else:
                line = line.replace('<h2>', '</section><section class="block container"><h2>')
        html_sec += line

    # Pre-processing: Add <main> & photo
    html_sec = '<main class="site-main" role="main">' \
             + html_sec \
             + '</main>'
    html_photo = '<div class="container"><div class="gw"><div class="g md-one-half">' \
               + '<div class="photo-wrap"><img src="photo.jpg" width="280" height="280"></div>' \
               + '</div><div class="g md-one-half padding-left-zero">' \
               + '<div class="header-cv">Curriculum Vitae</div>' \
               + '<div class="header-name">' + conf.get('cv', 'name') + '</div>' \
               + '</div></div></div>'
    html_sec = html_sec.replace('{{photo}}', html_photo)

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
    # TODO: These codes should be rewirted with template
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

    # Content with TOC
    content = BeautifulSoup(html_toc).prettify()

    # Jinja template
    env = Environment(loader=FileSystemLoader('./', encoding='utf-8'))
    tpl = env.get_template('cv.tpl')

    page = {
        'lang':        args.lang,
        'title':       conf.get('page', 'title'),
        'canonical':   conf.get('page', 'rooturl') + args.canonical,
        'description': conf.get('page', 'description'),
        'keywords':    conf.get('page', 'keywords'),
        'copyright':   conf.get('page', 'copyright')
    }
    ogp = {
        'locale':   args.locale,
        'title':    conf.get('ogp', 'title'),
        'url':      conf.get('page', 'rooturl') + args.canonical,
        'sitename': conf.get('ogp', 'sitename'),
        'image':    conf.get('page', 'rooturl') + 'photo.jpg'
    }

    # Output html
    html = tpl.render({'page': page, 'ogp': ogp, 'content': content})

    # Print or Save to file
    if args.output is None:
        print html
    else:
        with open(args.output, 'w') as file:
            file.write(html)
            print 'Converted: %s -> %s' % (args.input, args.output)
