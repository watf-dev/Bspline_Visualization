#!/bin/sh
# Created: Jan, 06, 2025 17:02:15 by Wataru Fukuda
set -eu

ORDER=3
ELEMENT=4
NUM_OF_FUNC=$(( ($ORDER + 1) * 2 + ($ELEMENT - 2) - $ORDER - 1 ))
OUTPUT=OUTPUT
KNOTS=knots

rm -rf $OUTPUT/GLOBAL/*
rm -rf pgfplots/GLOBAL/*
rm -rf pgfplots/pgfplots.tex
./gen_knots.py -p $ORDER -e $ELEMENT -o $KNOTS --output_dir $OUTPUT
./make_splines.py $OUTPUT/$KNOTS -p $ORDER
./make_tex.py -n $NUM_OF_FUNC -o pgfplots.tex
cd pgfplots
cp -r ../$OUTPUT/GLOBAL .
lualatex -shell-escape "\def\xmin{0} \def\xmax{$ELEMENT} \def\numoffunc{$NUM_OF_FUNC} \input{pgfplots.tex}"
pdfcrop --margins 10 pgfplots.pdf output.pdf
open output.pdf

