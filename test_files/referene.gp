set terminal epslatex size 9cm,7cm color colortext solid 
set output 'test_plot.tex'

set mxtics 5
set mytics 4
#set ytics 1.986,0.004,2.004 
set xrange [8.8:15.8] 
set yrange [2.17:3.80]
set format y "%.2f" 
set format x "%.2f"
set xlabel '\small{Normal Force (N)}'
set ylabel '\small{Static Friction (N)}' offset 1.0

f(x) = a * x + b
a = 0.1 
b = 2 
fit f(x) "F_n_vs_F_s.txt" via a,b

stats "F_n_vs_F_s.txt" using 1:2 prefix "R"
R2 = R_correlation**2
set label 1 sprintf('\small{$y = %.3f x + %.3f$}', a, R_correlation) at 9.2,3.65
set label 2 sprintf('\small{$r^2 = %.3f$}', R2) at 9.2,3.50

plot "F_n_vs_F_s.txt" using 1:2 with points lt 7 lc 7 notitle,\
f(x) lt 3 lc 8 notitle 
exit