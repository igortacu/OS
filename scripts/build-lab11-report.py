#!/usr/bin/env python3
"""Build the Lab 11 PDF from its Markdown report and native screenshots."""
from pathlib import Path
import re
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
lab = root / 'Lab11'
text = (lab / 'report.md').read_text()

# Keep every native image and its caption together, preserving its proportions.
# Captions already contain explicit figure numbers in the Markdown report.
def figure(match):
    heading, caption, path = match.groups()
    return ('\\noindent\\begin{minipage}{\\linewidth}\n'
            '\\textbf{' + heading + '}\\par\\medskip\n\\centering\n'
            '\\includegraphics[width=\\linewidth,height=0.60\\textheight,'
            'keepaspectratio]{' + str(lab / path) + '}\n'
            '\\captionof*{figure}{' + caption + '}\n\\end{minipage}\n')

text = re.sub(r'### ([^\n]+)\n\n!\[([^\]]+)\]\((evidence/screenshots/[^)]+)\)', figure, text)

header = r'''---
author: Tacu Igor
lang: en
papersize: a4
geometry: margin=2cm
fontsize: 11pt
colorlinks: true
header-includes:
  - \usepackage{graphicx}
  - \usepackage{caption}
  - \usepackage{listings}
  - \lstset{basicstyle=\ttfamily\small,breaklines=true,columns=fullflexible,keepspaces=true}
---

'''
# PDF file links resolve against the course repository on GitHub.
text = re.sub(r'(?<!!)\[([^\]]+)\]\((?!https?://)([^)]+)\)',
              lambda m: '[' + m[1] + '](https://github.com/igortacu/OS/blob/main/Lab11/' + m[2] + ')', text)
with tempfile.TemporaryDirectory(prefix='os-lab11-pdf-') as temp:
    source = Path(temp) / 'report.md'
    source.write_text(header + text)
    subprocess.run(['pandoc', str(source), '--pdf-engine=xelatex', '--listings',
                    '--lua-filter', str(root / 'scripts/keep-code.lua'),
                    '-V', 'mainfont=Arial', '-o', str(lab / 'Lab11_TacuIgor_FAF-242.pdf')], check=True)
