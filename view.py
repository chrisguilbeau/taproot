from lib import t
from lib import html5
from lib import url_for

def getHomeBody():
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
        t.div('Description of what to do'),
        _class='main flex-col',
        )

def home():
    return html5(
        css=[
            '/static/flex.css',
            '/static/style.css',
            ],
        body = getHomeBody(),
        title='taproot',
        )
