# -*- coding: utf-8 -*-
import numpy as np
from gnuplot import FigParams, PlotParams, SpecialParams, gnuplot

# %% Make x and y values
w_0 = 2 # set angular frequency
t = np.linspace(-10, 10, 10000)
y = np.cos(w_0*t)
y2 = np.cos(w_0*t + np.pi/4)
y3 = np.cos(w_0*t + np.pi/2)
y4 = np.cos(w_0*t + 3*np.pi/4)
y5 = np.cos(w_0*t + 2*np.pi)

# %% Plot with Gnuplot
fig_params = FigParams(terminal='epslatex', fig_size=[8, 8], units='cm', 
			  	 color=True, colortext=True, standalone=False, border_line='solid')

plot_params = PlotParams(plot_type='lines', color='black', line_type='solid', 
				 line_width=3, point_type='solid circle', notitle=True, 
				 line_dash='none', xlim=[-5,5], ylim=[-2,2], rotate_tick_vals=None,
				 xlabel='X Values', ylabel='Y Values', xtick_label_format='%.2f', 
				 ytick_label_format='%.2f', error_bars=None, fit_type=None, 
				 graph_label=None, mxticks=3, myticks=3, font_size=20)

special_params = SpecialParams(multi_color=['dark blue', 'light blue', 'green', 'yellow']) 
# special_params = SpecialParams(multi_color=None)
'''  
	Give output file path and name; do not specify an extension, 
    this will be done automatically
'''
output_file = 'plots/output_latex'
data = gnuplot(fig_params=fig_params, plot_params=plot_params,
		data=[t, y, t, y2, t, y3, t, y4], output_file=output_file,
		special_params=special_params)