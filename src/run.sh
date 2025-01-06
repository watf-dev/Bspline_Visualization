#!/bin/sh
# Created: Jan, 06, 2025 17:02:15 by Wataru Fukuda
set -eu

OUTPUT=OUTPUT
KNOTS=knots
ORDER=2

./gen_knots.py -o $KNOTS
./make_splines.py $OUTPUT/$KNOTS -p $ORDER
cd pgfplots
cp -r ../$OUTPUT/GLOBAL .
pdflatex -shell-escape pgfplots.tex
pdfcrop --margins 10 pgfplots.pdf output.pdf
open output.pdf
