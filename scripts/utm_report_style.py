"""Shared UTM report metadata and title-page construction."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / 'scripts/report-style'
CONFIG = json.loads((STYLE / 'reports.json').read_text())

def tex(text):
    chars = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
             '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(chars.get(c, c) for c in text)

def cover(key):
    item = CONFIG['reports'][key]
    return r'''\begin{titlepage}
\thispagestyle{empty}
\begin{center}
\setstretch{1.18}
\includegraphics[width=0.23\textwidth]{''' + 'scripts/report-style/utm-logo.png' + r'''}\\[12pt]
\textbf{MINISTERUL EDUCAȚIEI ȘI CERCETĂRII}\\
\textbf{AL REPUBLICII MOLDOVA}\\[4pt]
\textbf{Universitatea Tehnică a Moldovei}\\
\textbf{Facultatea de Calculatoare, Informatică și Microelectronică}\\
\textbf{Departamentul Inginerie Software și Automatică}\\[36pt]
{\fontsize{22}{26}\selectfont\textbf{Raport}}\\[10pt]
Lucrare de laborator nr. ''' + tex(item['number']) + r'''\\[8pt]
\textbf{\large Sisteme de operare}\\[24pt]
\textbf{Tema:} ''' + tex(item['topic']) + r'''
\end{center}
\vfill
\begin{flushright}
\setstretch{1.25}
Realizat de:\\
stud. gr. ''' + tex(CONFIG['group']) + ', ' + tex(CONFIG['author']) + r'''\\[24pt]
Verificat de:\\
''' + tex(CONFIG['verifier']) + r'''
\end{flushright}
\vfill
\begin{center}\textbf{Chișinău – ''' + tex(CONFIG['year']) + r''' }\end{center}
\end{titlepage}
'''

def intro_md(key):
    item = CONFIG['reports'][key]
    return ('# Scopul lucrării\n\n' + item['purpose'] + '\n\n# Sarcina lucrării\n\n' +
            '\n'.join('- '+x for x in item['tasks']) + '\n\n# Considerații teoretice\n\n' +
            item['theory'] + '\n\n# Implementare. Rezultate practice\n\n')

def word_cover_and_intro(d, number):
    from docx.shared import Cm, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    item = CONFIG['reports'][str(number)]
    sec = d.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.top_margin = sec.bottom_margin = Cm(2)
    sec.left_margin = sec.right_margin = Cm(2.5)
    sec.different_first_page_header_footer = True
    normal = d.styles['Normal']
    normal.font.name, normal.font.size = 'Times New Roman', Pt(12)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(6)
    for name, size in [('Title', 22), ('Heading 1', 16), ('Heading 2', 14), ('Heading 3', 12)]:
        st = d.styles[name]; st.font.name = 'Times New Roman'; st.font.size = Pt(size)
        st.font.color.rgb = RGBColor(0,0,0)
        st.paragraph_format.space_before = Pt(14); st.paragraph_format.space_after = Pt(7)
    # Remove inherited theme fonts and the built-in blue Title rule.
    for style in d.styles:
        for border in style.element.xpath('.//w:pBdr'):
            border.getparent().remove(border)
        for fonts in style.element.xpath('.//w:rFonts'):
            for attr in list(fonts.attrib):
                if 'theme' in attr.lower():del fonts.attrib[attr]
    def para(text='', bold=False, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, after=0):
        p=d.add_paragraph();p.alignment=align;p.paragraph_format.line_spacing=1.18
        p.paragraph_format.space_after=Pt(after)
        r=p.add_run(text);r.bold=bold;r.font.size=Pt(size)
        return p
    p=para(after=12);p.add_run().add_picture(str(STYLE/'utm-logo.png'),width=Cm(3.68))
    for text in ['MINISTERUL EDUCAȚIEI ȘI CERCETĂRII', 'AL REPUBLICII MOLDOVA',
                 'Universitatea Tehnică a Moldovei',
                 'Facultatea de Calculatoare, Informatică și Microelectronică',
                 'Departamentul Inginerie Software și Automatică']:
        para(text,bold=True)
    para(after=25)
    para('Raport',bold=True,size=22,after=8).style=d.styles['Title']
    para('Lucrare de laborator nr. '+item['number'],after=8)
    para('Sisteme de operare',bold=True,size=14,after=22)
    para('Tema: '+item['topic'],after=50)
    para('Realizat de:',align=WD_ALIGN_PARAGRAPH.RIGHT)
    para('stud. gr. '+CONFIG['group']+', '+CONFIG['author'],align=WD_ALIGN_PARAGRAPH.RIGHT,after=24)
    para('Verificat de:',align=WD_ALIGN_PARAGRAPH.RIGHT)
    para(CONFIG['verifier'],align=WD_ALIGN_PARAGRAPH.RIGHT,after=50)
    para('Chișinău – '+CONFIG['year'],bold=True)
    p=sec.footer.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');p._p.append(field)
    from docx.enum.section import WD_SECTION_START
    bodysec=d.add_section(WD_SECTION_START.NEW_PAGE)
    bodysec.different_first_page_header_footer=False
    bodysec.footer.is_linked_to_previous=False
    num=OxmlElement('w:pgNumType');num.set(qn('w:start'),'1');bodysec._sectPr.append(num)
    p=bodysec.footer.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
    field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');p._p.append(field)
    for heading,content in [('Scopul lucrării',item['purpose']), ('Sarcina lucrării',None),
                            ('Considerații teoretice',item['theory'])]:
        d.add_heading(heading,1)
        if content:d.add_paragraph(content)
        else:
            for task in item['tasks']:d.add_paragraph(task,style='List Bullet')
    d.add_heading('Implementare. Rezultate practice',1)
