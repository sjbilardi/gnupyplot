set size square
set terminal postscript eps size 8cm, 8cm color colortext solid;
set output 'output.eps';
plot '-' using 1:2 with lines lt 7 lc 8 lw 2 dt 5 notitle;
 -10.0	0.408082061813;
-5.0	-0.839071529076;
0.0	1.0;
5.0	-0.839071529076;
10.0	0.408082061813;
e;
