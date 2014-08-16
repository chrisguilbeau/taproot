#!/usr/bin/env python
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
import view

app = Flask(__name__)

@app.route('/')
def home():
    return view.home()

@app.route('/router')
def router():
    text = request.args['text']
    def isRef():
        return False
    if isRef():
        return redirect('/ref')
    else:
        return redirect('/eng/{}'.format(text))

@app.route('/eng/<text>')
def eng(text):
    return str(text)

@app.route('/ref')
def ref():
    return str(request.form)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
