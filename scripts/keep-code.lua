function CodeBlock(block)
  return {
    pandoc.RawBlock('latex', '\\par\\smallskip\\noindent\\begin{minipage}{\\linewidth}'),
    block,
    pandoc.RawBlock('latex', '\\end{minipage}\\par\\smallskip')
  }
end
