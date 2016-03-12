import matplotlib.pyplot as plt
from subprocess import call
import subprocess
import seaborn as sns
import numpy as np
import sys
import os

class FigParams:
	'''For holding the figure parameters to be passed to Gnuplot.'''

	def __init__(self, terminal='epslatex', fig_size=[8, 8], units='cm', 
			  	 color=True, colortext=True, border_line='solid'):

		self.terminal = terminal
		self.fig_size = fig_size
		self.units = units
		self.color = color
		self.colortext = colortext
		self.border_line = border_line

class PlotParams:
	'''For holding the plotting parameters for Gnuplot'''

	def __init__(self, plot_type='lines', color='black', line_type='solid', 
				 line_width=2, point_type='solid circle', notitle=True, 
				 xlim='none', ylim='none', rotate_tick_vals='none',
				 error_bars=False, function=None, fit_type='none'):

		self.plot_type = plot_type
		self.color = color
		self.notitle = notitle
		self.line_type = line_type
		self.line_width = line_width
		self.point_type = point_type
		self.function = function
		self.xlim = xlim
		self.ylim = ylim
		self.rotate_tick_vals = rotate_tick_vals
		self.error_bars = error_bars
		self.fit_type = fit_type


def gnuplot(fig_params, plot_params, x, y, output_file):
	'''Will pass arguments to Gnuplot to 
	   for plotting'''

	if fig_params.terminal == 'epslatex':
		# These dictionaries are for the use with "epslatex"
		ColorParams = {'black': 8, 'purple': 1, 'green': 2, 'light_blue': 3,
		 			   'orange': 4, 'yellow': 5, 'dark_blue': 6, 'red': 7}
		PointParams = {'plus': 1, 'cross': 2, 'plus and cross': 3, 'square and dot': 4,
					   'solid square': 5, 'circle and dot': 6, 'solid circle': 7,
					   'triangle and dot': 8, 'solid triangle': 9, 'inv solid triangle': 11}
		LineDashType = {'none': 0, 'single long': 1, 'single short': 2, 'dash dot': 3, 
						'double dot': 4}
	
		# Set figure parameters
		term_set = ('set terminal '+fig_params.terminal+' size '+str(fig_params.fig_size[0])
					+fig_params.units+', '+str(fig_params.fig_size[1])+fig_params.units)

		if fig_params.color == True:
			term_set += ' color'
		if fig_params.colortext == True:
			term_set += ' colortext'
		term_set = term_set + ' ' + fig_params.border_line+'; '
		print(term_set)

		# Set output file parameters
		output = 'set output ' + '\'' + output_file + '\'' + '; '
		print(output)

		# Set plotting parameters
		plot = ('plot \'-\' using 1:2 with '+plot_params.plot_type+' lt '+str(PointParams[plot_params.point_type])
				+' lc '+str(ColorParams[plot_params.color]))
		if plot_params.notitle == True:
			plot = plot + ' notitle'
		plot += ';\n'
		print(plot)

		# Plot Data
		data = ' '
		for val in np.arange(len(x)):
			if val == len(x) - 1:
				data = data + str(x[val]) + '\t' + str(y[val]) + ';'
				print(str(x[val]) + '\t' + str(y[val]) + ';')
			else:
				data = data + str(x[val]) + '\t' + str(y[val]) + '; '
				print(str(x[val]) + '\t' + str(y[val]) + '; ')
		# data = plot_params.function
		cmd = ('gnuplot -e \"'+term_set+output+plot+data+'\"')
		# launch gnuplot
		print(cmd)
		call(cmd, shell=True)

	return data

# %% Make x and y values
w_0 = 2 # set angular frequency
t = np.linspace(-10, 10, 1)
y = np.cos(w_0*t)
# %% Plot above with Matplotlib
# plt.close('all')
# sns.set_style("white")
# sns.set_style("ticks")
# plt.figure(figsize=(8,8))
# plt.plot(t, y)
# plt.show()  

# %% Plot with Gnuplot
fig_params = FigParams()
plot_params = PlotParams()
plot_params.function = 'sin(x)'
output_file = 'plots/output.tex'
data = gnuplot(fig_params=fig_params, plot_params=plot_params,
		x=t, y=y, output_file=output_file)
	