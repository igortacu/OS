#!/usr/bin/env python3
"""Render the two Word sources and publish only the joint Labs 3-4 PDF."""
from pathlib import Path
import argparse,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--python',type=Path,default=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3')
parser.add_argument('--renderer',type=Path)
parser.add_argument('--review-dir',type=Path)
args=parser.parse_args()
if args.renderer is None:
    options=sorted((Path.home()/'.codex/plugins/cache/openai-primary-runtime/documents').glob('*/skills/documents/render_docx.py'))
    if not options:parser.error('Specify --renderer pointing to render_docx.py')
    args.renderer=options[-1]
if not args.python.exists():parser.error('Specify --python with the managed document runtime')
with tempfile.TemporaryDirectory(prefix='os-word-export-') as temp:
    review=args.review_dir.resolve() if args.review_dir else Path(temp)
    pdfs=[]
    for number in (3,4):
        name=f'Lab{number}_TacuIgor_FAF-242'
        output=review/f'lab{number}'
        subprocess.run([str(args.python),str(args.renderer),str(ROOT/'Lab3-4/word'/(name+'.docx')),
                        '--output_dir',str(output),'--emit_pdf'],check=True)
        pdfs.append(output/(name+'.pdf'))
    joint=Path(temp)/'joint.pdf'
    subprocess.run(['pdfunite',*(str(p) for p in pdfs),str(joint)],check=True)
    target=ROOT/'Lab3-4/Lab3-4_TacuIgor_FAF-242.pdf'
    target.write_bytes(joint.read_bytes())
    print('Published',target)
    if args.review_dir:print('Review pages:',review)
