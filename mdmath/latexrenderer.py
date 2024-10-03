"""
latexrenderer.py - md-->latex

# **********************************************************************
#       This is latexrenderer.py, part of mdmath.
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


from mdmath.sidenote import SidenotePlugin


class MarkdownToLatexRenderer(mistune.HTMLRenderer):
    def heading(self, text, level, **attrs):
        if level == 1:
            return f'\\section{{{text}}}\n'
        elif level == 2:
            return f'\\subsection{{{text}}}\n'
        elif level == 3:
            return f'\\subsubsection{{{text}}}\n'
        return f'\\paragraph{{{text}}}\n'

    def paragraph(self, text):
        return f'{text}\n\n'

    def list_item(self, text):
        return f'\\item {text}\n'

    def list(self, text: str, ordered: bool, **attrs) -> str:
        if ordered:
            return '\\begin{enumerate}\n' + text + '\\end{enumerate}\n'
        return '\\begin{itemize}\n' + text + '\\end{itemize}\n'

    def block_quote(self, text):
        return f'\\begin{{quote}}\n{text}\\end{{quote}}\n'

    def link(self, text, url, title=None):
        return f'\\href{{{url}}}{{{text}}}'

    def emphasis(self, text):
        return f'\\emph{{{text}}}'

    def strong(self, text):
        return f'\\textbf{{{text}}}'

    def image(self, alt, url, title=None):
        return f'\\includegraphics{{{url}}}'

    def codespan(self, text):
        return f'\\texttt{{{text}}}'

    def block_code(self, code, info=None):
        if info is None:
            info = 'txt'
        return f'\\begin{{minted}}[breaklines, linenos, breaksymbol={{\\tiny\\color{{black}}\\ensuremath{{\\hookrightarrow}}}}]{{{info}}}\n{code}\\end{{minted}}\n'

    def sidenote(self, text):
        return f'\\marginpar{{{text}}}'


def markdown_to_latex(md_text, standalone=False):
    renderer = MarkdownToLatexRenderer()
    markdown = mistune.create_markdown(renderer=renderer, plugins=[SidenotePlugin])
    inner_text = markdown(md_text)
    if not standalone:
        return inner_text
    return latex_header + inner_text + latex_footer


### Header and Footer for my own use ###

latex_header = r"""
\documentclass[11pt,reqno]{amsart}
% We ain't got no time for eq. nums. on the left

% Enable UTF-8 encodings for input, to enter é instead of \'{e}.
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

\usepackage{fouriernc}
\usepackage[scale=0.92]{tgschola}

\usepackage{amsmath,amsthm,amssymb}

% Presented to you by Technicolor, and the number 3
\usepackage{graphics}
\usepackage{hyperref}
\usepackage[dvipsnames]{xcolor}

% For full minted support, it's necessary to compile using
% the -shell-escape flag. For example, pdflatex -shell-escape file.tex.
%
%\usepackage{minted}
%\usemintedstyle{borland}
%
% Then code can be included below using something like the following.
%
% \begin{minted}[breaklines, linenos,
% breaksymbol={\tiny\color{white}\ensuremath{\hookrightarrow}}]{python}
% ...CODE...
% \end{minted}

% For full page usage, shockingly
%\usepackage{fullpage}

% Slightly prettier tables
\usepackage{booktabs}

% Don't worry about starred environments. YOU are the star!
\usepackage{mathtools}
\mathtoolsset{showonlyrefs}

% Checkbox things
\usepackage{enumitem}
\newlist{todolist}{itemize}{2}
\setlist[todolist]{label=$\square$}
\usepackage{pifont}
\newcommand{\cmark}{\ding{51}}%
\newcommand{\xmark}{\ding{55}}%
\newcommand{\done}{\rlap{$\square$}{\raisebox{2pt}{\large\hspace{1pt}\cmark}}%
\hspace{-2.5pt}}
\newcommand{\wontfix}{\rlap{$\square$}{\large\hspace{1pt}\xmark}}
% To use, do e.g.
% \begin{todolist}
%   \item something
%   \item[\done] something done
%   \item[\wontfix] profit
% \end{todolist}

% For ease in writing labels and references
%\usepackage{showkeys}
\usepackage[square,sort,comma,numbers]{natbib}

% For pretty hyperlinks
\definecolor{darkblue}{rgb}{0.0,0.0,0.3}
\hypersetup{colorlinks,breaklinks,
  linkcolor=darkblue,urlcolor=darkblue,
anchorcolor=darkblue,citecolor=darkblue}

\theoremstyle{plain}
\newtheorem{theorem}{Theorem}%[section]
\newtheorem*{theorem*}{Theorem}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem*{proposition*}{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem*{corollary*}{Corollary}
\newtheorem{claim}[theorem]{Claim}
\newtheorem{conjecture}[theorem]{Conjecture}
\newtheorem{question}[theorem]{Question}
\theoremstyle{definition}
\newtheorem{remark}[theorem]{Remark}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{example}[theorem]{Example}
\newtheorem{exercise}[theorem]{Exercise}

\newtheorem{algorithm}[theorem]{Algorithm}
\newtheorem*{algorithm*}{Algorithm}
\newtheorem{experiment}[theorem]{Experiment}
\newtheorem*{experiment*}{Experiment}
\newtheorem*{expnotes}{Experiment Notes}

%\numberwithin{equation}{section}

% Nongross real and imaginary parts
\renewcommand{\Im}{\operatorname{Im}}
\renewcommand{\Re}{\operatorname{Re}}
\DeclareMathOperator{\SL}{SL}
\DeclareMathOperator*{\Res}{Res}


% Private macros for simplicity
% \usepackage{personalmacros-private}
% \usepackage{localmacros-private}
%% NOTE: To make a version with these macros removed, do the following steps
%  1. install the de-macro package (which is just a python program on CTAN)
%  2. run `de-macro THISFILE.tex`. This will output a "clean" version of the tex
%     with the personal macros above expanded.
%  3. The resulting texfile is clean, but still has comments. If desired,
%     these must be removed separately.

% Don't have subsections appear in TOC
\setcounter{tocdepth}{1}

\title{TITLE}
\author{AUTHORS}
\date{DATE}
%% Grant Info
\thanks{This work was supported by the Simons Collaboration in Arithmetic
Geometry, Number Theory, and Computation via the Simons Foundation grant
546235.}

\begin{document}

\maketitle
\tableofcontents
"""

latex_footer = r"""
\begin{thebibliography}{9}
\bibitem[Davenport]{davenport} Davenport, \emph{Multiplicative Number Theory}.
\end{thebibliography}

\end{document}
"""
