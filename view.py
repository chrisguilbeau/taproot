from itertools import cycle
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

def eng(word, meta):
    def print_meta(language):
        return t._(
            t.div(
                t.div(
                    t.div(lemma.encode('ascii', 'xmlcharrefreplace')),
                    t.div(xlit.encode('ascii', 'xmlcharrefreplace')),
                    t.div(pronounce.encode('ascii', 'xmlcharrefreplace')),
                    _class='flex-col',
                    ),
                t.div(
                    '{:,}'.format(count),
                    _class='count tight',
                    ),
                _class='flex-row meta',
                )
            for (
                lemma,
                xlit,
                pronounce,
                lang,
                count
                )in meta if lang == language
            )

    def get_content():
        color = cycle(colors)
        highlight = cycle(highlights)
        def get_data_dict(m):
            lemma, xlit, pro, lang, count = m
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
                    print_meta(lang)
                    ),
                t.div(
                    t.canvas(id='chart_{}'.format(lang),
                        width='300', height='300'),
                    t.script('''
                        $(document).ready(function(){{
                            chart_update_{}({});
                            }});
                        '''.format(
                            lang,
                            json_encode(list(
                                get_data_dict(m) for m in meta
                                    if m[-2] == lang)),
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
            get_lang('greek', show_word=True),
            divider(),
            get_lang('heb'),
            _class='flex-col',
            )
    return page(get_content())
