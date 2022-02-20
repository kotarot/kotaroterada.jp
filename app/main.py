#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, render_template, request

from urllib.parse import urlparse, urlunparse

# The Flask application
app = Flask(
    __name__,
    template_folder='templates',
    static_url_path='/static',
    static_folder='static',
)


# Before request
# Redirect to the main domain.
@app.before_request
def redirect_domain():
    parsed = urlparse(request.url)
    if parsed.netloc in ['www.kotaroterada.jp', 'teradakotaro.jp', 'www.teradakotaro.jp']:
        replaced = parsed._replace(netloc='kotaroterada.jp')
        return redirect(urlunparse(replaced), code=301)


# Routings
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bio')
def bio():
    return render_template('bio.html')

@app.route('/bio.ja')
def bio_ja():
    return render_template('bio.ja.html')

@app.route('/cv')
def cv():
    return redirect('/bio', code=302)

@app.route('/cv.ja')
def cv_ja():
    return redirect('/bio.ja', code=302)

# robots.txt
@app.route('/robots.txt')
def robots_txt():
    return app.send_static_file('robots.txt')

@app.route('/humans.txt')
def humans_txt():
    return app.send_static_file('humans.txt')

# Additional Redirects:
# Old psychsheet
@app.route('/psychsheet/ac-2018')
@app.route('/psychsheet/ac-2018.html')
def psychsheet():
    return redirect('https://kotarot.github.io/psych-gen/ac-2018', code=301)


if __name__ == '__main__':
    # [Note]
    # - default host: 127.0.0.1
    # - default port: 5000
    app.run()
