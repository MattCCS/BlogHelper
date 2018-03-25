#!/usr/bin/env python

import re

####################################
# from pip
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

####################################
# globals
PYTHON_CODE_DELIMITER = "<TOGGLEPYTHON>"

def convert(code):
    """
    Color the given code and convert urls into a/href tags
    """

    lexer = PythonLexer()
    formatter = HtmlFormatter(noclasses=True, nobackground=True)

    URLS = True
    if URLS:
        code = re.sub("(?P<url>https?://[^\s]+)", '\g<url> ', code)

    code = highlight(code, lexer, formatter)

    if URLS:
        code = re.sub("(?P<url>https?://[^\s]+)", '<a href="\g<url>">\g<url></a>', code)

    return code

####################################
# read the source text and process it
import sys

try:
    fname = sys.argv[1]
except IndexError:
    fname = "source.py"

code = open(fname,'r').read()


####################################
# convert the code to HTML (all, if no delimiter present)
ALTERNATE = (PYTHON_CODE_DELIMITER in code)
# ALTERNATE = 0

if ALTERNATE:
    L = code.split(PYTHON_CODE_DELIMITER)
    L = [(s if not i%2 else convert(s)) for i,s in enumerate(L)]
    OUT = ''.join(L)
else:
    OUT = convert(code)


####################################
# copy resulting HTML to clipboard
import subprocess

def write_to_clipboard(text):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))

write_to_clipboard(OUT)
print "(Sent to clipboard)"
