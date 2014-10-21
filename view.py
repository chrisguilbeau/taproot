from itertools import cycle
from collections import defaultdict
from lib import t
from lib import html5
from lib import url_for
from lib import json_encode
from lib import json_decode

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
                    autocomplete='off',
                    spellcheck='off',
                    dir='auto',
                    onkeydown='''
                        if (event.which == 13)
                            $('form').submit();
                        ''',
                    placeholder='Chapter, Verse, or Word',
                    ),
                t.input(type='submit', style='display:none;'),
                action=url_for('router'),
                _class='tight search-form',
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
            '/static/typeahead.js',
            '/static/app.js',
            ],
        metas={
            'viewport': 'initial-scale=1, user-scalable=no',
            'apple-mobile-web-app-capable': 'yes',
            },
        extras=[
            t.link(rel='shortcut icon', href='/static/taproot.ico'),
            ],
        body=get_body(),
        title='taproot',
        )

def edit(book, chap, verse, data):
    def get_content():
        return t._(
            t.div(
                t.form(
                    word,
                    t.input(type='hidden', _name='wordId', value=str(wordId)),
                    t.input(type='text', _name='strongsId', value=strongsId or ''),
                    t.input(type='submit'),
                    method='POST',
                    ),
                )
            for wordId, word, strongsId in data
            )
    return page(get_content())

def editStr(strongsId, strongs, data):
    lemma, xlit, pron, desc, pos, lang = strongs
    words = defaultdict(list)
    for word, book, chap, verse, text in data:
        words[word].append((book, chap, verse, text))
    def get_content():
        def getPrev():
            base = str(int(strongsId[1:]) - 1)
            return ''.join([lang[0].upper(), base])
        def getNext():
            base = str(int(strongsId[1:]) + 1)
            return ''.join([lang[0].upper(), base])
        prev = getPrev()
        _next = getNext()
        return t._(
            t.div(
                t.a(_next, href='/editStr/{}'.format(prev)),
                t.span(' << '),
                strongsId,
                t.span(' >> '),
                t.a(_next, href='/editStr/{}'.format(_next)),
                ),
            t.div(html_encode_utf8(xlit)),
            t.div(html_encode_utf8(lemma)),
            t.div(html_encode_utf8(desc)),
            t._(
                t.div(
                    t.h2(word),
                    t._(
                        t.div(
                            t.a(
                                '{} {}:{} - '.format(book, chap, verse),
                                text,
                                href='/edit/{}/{}/{}'.format(
                                    book, chap, verse
                                    ),
                                ),
                            )
                        for book, chap, verse, text in metas),
                    )
                for word, metas in words.iteritems()
                )
            )
    return page(get_content())


def home():
    def get_content():
        return  t.div('''
            Try a word like faith, hope or love. Try a reference
            like Gen 1, Matthew 28, or John 3:16.
            ''')
    return page(get_content())

def html_encode_utf8(u):
    return u.encode('ascii', 'xmlcharrefreplace')

def eng(word, meta):
    def print_meta(language):
        color = cycle(colors)
        return t._(
            t.a(
                t.div(
                    t.div(html_encode_utf8(
                            json_decode(json)['pronun']['sbl'])),
                    t.div(html_encode_utf8(word), _class='tight grey'),
                    # t.div(
                    #     '{}'.format(html_encode_utf8(lemma)),
                    #     ),
                    # t.div(html_encode_utf8(pronounce)),
                    # _class='flex-col',
                    ),
                t.div(
                    '{:,}'.format(count),
                    _class='count tight',
                    ),
                t.div(
                    t.div(
                        '&nbsp;',
                        _class='swatch',
                        style='''
                            background-color: {};
                            '''.format(next(color)),
                        ),
                    _class='tight',
                    ),
                href='/strongs/{}'.format(strongs),
                _class='flex-row meta center',
                )
            for (
                strongs,
                word,
                count,
                json
                )in meta if strongs[0] == language
            )
    def get_content():
        color = cycle(colors)
        highlight = cycle(highlights)
        def get_data_dict(m):
            strongs, word, count, json = m
            return dict(
                value=count,
                color=next(color),
                highlight=next(highlight),
                label='{}'.format(html_encode_utf8(word)),
                )
        def get_lang(lang, show_word=False):
            def get_language_from_lang(lang):
                return 'hebrew' if lang == 'H' else 'greek'
            return t._(
                t.div(
                    'Tap {} word for info'.format(
                        get_language_from_lang(lang)),
                    _class='subhead',
                    ),
                t.div(
                    t.div(
                        t.div(word, _class='word') if show_word else t._(),
                        print_meta(lang),
                        _class='tight',
                        ),
                    t.div(
                        t.canvas(id='chart_{}'.format(lang),
                            width='120', height='120'
                            ),
                        t.script('''
                            $(window).resize(function(){{
                                // chart_update_{}({});
                                }});
                            '''.format(
                                lang,
                                json_encode(list(
                                    get_data_dict(m) for m in meta
                                        if m[0][0] == lang)),
                                )
                            ),
                        _class='chart-container',
                        ),
                    _class='lang flex-row',
                    ),
                    t.script('''
                        $(document).ready(function(){{
                            resize_charts();
                            chart_update_{}({});
                            //$(window).resize();
                            }});
                        '''.format(
                            lang,
                            json_encode(list(
                                get_data_dict(m) for m in meta
                                    if m[0][0] == lang)),
                            )
                        ),
                )
        def divider():
            return t.div(
                t.div(),
                _class='divider',
                )
        return t.div(
            t.div(word, _class='word'),
            get_lang('G', show_word=False),
            divider(),
            get_lang('H'),
            _class='flex-col',
            )
    return page(get_content())

def ref(book, chapter, verse, data):
    _verse = verse
    def get_content():
        verse_words = defaultdict(list)
        for book, chapter, verse, phrase, strongs in data:
            verse_words[verse].append([
                phrase,
                strongs,
                ])
        return t._(
            t.div('{} {}'.format(book, chapter), _class='book'),
            t.div('Tap an underlined word for source text',
                _class='section-label',),
            t._(
                t.div(
                    t.a(str(verse), '&nbsp', _name='{}'.format(verse)),
                    t.span(
                        t._(
                            t.a(
                                phrase,
                                href='/strongs/{}'.format(strongs),
                                _class='ref-word-link',
                                ) if strongs else phrase,
                            ' ',
                        )
                        for phrase, strongs in phrase_data
                        ),
                    _class='verse',
                    )
                for verse, phrase_data in sorted(verse_words.items())
                ),
            t.script('''
                scrollToAnchor({});
                '''.format(json_encode(str(_verse)))) if _verse else t._(),
            )
    return page(get_content())

def na(text):
    return page(
        '{} has no strongs number and does not appear to be a valid reference'.format(text))

def strongs(strongs, word, jsons, usage_counts, usage):
    color = cycle(colors)
    color2 = cycle(colors)
    highlight = cycle(highlights)
    mainMeta = json_decode(jsons[0])
    def getPronun():
        return mainMeta['pronun']['sbl']
    def getDefn():
        return t._(t.div(json_decode(json)['def']['short'] for json in jsons))
    def get_content():
        def get_book_verses_dict():
            result = defaultdict(list)
            for phrase, word, book, book_id, chap, verse, text, author in usage:
                result[book].append([book_id, '{} {}:{}'.format(book, chap, verse),
                    text.replace(phrase, '<b>{}</b>'.format(phrase))])
            return result
        def get_words_verses_dict():
            result = defaultdict(list)
            for phrase, word, book, book_id, chap, verse, text, author in usage:
                result[word.lower()].append([word, '{} {}:{}'.format(book, chap, verse),
                    text.replace(phrase, '<b>{}</b>'.format(phrase))])
            return result
        def get_author_verses_dict():
            result = defaultdict(list)
            for phrase, word, book, book_id, chap, verse, text, author in usage:
                result[author].append([author, '{} {}:{}'.format(book, chap, verse),
                    text.replace(phrase, '<b>{}</b>'.format(phrase))])
            return result
        def get_data_dict(uc):
            word, count = uc
            return dict(
                value=count,
                color=next(color),
                highlight=next(highlight),
                label=word,
                )
        def get_verse_group(group_class, items, hide=False):
            return t.div(
                t._(
                    t.div(
                        t.div(
                            '{} ({})'.format(
                                group_key, len(verses)),
                            onclick='''
                                var offset = $(this).offset().top - 20;
                                var el = $(this).next('.verse-texts');;
                                $('.verse-texts').not(el).hide(300);
                                el.toggle(300, function(){
                                    $(window).scrollTop(offset);
                                    });
                                ''',
                            _class='verse-word',
                            ),
                        t.div(
                            t._(
                                t.div(
                                    t.a(ref, href='/ref/{}/{}/{}'.format(
                                        ref.rsplit(' ', 1)[0],
                                        ref.rsplit(' ', 1)[-1].split(':')[0],
                                        ref.rsplit(' ', 1)[-1].split(':')[-1],
                                        )),
                                    # t.a(
                                    #     ref,
                                    #     href='/ref/{}/{}/{}'.format(
                                    #         ref.rsplit(' ', 1)[0],
                                    #         ref.rsplit(' ', 1)[1].split(':')[0],
                                    #         ref.rsplit(' ', 1)[1].split(':')[1],
                                    #         ),
                                    #     ),
                                    t.span(' - '),
                                    t.span(html_encode_utf8(text)),
                                    _class='verse-text'
                                    )
                                for key, ref, text in verses
                                ),
                            _class='verse-texts',
                            ),
                        )
                    for group_key, verses in items
                    ),
                _class='strongs_group {} {}'.format(
                    group_class,
                    'hide' if hide else '',
                    ),
                )
        return t.div(
            t.div(
                t.div(
                    t.div(html_encode_utf8(getPronun()), _class='word'),
                    t.div(html_encode_utf8(word), _class='orig_word'),
                    _class='tight',
                    ),
                t.div(),
                t.div(
                    # t.div('Tap for morphology', _class='hint'),
                    t.div(html_encode_utf8(getDefn())),
                    _class='definition tight',
                    ),
                _class='flex-row tight strongs'
                ),
            t.div(
                t.div(
                    # t.div('Translated As', _class='section-label tight'),
                    t._(
                        t.div(
                            t.div(html_encode_utf8(word)),
                            # t.div(str(count), _class='count tight'),
                            t.div('{:,}'.format(count), _class='count tight'),
                            t.div(
                                t.div(
                                    '&nbsp;',
                                    _class='swatch',
                                    style='''
                                        background-color: {};
                                        '''.format(next(color2)),
                                    ),
                                _class='flex-row center tight',
                                ),
                            _class='flex-row tight center',
                            )
                        for word, count in usage_counts
                        ),
                    t.div(),
                    _class='flex-col tight lang',
                    ),
                t.div(
                    t.canvas(id='chart_eng', width='150', height='150'),
                    t.script('''
                        $(window).resize(function(){{
                            // chart_update('eng', {});
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
                t.div(
                    t.div(
                        t.div(),
                        t.div(
                            'By Word',
                            onclick="strongs_change_group(this, 'by_word');",
                            _class='usage-sorter first tight selected',
                            ),
                        t.div(
                            'By Book',
                            onclick="strongs_change_group(this, 'by_book');",
                            _class='usage-sorter tight',
                            ),
                        t.div(
                            'By Author',
                            onclick="strongs_change_group(this, 'by_author');",
                            _class='usage-sorter tight',
                            ),
                        t.div(),
                        _class='usage-sort flex-row',
                        ),
                    _class='sort-control',
                    ),
                # t.div('Tap above to change grouping', _class='hint'),
                # t.div('Tap below to expand', _class='hint'),
                get_verse_group(
                    'by_author',
                    sorted(get_author_verses_dict().items(),
                        key=lambda a: a[1][-1]),
                    hide=True,
                    ),
                get_verse_group(
                    'by_book',
                    sorted(get_book_verses_dict().items(),
                        key=lambda a: a[1][0]),
                    hide=True,
                    ),
                get_verse_group(
                    'by_word',
                    sorted(get_words_verses_dict().items(),
                        key=lambda a: len(a[1]), reverse=True),
                    ),
                _class='verses-container',
                ),
                t.script('''
                    $(document).ready(function(){{
                        resize_charts();
                        chart_update('eng', {});
                        }});
                    '''.format(
                        json_encode(list(
                            get_data_dict(uc) for uc in usage_counts)),
                        )
                    ),
            )
    return page(get_content())
