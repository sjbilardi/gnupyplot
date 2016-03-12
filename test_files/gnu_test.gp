set terminal epslatex size 9cm,7cm color colortext solid 
set output 'test_plot.tex'

plot '-' using 1:2 with points lt 7 lc 7 notitle
0 0
1 1
2 2
3 3
4 4
