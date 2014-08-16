from tag import Tags as t
from flask import url_for

def html5(title='', css=[], js=[], metas=[], body=''):
    def getJs():
        return t._(t.script(src=_js) for _js in js)
    def getCss():
        return t._(t.link(rel='stylesheet', href=_css) for _css in css)
    def getMetas():
        return t._(t.meta(_name=name, content=content)
            for name, content in metas.iteritems())
    return t._(
        "<!DOCTYPE html>",
        t.html(
            t.head(
                t.title(title),
                getCss(),
                getJs(),
                getMetas(),
                ),
            t.body(body),
            ),
        )
