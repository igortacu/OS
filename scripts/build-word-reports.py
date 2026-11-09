#!/usr/bin/env python3
"""Build the separate Word deliverables required by the original L3/L4 sheets.

Figures render the saved terminal output without inventing terminal messages.
Use the bundled workspace Python with python-docx and Pillow.
"""
from pathlib import Path
import json
import re
import shutil
import textwrap
import hashlib
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'Lab3-4/evidence/screenshots'
FIG.mkdir(exist_ok=True)
def read(path):return (ROOT/path).read_text()
raw=read('Lab3-4/evidence/handout-linux.txt')
linux=read('Lab3-4/evidence/linux.txt')
xv=read('Lab3-4/evidence/xv6.txt')
comp=read('Lab3-4/evidence/xv6-comparison.txt')
inspect=read('Lab3-4/evidence/source-inspection.txt')
pred=json.loads(read('Lab3-4/evidence/predictions.json'))
CAPTURES={}

def clip(text,start,end=None):
    s=text[text.index(start):]
    return s[:s.index(end)].strip() if end else s.strip()

def picture(name,content):
    mapping=json.loads((FIG/'manifest.json').read_text())
    path=FIG/mapping.get(name,{}).get('file',name+'.png')
    if not path.exists():raise FileNotFoundError('Missing native screenshot: '+str(path))
    return path

def body(doc,text):doc.add_paragraph(text)
def head(doc,text):doc.add_heading(text,1)
def fig(doc,number,title,text,capture_number=None):
    image=picture('lab'+str(doc.core_properties.subject)+'-'+(capture_number or number),text)
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next=True
    with Image.open(image) as im:w,h=im.size
    width=min(16.4,20.2*w/h)
    p.add_run().add_picture(str(image),width=Cm(width))
    p=doc.add_paragraph('Figure '+number+' – '+title)
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_together=True
    for r in p.runs:r.font.size=Pt(10)

def table(doc,headers,rows,widths=None):
    t=doc.add_table(rows=1,cols=len(headers));t.style='Table Grid'
    for c,value in zip(t.rows[0].cells,headers):c.text=value
    for row in rows:
        for c,value in zip(t.add_row().cells,row):c.text=str(value)
    repeat=OxmlElement('w:tblHeader');t.rows[0]._tr.get_or_add_trPr().append(repeat)
    for i,row in enumerate(t.rows):
        cant=OxmlElement('w:cantSplit');row._tr.get_or_add_trPr().append(cant)
        for j,c in enumerate(row.cells):
            if widths:c.width=Cm(widths[j])
            if i==0:
                shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E7E6E6');c._tc.get_or_add_tcPr().append(shade)
            for p in c.paragraphs:
                p.paragraph_format.space_after=Pt(4)
                for r in p.runs:
                    r.font.size=Pt(9)
                    if i==0:r.bold=True

def document(number,topic):
    d=Document();d.core_properties.author='Tacu Igor';d.core_properties.subject=str(number)
    d.core_properties.title='Report on laboratory work '+str(number)
    sec=d.sections[0];sec.page_width=Cm(21);sec.page_height=Cm(29.7)
    sec.top_margin=sec.bottom_margin=Cm(2);sec.left_margin=sec.right_margin=Cm(2.2)
    normal=d.styles['Normal'];normal.font.name='Arial';normal.font.size=Pt(11)
    normal.paragraph_format.space_after=Pt(7)
    for name in ['Title','Heading 1','Heading 2']:
        d.styles[name].font.name='Arial';d.styles[name].font.color.rgb=RGBColor(0,0,0)
    for s in ['MINISTRY OF EDUCATION AND RESEARCH OF THE REPUBLIC OF MOLDOVA','Technical University of Moldova','Faculty of Computers Informatics and Microelectronics','Department of Software Engineering and Automation']:
        p=d.add_paragraph(s);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    d.add_paragraph('\n\n')
    p=d.add_paragraph('Report on laboratory work '+str(number),'Title');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p=d.add_paragraph(topic);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p=d.add_paragraph('Course Operating Systems');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    d.add_paragraph('\n\n')
    p=d.add_paragraph('Done by: st. gr. FAF-242, Tacu Igor\nChecked by: Reițman Patricia');p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    d.add_paragraph('\n\n\n')
    p=d.add_paragraph('Chișinău, 2026');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p=sec.footer.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');p._p.append(field)
    d.add_page_break()
    head(d,'Purpose and execution record')
    if number == 4:
        body(d,'All twelve figures are native Terminal screenshots supplied by the author from direct command execution and source inspection on the Ubuntu server on 9 November 2026. The xv6 tests use an isolated source copy and its generated test disk. The directory d already existed during the directory-handling capture; grep READ limits the displayed listing. Bash comparisons use separate temporary directories. Source files and earlier full execution transcripts accompany the screenshots. The submission was prepared with coding assistance; MIT xv6 is identified as upstream in the source provenance file.')
    else:
        body(d,'All twenty-four Lab 3 figures now use native Terminal screenshots supplied by the author from direct execution and source inspection on the Ubuntu server on 9 November 2026. Some screenshots cover two adjacent questions. The initial predictions and their original run are retained in predictions.json; the screenshots document subsequent verification runs. The exact text logs and source are also included in the repository. The submission was prepared with coding assistance, and MIT xv6 is identified as upstream in the source provenance file.')

    return d

d=document(3,'The command line shell pipes and text filters')
head(d,'Part 1 Move fast and find help')
body(d,'Cd and echo are Bash builtins. In the interactive capture, ls is an alias for ls --color=auto; which resolves the underlying external executable to /usr/bin/ls. Cd must change the current directory of the persistent shell itself. A child process could change only its own directory. In this run PATH had nine entries and which resolved ls to /usr/bin/ls. A nonexistent command returned 127. The ls option -t sorts by modification time, newest first. Man, man -k, ls --help and help cd supplied local help.')
interactive=read('Lab3-4/evidence/interactive-bash.txt')
fig(d,'1.1','Tab completion and reverse history search',interactive)
fig(d,'1.2','Type and which',clip(raw,'+ type cd','+ echo /usr/local'))
fig(d,'1.3','Directories in PATH',clip(raw,'+ printf \'PATH directory count:', '+ nosuchprog'))
fig(d,'1.4','Exit status of a missing command',clip(raw,'+ nosuchprog','+ ls --help'))

head(d,'Part 2 Predictions and shell expansion')
body(d,'The required play directory contained a.c, b.c, file1.txt, file2.txt, notes.txt and alfa beta.txt. Each prediction below was recorded before execution; timestamps and complete stderr are retained in the JSON evidence. Differences in line layout from ls are presentation differences, not additional filenames.')
explanations=[
 'Bash expands the pattern before echo starts.', 'Question mark matches one character.',
 'The range matches names beginning with a or b.', 'The unmatched pattern remains literal with the default settings.',
 'Unquoted whitespace creates two operands.', 'Quotes preserve one pathname containing a space.',
 'Single quotes and backslash protect the dollar sign; double quotes permit expansion.',
 'Brace expansion lists values; arithmetic expansion computes 42.',
 'Command substitution supplies the current weekday and identity.', 'Brace expansion creates three filenames.'
]
d.add_page_break()
table(d,['Command','Prediction before run','Observed output and status','Explanation'],[
 (v['command'],v['prediction'],(v['stdout']+v['stderr']).strip()+'\nstatus '+str(v['status']),e)
 for v,e in zip(pred,explanations)])
body(d,'Echo does not discover files; Bash supplies the expanded arguments. The unquoted space in ls alfa beta.txt produces two failed lookups. Both ls "alfa beta.txt" and ls alfa\\ beta.txt address the single file correctly. Single quotes retain literal text; double quotes still allow parameter and command substitution. GNU ls may display quotes for a space-containing filename when its output is a terminal, but those display quotes are not stored in the name.')
fig(d,'2.1','Files in the required play directory',read('Lab3-4/evidence/play-files.txt'))
def cases(indices):return '\n'.join('$ '+pred[i]['command']+'\n'+pred[i]['stdout']+pred[i]['stderr'] for i in indices)
fig(d,'2.2','Globbing results',cases(range(4)))
fig(d,'2.3','A space containing name and the quoted fix',cases([4,5]))
fig(d,'2.4','Single double and escaped dollar quoting',cases([6]))

head(d,'Part 3 Redirection chaining and jobs')
body(d,'Out.txt received stdout, while err.txt received the diagnostic for /nope. In > all.txt 2>&1, descriptor 1 is changed first and descriptor 2 duplicates that new target. In 2>&1 > all.txt, stderr keeps the original stdout target while only stdout moves to the file. Wc -l < access.log receives stdin and therefore prints a count only; with access.log as an operand it also knows and prints the filename. A semicolon sequences regardless of the previous status; AND runs the next command only after success; OR runs it only after failure. The background sleep was listed, terminated and reaped with status 143.')
fig(d,'3.1','Stdout and stderr in separate files',clip(raw,'+ ls /etc /nope','+ ls /etc /nope > all.txt') if '+ ls /etc /nope > all.txt' in raw else clip(raw,'+ ls /etc /nope','+ tail -2 all.txt'))
fig(d,'3.2','Order of descriptor redirections',clip(raw,'+ tail -2 all.txt','+ echo first'))
fig(d,'3.3','Semicolon AND and OR',clip(raw,'+ false','+ jobpid='))
fig(d,'3.4','Background job and termination',clip(raw,'+ jobpid=','+ cp '))

head(d,'Part 4 Answers to the eight log questions')
body(d,'The artificial dataset uses the exact 2026-10-05 generator supplied in the handout. It is shared assignment input rather than real web traffic. All 500 lines were regenerated. The pipelines compare the result field, preserve tied maxima and sort their output. The four page counts sum to 500 and the seven user failure counts sum to 100. In Q8 the long listing has one extra total header line; the entries are otherwise the same.')
stats=clip(raw,'Q1 failed requests\n')
sections=re.split(r'\n(?=Q[1-8] )',stats)
native_map=json.loads((FIG/'manifest.json').read_text())
i=1
while i<=8:
    current='4.'+str(i)
    next_number='4.'+str(i+1)
    same=i<8 and native_map['lab3-'+current]['file']==native_map['lab3-'+next_number]['file']
    if same:
        fig(d,current+'–'+next_number,'Questions '+str(i)+' and '+str(i+1)+' results',sections[i-1].strip(),capture_number=current)
        i+=2
    else:
        fig(d,current,'Question '+str(i)+' result',sections[i-1].strip())
        i+=1
fig(d,'4.9','Full run of oneliners.sh',stats)

head(d,'Part 5 The report script and its error path')
body(d,'The shebang #!/bin/bash selects Bash when the executable script is launched directly. Before chmod +x, ./report.sh returned permission denied and status 126. The prefix ./ supplies a pathname because the current directory is not searched through PATH here. The error is written to descriptor 2 so stdout remains usable for normal results; exit 1 lets a caller detect failure. The script prints every user from user0 to user6, including zero counts, using its aggregation loop. Optional cron and bonus tasks are not claimed.')
fig(d,'5.1','Source of report.sh',read('Lab3-4/linux/report.sh'))
fig(d,'5.2','Successful report and execute permission check',clip(raw,'+ chmod 644 report.sh','+ ./report.sh nope.log'))
fig(d,'5.3','Missing file diagnostic and status',clip(raw,'+ ./report.sh nope.log','+ bash oneliners.sh'))
head(d,'Conclusions')
body(d,'Argument expansion belongs to Bash before program execution. Descriptor duplication explains the order-sensitive redirection result, while status-dependent operators make failure handling explicit. The one-liners were verified against fixed input totals and the reusable script was tested on success and missing input. Source files, predictions and raw recordings accompany this report.')
(ROOT/'Lab3-4/word').mkdir(exist_ok=True)
d.save(ROOT/'Lab3-4/word/Lab3_TacuIgor_FAF-242.docx')


d=document(4,'The xv6 shell from the outside')
head(d,'Part 1 Sleep and the current interface')
body(d,'The header declares pause rather than sleep. The submitted utility calls pause with validated decimal ticks; sleep 20 returns normally, missing input produces usage, and negative input produces a diagnostic. The Makefile contains the _sleep entry. Forked processes inherit the binary and descriptor context, while pause is the kernel operation that performs the delay.')
fig(d,'1.1','The pause declaration',clip(inspect,'API','UPROGS'))
fig(d,'1.2','Sleep source and registration',read('xv6/user/sleep.c')+'\n'+clip(inspect,'UPROGS','SHELL_KINDS'))
fig(d,'1.3','Sleep with valid and invalid arguments',clip(xv,'$ sleep',' $ args') if ' $ args' in xv else clip(xv,'$ sleep','$ args'))
head(d,'Part 2 Comparing every command in the two shells')
body(d,'The Bash test starts in a fresh directory containing README. Both shells provide execution, descriptor redirection, pipelines, command lists, grouping and background commands. Bash additionally expands wildcards and variables, removes syntactic quotes, and offers readline history and completion. The table records the actual small-shell behavior rather than assuming it implements Bash syntax.')
commands=[('echo hello > f ; cat < f','hello','hello','descriptor redirection'),('ls | grep READ','README','README line','pipe'),('(echo a; echo b) | wc','2 lines 2 words 4 bytes','2 2 4','group and list'),('echo one ; echo two','one then two','one then two','sequence'),('echo bg &','bg and prompt','bg and prompt','background'),('ls *','expands existing names','cannot open *','Bash pathname expansion'),('echo $HOME','/root','$HOME','Bash variable expansion'),('echo "a b"','a b','"a b"','Bash quote removal'),('mkdir d ; cd d ; ls ..','lists parent after changing directory','exec cd failed; lists from original directory','xv6 handles cd only as a whole input line'),('Up Tab Ctrl+R','history and completion','not implemented as Bash readline features','source and PTY inspection')]
table(d,['Command','Bash','xv6','Reason'],commands)
body(d,'There is an important distinction in the last directory case. A cd embedded in a semicolon list is passed through the xv6 execution parser and fails as an external command. Issuing cd d as its own input line does change the parent shell. From there a bare ls fails because xv6 has no PATH search, while /ls .. succeeds. For interactive work, history and completion are valuable additions. Basic quote handling would be a localized tokenizer improvement; full pathname expansion would also require directory traversal.')
fig(d,'2.1','The original comparison commands in Bash',read('Lab3-4/evidence/bash-comparison.txt'))
fig(d,'2.2','The same comparison commands in xv6',clip(comp,'$ echo hello','$ mkdir d'))
fig(d,'2.3','Directory handling and absolute ls (README-filtered listing)',clip(comp,'$ mkdir d'))
head(d,'Part 3 Who expands the argument vector')
body(d,'Both inspectors print only argc and argv. The Linux wildcard experiment in this additional test directory had four C files and one quoted x y operand, giving argc 6 including argv zero. Xv6 passed four arguments: args, the literal *.c, and two values containing the double quote marks. The shell, not the inspector or kernel, is responsible for expansion and syntactic quote removal. Repeated unquoted spaces delimit arguments in both shells; they do not become empty arguments.')
fig(d,'3.1','Args source and UPROGS entry',read('xv6/user/args.c')+'\n'+clip(inspect,'UPROGS','SHELL_KINDS'))
fig(d,'3.2','Argument arrays from xv6',clip(xv,'$ args one','$ echo hello'))
fig(d,'3.3','Argument arrays from Linux',clip(linux,'+ ./args one','+ ls'))
head(d,'Part 4 Reading the shell')
body(d,'This version of user/sh.c has 499 lines. EXEC represents a plain command; REDIR is introduced by < or >; PIPE by |; LIST by a semicolon; and BACK by ampersand. Parentheses group a parsed command tree. Cd is recognized in the parent loop before forking and parsing a general command, so its directory change persists. The parser has no Bash parameter-expansion or globbing stage, explaining the literal * and $HOME results. The five command kinds are visible both in their definitions and in runcmd dispatch.')
fig(d,'4.1','Defined command kinds',clip(inspect,'SHELL_KINDS','SHELL_CASES'))
fig(d,'4.2','Dispatch cases',clip(inspect,'SHELL_CASES','CD'))
fig(d,'4.3','Parent shell implementation of cd',clip(inspect,'CD_IMPLEMENTATION'))
head(d,'Conclusions')
body(d,'The two shells share process and descriptor mechanisms but differ before exec in parsing and expansion. The argument inspector isolates those differences. The additional cd-list test also shows why a small shell feature cannot be assumed to compose exactly as in Bash. Both requested programs and the integrated Makefile are submitted with the full xv6 source and raw console evidence.')
(ROOT/'Lab3-4/word').mkdir(exist_ok=True)
d.save(ROOT/'Lab3-4/word/Lab4_TacuIgor_FAF-242.docx')
print('Built Lab 3 and Lab 4 Word sources under Lab3-4/word')
