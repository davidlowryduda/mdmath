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


from mdmath.sidenote import SidenotePlugin


class MarkdownToHTMLRenderer(mistune.HTMLRenderer):
    def __init__(self):
        super().__init__()

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
        if not info: lexer = guess_lexer(code)
        else:
            try:
                lexer = get_lexer_by_name(info)
            except ClassNotFound:
                lexer = guess_lexer(code)
        formatter = HtmlFormatter()
        highlighted_code = highlight(code, lexer, formatter)
        return f'<div class="codehilite">{highlighted_code}</div>\n\n'


sidenote_counter = 1
def render_sidenote(renderer, text):
    global sidenote_counter
    marker = f'<sup>{sidenote_counter}</sup>'
    sidenote_content = f'<aside id="sidenote-{sidenote_counter}"><sup>{sidenote_counter}</sup> {text}</aside>'
    sidenote_counter += 1
    return marker + sidenote_content


def markdown_to_html(md_text, standalone=False):
    """
    `standalone` means the output should be a rendering of a complete HTML
    page.
    """
    renderer = MarkdownToHTMLRenderer()
    renderer.register('sidenote', render_sidenote)
    markdown = mistune.create_markdown(renderer=renderer, plugins=[SidenotePlugin])
    html_content = markdown(md_text)
    if not standalone:
        return html_content
    formatter = HtmlFormatter(style="borland")
    pygments_css = formatter.get_style_defs(".codehilite")
    html_page = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Document</title>
    <style>
    {pygments_css}
    {BASE_CSS}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""
    return html_page


BASE_CSS = """
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    margin: 20px;
    padding: 0;
    background-color: #f4f4f9;
    color: #333;
}
h1, h2, h3 {
    border-bottom: 2px solid #ddd;
    padding-bottom: 0.3em;
}
aside {
    float: right;
    width: 200px;
    margin-left: 1rem;
    padding: 0.5rem;
    border-left: 2px solid #ccc;
    font-size: 0.9rem;
    background-color: #f9f9f9;
    color: #333;
    position: relative;
}
p {
    clear: both;
}
sup {
    font-size: 0.8rem;
}
pre {
    background: #f0f0f0;
    padding: 1rem;
    border-radius: 5px;
    overflow-x: auto;
}
code {
    background: #f0f0f0;
    padding: 2px 5px;
    border-radius: 3px;
}
.codehilite {
    margin-bottom: 1rem;
}
"""
