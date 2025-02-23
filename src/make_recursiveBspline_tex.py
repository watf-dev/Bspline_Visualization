#!/usr/bin/env python3
# Created: Feb 21, 2025 20:57:15 by Wataru Fukuda

import argparse
import os

def main():
  parser = argparse.ArgumentParser(description="Generate a TeX file")
  parser.add_argument("-n", "--num_of_funcs", required=True, type=int, help="Number of functions to plot")
  parser.add_argument("-o", "--output", default="pgfplots.tex", help="Output TeX filename")
  parser.add_argument("--output_dir",metavar="output-dir",default="pgfplots")
  options = parser.parse_args()

  num_of_funcs = options.num_of_funcs  # Ensure integer input

  template = r"""\documentclass[multi=minipage,border=0]{standalone}
\usepackage{amsmath,amssymb,mathtools}
\usepackage{pgfplots,tikz}
\usepackage{geometry}
\usepackage[T1]{fontenc}
\usepackage[scaled]{helvet}
\usepackage{pgffor}
\renewcommand*\familydefault{\sfdefault}

\providecommand{\xmin}{0}
\providecommand{\xmax}{0}
\providecommand{\id}{0}

\pgfplotsset{compat=newest}
\pgfplotsset{every axis/.append style={
  thick,
  solid,
  grid=major,
  axis equal image,
  scale only axis=true,
  %=== x setting ===%
  xmin=\xmin, xmax=\xmax,
  xtick={\xmin,...,\xmax},
  xlabel={$\Xi$},
  %=== y setting ===%
  ymin=0, ymax=1,
  ytick={0,1},
  ylabel={$N_a$},
  %=== legend setting ===%
  legend columns=7,
  legend style={
    at={(0.5,-0.4)},
    anchor=north,
    font=\normalsize,
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
}}

\begin{document}
\begin{tikzpicture}
\begin{axis}
% REPEAT_HERE
\end{axis}
\end{tikzpicture}
\end{document}
"""

  repeat_pattern = r"""
  \addplot table [x index=0, y index=1] {{GLOBAL/recursiveBspline\id/recursiveBspline{num}.txt}};
  \addlegendentry{{$N_{{{num}}}$}};
""".strip("\n")

  repeated_lines = "\n".join(repeat_pattern.format(num=i) for i in range(num_of_funcs+1))
  final_tex = template.replace("% REPEAT_HERE", repeated_lines)

  os.makedirs(options.output_dir,exist_ok=True)
  with open(os.path.join(options.output_dir,options.output), "w") as f:
    f.write(final_tex)


if __name__ == '__main__':
    main()

