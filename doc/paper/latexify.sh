#!/usr/bin/env sh

PAPER="paper"
TEX=$PAPER.tex

makeindex $PAPER.nlo -s nomencl.ist -o $PAPER.nls

for i in [1..3]; do
	latexmk -pdf $TEX
done

latexmk -c $TEX
#rm -f $PAPER.run.xml $PAPER-blx.bib $PAPER.bbl $PAPER.nlo $PAPER.nls

