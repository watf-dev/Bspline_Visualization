#!/bin/sh
# Created: Jan, 06, 2025 17:02:15 by Wataru Fukuda
set -eu

ORDER=3
ELEMENT=4
NUM_OF_FUNC=$(( ($ORDER + 1) * 2 + ($ELEMENT - 2) - $ORDER - 1 ))
OUTPUT=OUTPUT
KNOTS=knots
XYZ=xyz0.txt
BASE=$(pwd)/src

# mkdir -p $OUTPUT/GLOBAL
# ln -sf ../../$XYZ $OUTPUT/GLOBAL/
# $BASE/gen_knots.py -p $ORDER -e $ELEMENT -o $KNOTS --output_dir $OUTPUT
# $BASE/make_splines.py $OUTPUT/$KNOTS -p $ORDER -c $XYZ
# $BASE/make_bspline_tex.py -n $NUM_OF_FUNC -o bspline.tex --output_dir pgfplots
# $BASE/make_curve_tex.py -n $ELEMENT -o curve.tex --output_dir pgfplots
cd pgfplots
# ln -sf ../$OUTPUT/GLOBAL
# lualatex -shell-escape "\def\xmin{0} \def\xmax{$ELEMENT} \def\numoffunc{$NUM_OF_FUNC} \input{bspline.tex}"
# pdfcrop --margins 10 bspline.pdf bspline_c.pdf
# ln -sf ../$XYZ
# for i in {0..6};do
#   ln -sf ../$OUTPUT/GLOBAL/xyz$i.txt
#   lualatex "\def\maxnum{$i} \input{curve.tex}"
#   pdfcrop --margins 10 curve.pdf curve_c_$i.pdf
# done
for i in {0..6};do
  # $BASE/make_recursiveBspline_tex.py -n $(($NUM_OF_FUNC + $i)) -o recursiveBspline.tex --output_dir .
  # ln -sf ../$OUTPUT/GLOBAL/recursiveBspline$i
  # lualatex -shell-escape "\def\xmin{0} \def\xmax{$ELEMENT} \def\id{$i} \input{recursiveBspline.tex}"
  lualatex -shell-escape "\def\xmin{0} \def\xmax{$ELEMENT} \def\id{$i} \input{recursiveBspline_split.tex}"
  # pdfcrop --margins 0 recursiveBspline.pdf recursiveBspline_c_$i.pdf
  pdfcrop --margins 0 recursiveBspline_split.pdf recursiveBspline_split_c_$i.pdf
done
# open bspline_c.pdf
# open curve_c*.pdf
# open recursiveBspline_c*.pdf
open recursiveBspline_split_c*.pdf
# cd ..
# lualatex src/all_figs.tex

