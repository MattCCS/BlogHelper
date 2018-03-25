#TEXT
# This is a <strong>test</strong> of automatic Python-to-Wordpress HTML conversion.

"""
Converts a Python file to be Wordpress-friendly.

Blocks of #TEXT and #OUTPUT must be continuous comment blocks.
Blocks following #TEXT and #OUTPUT must begin with "# " (hash, space)
Everything else has no restrictions.

Pass --copy to copy results to clipboard.
"""

import argparse
import cgi
import re
import subprocess

from pygments import highlight
from pygments.style import Style
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer


TEXT_FLAG = "#TEXT"
OUTPUT_FLAG = "#OUTPUT"
BLOCK_DELIMITER = "\n\n"


class MyStyle(Style):
    default_style = 'bg:#8f8f8f'


def parse_args():
    parser = argparse.ArgumentParser(description="Converts a Python file into Wordpress-friendly HTML.")
    parser.add_argument("file", help="The file to convert")
    parser.add_argument("-c", "--copy", help="Whether to copy to clipboard", default=False, action='store_true')
    return parser.parse_args()


def convert_code(code, URLs=True):
    """Color the given code and convert urls into a/href tags"""

    lexer = Python3Lexer(style=MyStyle)
    formatter = HtmlFormatter(noclasses=True, nobackground=True)

    # if URLs:
    #     code = re.sub("(?P<url>https?://[^\s]+)", '\g<url> ', code)

    code = highlight(code, lexer, formatter)

    if URLs:
        code = re.sub("(?P<url>https?://[^\s]+)", '<a href="\g<url>">\g<url></a>', code)

    return code


def convert_text(text):
    text_lines = text.split('\n')[1:]
    text_lines = [line[2:] for line in text_lines]
    text = '\n'.join(text_lines)
    return text


def convert_output(output):
    output_lines = output.split('\n')[1:]
    output_lines = [line[2:] for line in output_lines]
    output = '\n'.join(output_lines)
    return "<pre>{}</pre>".format(cgi.escape(output))


def convert(source):
    # 1) split source up by block
    # (guarantees text and output are separated from code)
    cut_source = source.split(BLOCK_DELIMITER)

    # 2) join code back together if separated by multiple newlines
    # (guarantees all text/output/code are joined)
    blocks = []
    acc = ''

    for block in cut_source:
        if block.startswith(TEXT_FLAG) or block.startswith(OUTPUT_FLAG):
            if acc:
                blocks.append(acc)
                acc = ''
            blocks.append(block)
        else:
            acc += BLOCK_DELIMITER + block
    else:
        if acc:
            blocks.append(acc)

    # 3) format blocks, whether text/output/code
    formatted_blocks = []

    for block in blocks:
        if block.startswith(TEXT_FLAG):
            formatted_blocks.append(convert_text(block))
        elif block.startswith(OUTPUT_FLAG):
            formatted_blocks.append(convert_output(block))
        else:
            formatted_blocks.append(convert_code(block))

    # 4) join back together
    out = BLOCK_DELIMITER.join(formatted_blocks)
    return out


def write_to_clipboard(text):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(text.encode('utf-8'))


def main():
    args = parse_args()

    fname = args.file
    print("[ ] Reading '{}'...".format(fname))
    source = open(fname).read().strip()

    print("[ ] Converting...")
    converted_source = convert(source)

    if args.copy:
        write_to_clipboard(converted_source)
        print("[+] Sent to clipboard")
    else:
        print()
        print(converted_source)


if __name__ == '__main__':
    main()

#TEXT
# We see the <i>output:</i>

#OUTPUT
# (Sent to clipboard)
