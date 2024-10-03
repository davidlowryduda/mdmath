"""
htmlrenderer.py - md-->html

# **********************************************************************
#       This is htmlrenderer.py, part of mdmath.
#       Copyright (c) 2024 David Lowry-Duda <david@lowryduda.com>
#       All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
#                 <http://www.gnu.org/licenses/>.
# **********************************************************************
"""
import mistune
import pygments
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


from dbmath.sidenote import SidenotePlugin


class MarkdownToHTMLRenderer(mistune.HTMLRenderer):
    def __init__(self):
        super().__init__()
        self.sidenote_counter = 1
        self.sidenotes = []

    def heading(self, text, level):
        return f'<h{level}>{text}</h{level}>\n'

    def paragraph(self, text):
        return f'<p>{text}</p>\n\n'

    def list_item(self, text):
        return f'<li>{text}</li>\n'

    def list(self, text: str, ordered: bool, **attrs) -> str:
        if ordered:
            return '<ol>\n' + text + '</ol>\n\n'
        return '<ul>\n' + text + '</ul>\n\n'

    def block_quote(self, text):
        return f'<blockquote>{text}</blockquote>\n\n'

    def link(self, text, url, title=None):
        return f'<a href="{url}">{text}</a>'

    def emphasis(self, text):
        return f'<em>{text}</em>'

    def strong(self, text):
        return f'<strong>{text}</strong>'

    def image(self, alt, url, title=None):
        return f'<img src="{url}" alt="{alt}"/>'

    def codespan(self, text):
        return f'<code>{text}</code>'

    def block_code(self, code, info=None):
        """Render code block with Pygments highlighting."""
        if not lang: lexer = guess_lexer(code)
        else:
            try:
                lexer = get_lexer_by_name(lang)
            except ClassNotFound:
                lexer = guess_lexer(code)
        formatter = HtmlFormatter()
        highlighted_code = highlight(code, lexer, formatter)
        return f'<div class="codehilite">{highlighted_code}</div>\n\n'

    def sidenote(self, text):
        marker = f'<sup>{self.sidenote_counter}</sup>'
        sidenote_content = f'<aside id="sidenote-{self.sidenote_counter}"><sup>{self.sidenote_counter}</sup> {text}</aside>'
        self.sidenote_counter += 1
        return marker + sidenote_content


def markdown_to_html_with_sidenotes(md_text):
    renderer = MarkdownToHTMLRenderer()
    markdown = mistune.create_markdown(renderer=renderer, plugins=[SidenotePlugin])
    html_content = markdown(md_text)
    return html_content
