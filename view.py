from itertools import cycle
from collections import defaultdict
from lib import t
from lib import html5
from lib import url_for
from lib import json_encode

tableau = [
        "#1F77B4",  # blue
        "#AEC7E8",  # light blue
        "#FF7F0E",  # orange
        "#FFBB78",  # light orange
        "#2CA02C",  # green
        "#98DFA8",  # light green
        "#D62728",  # red
        "#FF9896",  # light red
        "#9467BD",  # purple
        "#C5B0D5",  # light purple
        "#8C564B",  # brown
        "#C49C94",  # light brown
        "#E377C2",  # pink
        "#F7B6D2",  # light pink
        "#7F7F7F",  # grey
        "#C7C7C7",  # light grey
        "#BCBD22",  # lime
        "#DBDB8D",  # light lime
        "#17BECF",  # sky
        "#9EDAE5",  # light sky
    ]

colors = tableau[::2]

highlights = tableau[1::2]

def page(content):
    def get_body():
        return t.div(
            t.form(
                t.input(
                    type='textbox',
                    _name='text',
                    placeholder='Type word or reference',
                    ),
                action=url_for('router'),
                _class='flex-col tight',
                ),
            t.div(
                content,
                _class='content',
                ),
            _class='main flex-col',
            )
    return html5(
        css=[
            '/static/flex.css',
            '/static/style.css',
            ],
        js=[
            '/static/jquery.js',
            '/static/Chart.min.js',
            '/static/app.js',
            ],
        metas={
            'viewport': 'initial-scale=1, user-scalable=no',
            },
        body=get_body(),
        title='taproot',
        )


def home():
    def get_content():
        return  t.div('Description of what to do')
    return page(get_content())

def html_encode_utf8(u):
    return u.encode('ascii', 'xmlcharrefreplace')

def eng(word, meta):
    def print_meta(language):
        return t._(
            t.a(
                t.div(
                    t.div(html_encode_utf8(lemma)),
                    t.div(html_encode_utf8(xlit)),
                    t.div(html_encode_utf8(pronounce)),
                    _class='flex-col',
                    ),
                t.div(
                    '{:,}'.format(count),
                    _class='count tight',
                    ),
                href='/strongs/{}'.format(strongs),
                _class='flex-row meta',
                )
            for (
                lemma,
                xlit,
                pronounce,
                lang,
                strongs,
                count
                )in meta if lang == language
            )
    def get_content():
        color = cycle(colors)
        highlight = cycle(highlights)
        def get_data_dict(m):
            lemma, xlit, pro, lang, strongs, count = m
            return dict(
                value=count,
                color=next(color),
                highlight=next(highlight),
                label=lemma,
                )
        def get_lang(lang, show_word=False):
            return t.div(
                t.div(
                    t.div(word, _class='word') if show_word else t._(),
                    print_meta(lang),
                    _class='tight',
                    ),
                t.div(
                    t.canvas(id='chart_{}'.format(lang),
                        width='120', height='120'),
                    t.script('''
                        $(document).ready(function(){{
                            chart_update_{}({});
                            }});
                        '''.format(
                            lang,
                            json_encode(list(
                                get_data_dict(m) for m in meta
                                    if m[-3] == lang)),
                            )
                        ),
                    _class='chart-container',
                    ),
                _class='lang flex-row',
                )
        def divider():
            return t.div(
                'Greek',
                t.div(),
                'Hebrew',
                _class='divider',
                )
        return t.div(
            t.div(word, _class='word'),
            get_lang('greek', show_word=False),
            divider(),
            get_lang('heb'),
            _class='flex-col',
            )
    return page(get_content())

def ref(book, chapter, verse, words):
    _verse = verse
    def get_content():
        verse_words = defaultdict(list)
        for book, chap, verse, word, punc, isItalic, isOp, isCl, strongs in words:
            verse_words[verse].append([
                word,
                punc,
                isOp,
                isCl,
                strongs,
                ])
        return t._(
            t.div('{} {}'.format(book, chapter), _class='book'),
            t._(
                t.div(
                    t.a(str(verse), '&nbsp', _name='{}'.format(verse)),
                    # t.span(str(verse), '&nbsp;'),
                    t.span(
                        t._(
                            t.a(
                                word,
                                href='/strongs/{}'.format(strongs),
                                _class='ref-word-link',
                                ) if strongs else word,
                            punc or '',
                            '(' if isOp else '',
                            ')' if isCl else '',
                            ' ',
                        )
                        for word, punc, isOp, isCl, strongs in words
                        ),
                    _class='verse',
                    )
                for verse, words in sorted(verse_words.items())
                ),
            t.script('''
                scrollToAnchor({});
                '''.format(json_encode(str(_verse)))) if _verse else t._(),
            )
    return page(get_content())

def na(text):
    return page(
        '{} has no strongs number and does not appear to be a valid reference'.format(text))

def strongs(number, record, usage, usage_counts):
    lemma, xlit, pronounce, description, PartOfSpeech, Language = record
    color = cycle(colors)
    highlight = cycle(highlights)
    def get_content():
        def get_words_verses_dict():
            result = defaultdict(list)
            for word, book, chap, verse, text in usage:
                result[word].append(['{} {}:{}'.format(book, chap, verse),
                    text.replace(word, '<b>{}</b>'.format(word))])
            return result
        def get_data_dict(uc):
            word, count = uc
            return dict(
                value=count,
                color=next(color),
                highlight=next(highlight),
                label=word,
                )
        return t.div(
            t.div(
                t.div(
                    t.div(html_encode_utf8(lemma), _class='word'),
                    t.div(html_encode_utf8(xlit)),
                    t.div(html_encode_utf8(pronounce)),
                    t.div(Language),
                    t.div(PartOfSpeech),
                    ),
                t.div(
                    t.div(html_encode_utf8(description)),
                    _class='definition',
                    ),
                _class='flex-row tight strongs'
                ),
            t.div(
                t.div(
                    t._(
                        t.div(
                            t.div(html_encode_utf8(word)),
                            t.div(str(count), _class='count tight'),
                            _class='flex-row tight',
                            )
                        for word, count in usage_counts
                        ),
                    t.div(),
                    _class='flex-col tight',
                    ),
                t.div(
                    t.canvas(id='chart_eng', width='150', height='150'),
                    t.script('''
                        $(document).ready(function(){{
                            chart_update('eng', {});
                            }});
                        '''.format(
                            json_encode(list(
                                get_data_dict(uc) for uc in usage_counts)),
                            )
                        ),
                    _class='chart-container',
                    ),
                _class='flex-row',
                ),
            t.div(
                t._(
                    t.div(
                        t.div(word, _class='verse-word'),
                        t._(
                            t.div(
                                t.div(ref),
                                t.div(text, _class='verse-text'),
                                )
                            for ref, text in verses
                            ),
                        )
                    for word, verses in get_words_verses_dict().items()
                    ),
                _class='verses-container',
                ),
            )
    return page(get_content())
