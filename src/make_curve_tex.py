#!/usr/bin/env python3
# Created: Feb 21, 2025 20:57:15 by Wataru Fukuda

import argparse
import os

def main():
  parser = argparse.ArgumentParser(description="Generate a TeX file")
  parser.add_argument("-n", "--num_of_pieces", required=True, type=int, help="Number of pieces")
  parser.add_argument("-o", "--output", default="pgfplots.tex", help="Output TeX filename")
  parser.add_argument("--output_dir",metavar="output-dir",default="pgfplots")
  options = parser.parse_args()

  num_of_pieces = options.num_of_pieces  # Ensure integer input

  template = r"""\documentclass[multi=minipage,border=0]{standalone}
\usepackage{pgfplots}
\usepackage{filecontents}

\providecommand{\maxnum}{0}

\pgfplotsset{compat=newest}
\pgfplotsset{every axis/.append style={
  axis lines=middle,
  xtick=\empty,
  ytick=\empty,
  axis equal image,
  axis line style={draw=none}
  },
  %=== legend setting ===%
  legend columns=3,
  legend style={
    at={(0.5,-0.2)},
    anchor=north,
    font=\normalsize,
    legend columns=-1,
    legend cell align=left,
    /tikz/every even column/.append style={column sep=0.5cm},
    draw=none,
  },
  %=== cycle list ===%
  cycle list name=color list,
  cycle list={
    {mark=none, color=red},
    {mark=none, color=blue},
    {mark=none, color=orange},
    {mark=none, color=green},
    {mark=none, color=pink},
    {mark=none, color=yellow},
    {mark=none, color=purple},
  },
}

\begin{document}
\begin{tikzpicture}
\begin{axis}
% REPEAT_HERE
  \addplot+[mark=*, color=black] table[x index=0, y index=1] {xyz\maxnum.txt};
\end{axis}
\end{tikzpicture}
\end{document}
"""

  repeat_pattern = r"""
  \addplot+[smooth, tension=1.0, thick] table[x index=0, y index=1] {{GLOBAL/curve{num}.txt}};
  \addlegendentry{{element {num}}};
""".strip("\n")

  repeated_lines = "\n".join(repeat_pattern.format(num=i) for i in range(num_of_pieces))
  final_tex = template.replace("% REPEAT_HERE", repeated_lines)

  os.makedirs(options.output_dir,exist_ok=True)
  with open(os.path.join(options.output_dir,options.output), "w") as f:
    f.write(final_tex)


if __name__ == '__main__':
    main()

