#!/bin/sh
# Created: Jan, 06, 2025 17:02:15 by Wataru Fukuda
set -eu

ORDER=3
ELEMENT=4
NUM_OF_FUNC=$(( ($ORDER + 1) * 2 + ($ELEMENT - 2) - $ORDER - 1 ))
OUTPUT=OUTPUT
KNOTS=knots
PLOTS=data.txt
BASE=$(pwd)/src

$BASE/gen_knots.py -p $ORDER -e $ELEMENT -o $KNOTS --output_dir $OUTPUT
$BASE/make_splines.py $OUTPUT/$KNOTS -p $ORDER -c $PLOTS
$BASE/make_tex.py -n $NUM_OF_FUNC -o bspline.tex --output_dir pgfplots
cd pgfplots
ln -sf ../$OUTPUT/GLOBAL
ln -sf ../src/curve.tex
ln -sf ../$PLOTS
lualatex -shell-escape "\def\xmin{0} \def\xmax{$ELEMENT} \def\numoffunc{$NUM_OF_FUNC} \input{bspline.tex}"
lualatex curve.tex
pdfcrop --margins 10 bspline.pdf bspline_c.pdf
pdfcrop --margins 10 curve.pdf curve_c.pdf
open bspline_c.pdf
open curve_c.pdf

