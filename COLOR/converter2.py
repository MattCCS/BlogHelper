#!/usr/bin/env python

GREY = False


import re

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

code = open('source.py','r').read()

if not GREY:
    lexer = PythonLexer()
    formatter = HtmlFormatter(noclasses=True, nobackground=True)

    URLS = True
    if URLS:
        code = re.sub("(?P<url>https?://[^\s]+)", '\g<url> ', code)

    # print '\n'*10
    # print 'spaced urls'
    # print code

    code = highlight(code, lexer, formatter)

    # print '\n'*10
    # print 'highlighted'
    # print code

    if URLS:
        code = re.sub("(?P<url>https?://[^\s]+)", '<a href="\g<url>">\g<url></a>', code)

    print '\n'*10   # to make it stand out
    # print 'linked urls'
    print code

else:
    print "NOT DONE YET"
    print """<div class="highlight"><pre style="line-height: 125%%""><span style="color: #666666">%s</span></pre></div>""" % code







