#!/usr/bin/env python

# standard
import cgi
import re
import subprocess
import sys

# pip
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

####################################
# GLOBALS
PYTHON_CODE_DELIMITER   = "<TOGGLEPYTHON>"
PYTHON_OUTPUT_DELIMITER = "<TOGGLEOUT>"

def convert_code(code, URLS=True):
    """Color the given code and convert urls into a/href tags"""

    lexer = PythonLexer()
    formatter = HtmlFormatter(noclasses=True, nobackground=True)

    if URLS:
        code = re.sub("(?P<url>https?://[^\s]+)", '\g<url> ', code)

    code = highlight(code, lexer, formatter)

    if URLS:
        code = re.sub("(?P<url>https?://[^\s]+)", '<a href="\g<url>">\g<url></a>', code)

    return code

def convert_output(output):
    return "<pre>{}</pre>".format(cgi.escape(output))

####################################
# read the source text and process it

try:
    fname = sys.argv[1]
except IndexError:
    fname = "source.py"

code = open(fname,'r').read()


####################################
# convert the code to HTML (all, if no delimiter present)
ALTERNATE = (PYTHON_CODE_DELIMITER in code)

def convert(source):
    cut_source = source.split(PYTHON_CODE_DELIMITER)

    blocks = []

    for (i, block) in enumerate(cut_source):
        if i%2:
            blocks.append(convert_code(block))
        else:
            cut_block = block.split(PYTHON_OUTPUT_DELIMITER)
            for (j, block) in enumerate(cut_block):
                if j%2:
                    blocks.append(convert_output(block))
                else:
                    blocks.append(block)

    return ''.join(blocks)

# if ALTERNATE:
#     L = code.split(PYTHON_CODE_DELIMITER)
#     L = [(s if not i%2 else convert(s)) for i,s in enumerate(L)]
#     OUT = ''.join(L)
# else:
#     OUT = convert(code)

OUT = convert(code)
# print OUT
# exit()

####################################
# copy resulting HTML to clipboard

def write_to_clipboard(text):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))

write_to_clipboard(OUT)
print "(Sent to clipboard)"
