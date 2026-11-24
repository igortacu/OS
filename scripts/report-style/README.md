# UTM report structure

The layout follows the LaTeX structure supplied by the user on 24 November 2026:
UTM title page, purpose, tasks, theoretical considerations, practical work and
conclusion. The subject is Operating Systems, the author is Tacu Igor, the group
is FAF-242, and the year is 2026. The verifier name is retained from the existing
course reports. These values and the report-specific introductory text are in
`reports.json`. The UTM logo is the unchanged local `logo_1.png` supplied as the
reference asset.

`utm-template.tex` uses A4, Times New Roman 12 pt, 1.5 line spacing and margins
of 2 cm top/bottom and 2.5 cm left/right. Source and terminal transcripts use
Courier New with single spacing, wrapping and a thin frame. Native screenshots
retain their bytes and aspect ratio, with captions above them. No execution
output is regenerated or altered by the formatting pass.

Run `python3 scripts/build-utm-reports.py` from the repository root to rebuild
all eight main PDFs. Use `--only 11,12,13` to select reports. Requirements:
Python 3, Pandoc, XeLaTeX, Times New Roman, Arial and Courier New. A basic TeX
installation with fontspec, Babel locale support, setspace, graphicx, listings,
caption, float, subcaption, longtable, fancyhdr and hyperref is sufficient;
newtx and titlesec are not required.

Each lab directory contains its generated `utm-report.tex`, using repository-
relative image paths. Compile it from the repository root or regenerate it
through the builder. Labs 1–2 retain their authored technical body under
`Lab1-2/latex/report-body.tex`; the main TeX entry point delegates to the new
report. Labs 3–4 retain both required editable Word deliverables. Build those
with the managed document Python runtime and `scripts/build-word-reports.py`,
then render them with `scripts/export-word-reports.py` before final review.

Main PDFs are kept in the existing laboratory groups. Temporary Word exports,
page images and build diagnostics belong outside the repository. The shared
builder reads the existing report sources and preserves all technical results
and image references. The added Romanian introductory and concluding sections
organize that material without replacing the original execution evidence.
