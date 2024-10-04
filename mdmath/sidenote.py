"""
sidenote.py - a sidenote plugin for mistune

# **********************************************************************
#       This is part of mdmath.
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
SIDENOTE_PATTERN = r'\[note\](?P<sidenote_text>.*?)\[\/note\]'


def parse_sidenote(inline, m, state):
    text = m.group('sidenote_text')
    new_state = state.copy()
    new_state.src = text
    children = inline.render(new_state)
    state.append_token({'type': 'sidenote', 'children': children})
    return m.end()


def SidenotePlugin(md):
    md.inline.register('sidenote', SIDENOTE_PATTERN, parse_sidenote, before='link')
