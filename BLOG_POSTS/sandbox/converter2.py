from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

lexer = get_lexer_by_name("python", stripall=True)
formatter = HtmlFormatter(linenos=True, cssclass="source")

code = open('source.py','r').read()

result = highlight(code, lexer, formatter)

print result