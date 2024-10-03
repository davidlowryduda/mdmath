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
class SidenotePlugin:
    def __init__(self, *args):
        print(args)
        self.pattern = r'\[note\](.*?)\[\/note\]'

    def parse(self, match, state):
        text = match.group(1)
        return {'type': 'sidenote', 'text': text}

    def render(self, renderer, data):
        return renderer.sidenote(data['text'])
