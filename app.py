#!/usr/bin/env python
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
import view
from model import get_distinct_words
from json import dumps as json_encode
from model import is_word
from model import get_word_meta
import model

app = Flask(__name__)

@app.route('/')
def home():
    return view.home()

@app.route('/router')
def router():
    text = request.args['text']
    def is_ref(text):
        return False
    if is_word(text):
        return redirect('/eng/{}'.format(text))
    elif is_ref(text):
        return reidrect('/ref/{}'.format(text))
    else:
        return 'nothing my friend'

@app.route('/eng/<text>')
def eng(text):
    return view.eng(
        word=text,
        meta=get_word_meta(text),
        )

@app.route('/strongs/<number>')
def strongs(number):
    return view.strongs(
        number=number,
        record=model.get_strongs_record(number),
        usage=model.get_strongs_usage(number),
        usage_counts=model.get_strongs_usage_counts(number),
        )

@app.route('/ref')
def ref():
    return str(request.form)

@app.route('/autocomplete_words/<term>')
def autocomplete_words(term):
    return json_encode(list(word for word in get_distinct_words()
        if word.startswith(term.lower())))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
