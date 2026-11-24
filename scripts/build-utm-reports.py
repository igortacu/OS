#!/usr/bin/env python3
"""Rebuild every report with the supplied UTM structure; preserve source evidence."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from utm_report_style import ROOT, STYLE, CONFIG, cover, intro_md, tex

parser=argparse.ArgumentParser()
parser.add_argument('--only',help='Comma-separated report keys, e.g. 11,12,13')
args=parser.parse_args()
keys=args.only.split(',') if args.only else [k for k,v in CONFIG['reports'].items() if 'folder' in v]


def pandoc(text,fmt='markdown',target='json'):
    return subprocess.check_output(['pandoc','-f',fmt,'-t',target],input=text.encode()).decode()

def ast(text):return json.loads(pandoc(text))['blocks']
def text_of(inlines):
    out=''
    for x in inlines:
        if x['t']=='Str':out+=x['c']
        elif x['t'] in ('Space','SoftBreak','LineBreak'):out+=' '
        elif x['t']=='Code':out+=x['c'][1]
        elif x['t'] in ('Emph','Strong','SmallCaps','Strikeout'):out+=text_of(x['c'])
        elif x['t']=='Link':out+=text_of(x['c'][1])
    return out

figure_number=0

def figure(path,caption):
    global figure_number
    figure_number+=1
    if not caption.startswith(('Figure ','Figura ')):
        caption=f'Figura {figure_number}. '+caption
    path=Path(path)
    if not path.is_file():raise FileNotFoundError(path)
    return r'\par\medskip\noindent\begin{minipage}{\linewidth}\setstretch{1.0}'+'\n'+r'\captionof*{figure}{'+tex(caption.replace('Figure ','Figura '))+r'}'+'\n'+r'\centering\includegraphics[width=\linewidth,height=0.67\textheight,keepaspectratio]{'+str(path.relative_to(ROOT))+r'}'+'\n'+r'\end{minipage}\par\medskip'+'\n'

def clean_md(s):
    if s.startswith('---\n'):s=s[s.index('\n---',4)+4:].lstrip()
    # The first level-two header starts the authored technical content.
    m=re.search(r'^## ',s,re.M)
    if m:s=s[m.start():]
    return s

def raw_figures(s):
    # Older reports use explicit LaTeX figures; retain their captions and PNGs.
    def replace(m):
        block=m[0]
        image=re.search(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',block)
        caption=re.search(r'\\caption(?:\*)?\{(.*)\}',block)
        if not image or not caption:raise ValueError('Unrecognized native figure')
        return figure(ROOT/image[1],caption[1])
    s=re.sub(r'\\begin\{figure\}(?:\[[^\]]*\])?.*?\\end\{figure\}',replace,s,flags=re.S)
    return s.replace(r'\clearpage','')

def normalize(blocks,folder,media_map=None):
    output=[]; i=0; pending_caption=None
    while i<len(blocks):
        b=blocks[i]
        if b['t']=='Para' and text_of(b['c']).startswith(('Figure ','Figura ')) and i+1<len(blocks):
            following=blocks[i+1]
            if following['t']=='Para' and any(v['t']=='Image' for v in following['c']):
                pending_caption=text_of(b['c']);i+=1;continue
        if b['t']=='Figure':
            # Pandoc 3 represents a captioned Markdown image as a Figure.
            content=b['c'][2]
            assert len(content)==1 and content[0]['t'] in ('Plain','Para')
            b={'t':'Para','c':content[0]['c']}
        if b['t']=='Header':
            b['c'][0]=min(4,max(2,b['c'][0]))
        if b['t']=='Para' and any(v['t']=='Image' for v in b['c']):
            images=[v for v in b['c'] if v['t']=='Image']
            if len(images)!=1:raise ValueError('Expected a single native image per paragraph')
            im=images[0];path=Path(im['c'][2][0])
            if not path.is_absolute():path=folder/path
            if media_map:
                digest=hashlib.sha256(path.read_bytes()).hexdigest()
                path=media_map[digest]
            caption=pending_caption or text_of(im['c'][1]);pending_caption=None
            if not caption and i+1<len(blocks) and blocks[i+1]['t']=='Para':
                following=text_of(blocks[i+1]['c'])
                if following.startswith(('Figure ','Figura ')):caption=following;i+=1
            output.append({'t':'RawBlock','c':['latex',figure(path,caption)]})
        else:output.append(b)
        i+=1
    return output

def md_blocks(file):return normalize(ast(raw_figures(clean_md(file.read_text()))),file.parent)

def word_blocks(number,temp):
    path=ROOT/f'Lab3-4/word/Lab{number}_TacuIgor_FAF-242.docx'
    doc=json.loads(subprocess.check_output(['pandoc',str(path),'-t','json','--extract-media='+str(temp/f'lab{number}')]))
    blocks=doc['blocks']
    start=next((i+1 for i,b in enumerate(blocks) if b['t']=='Header' and text_of(b['c'][2])=='Implementare. Rezultate practice'),None)
    if start is None:start=next(i for i,b in enumerate(blocks) if b['t']=='Header')
    blocks=blocks[start:]
    for block in blocks:
        if block['t']=='Header':
            block['c'][1][0]=f'lab{number}-'+block['c'][1][0]
            if text_of(block['c'][2])=='Concluzie':
                block['c'][2]=[{'t':'Str','c':f'Concluziile laboratorului {number}'}]
    mapping={hashlib.sha256(p.read_bytes()).hexdigest():p for p in (ROOT/'Lab3-4/evidence/screenshots').glob('*.png')}
    heading=ast(f'## Laboratorul {number}\n\n')[0]
    return [heading]+normalize(blocks,ROOT/'Lab3-4',mapping)

def rewrite_links(block):
    if isinstance(block,dict):
        if block.get('t')=='Link':
            url=block['c'][2][0]
            if not re.match(r'https?://|#',url):
                from posixpath import normpath
                rel=normpath(str(current_folder.relative_to(ROOT))+'/'+url)
                block['c'][2][0]='https://github.com/igortacu/OS/blob/main/'+rel
        for value in block.values():rewrite_links(value)
    elif isinstance(block,list):
        for x in block:rewrite_links(x)


def caption_content(block):
    start=block.index(r'\caption{')+len(r'\caption{')
    depth=1; i=start
    while depth:
        if block[i]=='{' and block[i-1]!='\\':depth+=1
        if block[i]=='}' and block[i-1]!='\\':depth-=1
        i+=1
    return block[start:i-1]

def legacy_l12():
    source=ROOT/'Lab1-2/latex/report-body.tex'
    s=source.read_text()
    # Retain the authored objective, practical sections, conclusion and all images.
    body=s
    body=re.sub(r'\\addcontentsline\{toc\}\{[^}]+\}\{[^\n]*\}\n','',body)
    body=body.replace(r'\section*{OBJECTIVE}',r'\subsection*{Obiectivul experimentelor}')
    body=body.replace(r'\section*{CONCLUSION}',r'\section*{Concluzie}')
    body=body.replace(r'\section*{PART I',r'\subsection*{PART I').replace(r'\section*{PART II',r'\subsection*{PART II')
    body=body.replace(r'\pagebreak','')
    # Split old side-by-side screenshots into full-width evidence figures.
    def split(m):
        block=m[0]
        sub=re.findall(r'\\begin\{subfigure\}.*?\\end\{subfigure\}',block,re.S)
        if not sub:
            path=re.search(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',block)
            # Keep complex caption TeX from the original source.
            caption=caption_content(block)
            p=next(p for p in (ROOT/'Lab1-2/reports/evidence').rglob(path[1]))
            return (r'\begin{figure}[H]\centering\caption{'+caption+'}\n'+r'\includegraphics[width=\linewidth,height=0.67\textheight,keepaspectratio]{'+str(p.relative_to(ROOT))+r'}\end{figure}')
        result=''
        for part in sub:
            path=re.search(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',part)
            caption=caption_content(part)
            p=next(p for p in (ROOT/'Lab1-2/reports/evidence').rglob(path[1]))
            result+=(r'\begin{figure}[H]\centering\caption{'+caption+'}\n'+r'\includegraphics[width=\linewidth,height=0.67\textheight,keepaspectratio]{'+str(p.relative_to(ROOT))+r'}\end{figure}'+'\n')
        return result
    body=re.sub(r'\\begin\{figure\}.*?\\end\{figure\}',split,body,flags=re.S)
    def keep_listing(m):
        return (r'\par\noindent\begin{minipage}{\linewidth}'+'\n'+m[0]+'\n'+r'\end{minipage}\par') if m[0].count('\n')<32 else m[0]
    body=re.sub(r'\\begin\{lstlisting\}.*?\\end\{lstlisting\}',keep_listing,body,flags=re.S)
    intro=pandoc(intro_md('1-2'),target='latex')
    return intro+body

with tempfile.TemporaryDirectory(prefix='utm-os-reports-') as tmp:
    temp=Path(tmp)
    for key in keys:
        figure_number=0
        item=CONFIG['reports'][key];current_folder=ROOT/item['folder']
        if key=='1-2':body=legacy_l12()
        else:
            if key=='3-4':practical=word_blocks(3,temp)+word_blocks(4,temp)
            elif key=='5-6':practical=md_blocks(current_folder/'report-lab5.md')+md_blocks(current_folder/'report-lab6.md')
            else:practical=md_blocks(current_folder/'report.md')
            conclusion=[{'t':'RawBlock','c':['latex',r'\par\noindent\begin{minipage}{\linewidth}']}]+ast('# Concluzie\n\n'+item['conclusion'])+[{'t':'RawBlock','c':['latex',r'\end{minipage}\par']}]
            blocks=ast(intro_md(key))+practical+conclusion
            rewrite_links(blocks)
            doc={'pandoc-api-version':json.loads(pandoc(''))['pandoc-api-version'],'meta':{},'blocks':blocks}
            body=subprocess.check_output(['pandoc','-f','json','-t','latex','--listings',
                '--lua-filter='+str(STYLE/'keep-blocks.lua')],input=json.dumps(doc).encode()).decode()
        body=body.replace(r'\def\LTcaptype{none}',r'\def\LTcaptype{table}')
        # Use the same tested preamble for the native LaTeX and Pandoc sources.
        template=(STYLE/'utm-template.tex').read_text()
        rendered=template.replace('$report-title$',tex('Sisteme de operare — Laborator '+item['number']))
        rendered=rendered.replace('$utm-cover$',cover(key)).replace('$body$',body)
        texfile=current_folder/'utm-report.tex'
        texfile.write_text(rendered)
        for attempt in range(2):
            p=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',
                '-output-directory='+str(temp),str(texfile)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            if p.returncode:
                (current_folder/'utm-build-error.txt').write_bytes(p.stdout)
                raise RuntimeError(p.stdout.decode(errors='replace')[-4000:])
        target=current_folder/f'{item["folder"]}_TacuIgor_FAF-242.pdf'
        target.write_bytes((temp/'utm-report.pdf').read_bytes())
        print('Built',target.relative_to(ROOT),flush=True)
