"""
cli.py

# **********************************************************************
#       This is cli.py, part of mdmath.
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
import argparse
import os
import sys


from mdmath import markdown_to_html, markdown_to_latex


def validate_to(toarg):
    arg = toarg.lower()
    if not arg in ('html', 'tex', 'latex'):
        raise ValueError(f"Filetype '{toarg}' not understood. Must be 'html' or 'tex'")
    if arg == 'html': return 'html'
    return 'tex'


def validate_input_file(fname):
    if not os.path.exists(fname):
        raise FileExistsError(f"File '{fname}' not found.")
    return fname


def make_parser():
    parser = argparse.ArgumentParser(
        description="MDMath Command Line Interface.",
        epilog="Made by David Lowry-Duda <david@lowryduda.com>."
    )
    parser.add_argument('--to', default='html', help='Type to convert to (html or latex, defaults to html)')
    parser.add_argument('--standalone', '-s', action='store_true', help='Make standalone output.')
    parser.add_argument('filename', help='The FILENAME to be converted.')
    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()
    try:
        ft = validate_to(args.to)
    except ValueError as e:
        print(e)
        sys.exit(1)
    try:
        fname = validate_input_file(args.filename)
    except FileExistsError as e:
        print(e)
        sys.exit(1)
    with open(fname, "r", encoding="utf8") as infile:
        mdcontent = infile.read()
    if ft == 'html':
        output = markdown_to_html(mdcontent, standalone=args.standalone)
        print(output)
        return
    elif ft == 'tex':
        output = markdown_to_latex(mdcontent, standalone=args.standalone)
        print(output)
        return
    sys.exit(2)


if __name__ == "__main__":
    main()
