#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, request


# The Flask application
app = Flask(__name__)


# Routings: Redirects to kotaroterada.jp
@app.before_request
def before_request():
    redirect_from = 'www.kotaroterada.jp'
    redirect_to = 'kotaroterada.jp'
    redirect_url = request.url.replace(redirect_from, redirect_to)
    return redirect(redirect_url, code=301)


if __name__ == '__main__':
    # [Note]
    # - default host: 127.0.0.1
    # - default port: 5000
    app.run()
