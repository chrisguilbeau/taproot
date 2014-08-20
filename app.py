#!/usr/bin/env python
from argparse import ArgumentParser
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
import view
from model import get_distinct_words
from json import dumps as json_encode
from model import is_word
from model import get_word_meta
from model import get_verse_edit_data
from model import make_edit
import model

app = Flask(__name__)

def parse_ref(text):
    if text.count(' ') == 1:
        book, rest = text.split(' ')
        if rest.count(':') == 1:
            chap, verse = rest.split(':')
        else:
            chap = rest
            verse = None
        return book, chap, verse

@app.route('/')
def home():
    return view.home()

@app.route('/router')
def router():
    text = request.args['text']
    if is_word(text):
        return redirect('/eng/{}'.format(text))
    elif parse_ref(text):
        book, chap, verse = parse_ref(text)
        return (
            redirect('/ref/{}/{}/{}'.format(book, chap, verse)) if verse else
            redirect('/ref/{}/{}'.format(book, chap))
            )
    else:
        return redirect('/na/{}'.format(text))

@app.route('/eng/<text>')
def eng(text):
    return view.eng(
        word=text,
        meta=get_word_meta(text),
        )

@app.route('/edit/<book>/<chap>/<verse>', methods=['GET'])
def edit(book, chap, verse):
    return view.edit(
        book=book,
        chap=chap,
        verse=verse,
        data=get_verse_edit_data(book, chap, verse),
        )

@app.route('/edit/<book>/<chap>/<verse>', methods=['POST'])
def makeedit(book, chap, verse):
    form = request.form
    wordId = int(form['wordId'])
    strongsId = form['strongsId'] or None
    make_edit(wordId, strongsId)
    return redirect('/edit/{}/{}/{}'.format(book, chap, verse))

@app.route('/na/<text>')
def na(text):
    return view.na(text)

@app.route('/strongs/<number>')
def strongs(number):
    return view.strongs(
        number=number,
        record=model.get_strongs_record(number),
        usage=model.get_strongs_usage(number),
        usage_counts=model.get_strongs_usage_counts(number),
        )

@app.route('/ref/<book>/<chap>')
@app.route('/ref/<book>/<chap>/<verse>')
def ref(book, chap, verse=None):
    words = model.get_ref_words(book, chap)
    if not words:
        return redirect('/na/{} {}'.format(book, chap))
    book = words[0][0]
    chapter = chap
    return view.ref(
        book = words[0][0],
        chapter = chap,
        verse = verse,
        words = words,
        )

@app.route('/autocomplete_words/<term>')
def autocomplete_words(term):
    return json_encode(list(word for word in get_distinct_words()
        if word.startswith(term.lower())))

if __name__ == '__main__':
    def get_app_desc():
        return 'taproot webserver'
    parser = ArgumentParser(description=get_app_desc(), add_help=False)
    parser.add_argument('-?', '--help', action='help',
        help='show this help message and exit')
    parser.add_argument('-p', metavar='port', type=int,
        default=5000, help='port for the HTTP server (default: 5000)')
    args = parser.parse_args()
    app.run(debug=True, host='0.0.0.0', port=args.p)
