function CodeBlock(block)
  local _, n = block.text:gsub('\n', '')
  if n < 20 then
    return {pandoc.RawBlock('latex','\\par\\noindent\\begin{minipage}{\\linewidth}'),
            block, pandoc.RawBlock('latex','\\end{minipage}\\par')}
  end
end

-- Inline identifiers (including full Git hashes) must not cross the margin.
function Code(code)
  local chars={['\\']='\\textbackslash{}',['{']='\\{',['}']='\\}',
    ['_']='\\_',['%']='\\%',['&']='\\&',['#']='\\#',['$']='\\$',
    ['~']='\\textasciitilde{}',['^']='\\textasciicircum{}'}
  local function escape(s)
    return (s:gsub('.',function(c)return chars[c] or c end))
  end
  local text=code.text:gsub('%S+',function(token)
    if #token<=12 then return escape(token) end
    local parts={};local part={};local n=0
    for _,cp in utf8.codes(token) do
      table.insert(part,utf8.char(cp));n=n+1
      if n==12 then table.insert(parts,escape(table.concat(part)));part={};n=0 end
    end
    if #part>0 then table.insert(parts,escape(table.concat(part))) end
    return table.concat(parts,'\\allowbreak{}')
  end)
  return pandoc.RawInline('latex','{\\ttfamily\\fontsize{10}{12}\\selectfont '..text..'}')
end
