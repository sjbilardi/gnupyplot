# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from subprocess import call
import numpy as np
import sys
import os

class FigParams:
	'''For holding the figure parameters to be passed to Gnuplot.
	   Note that "standalone" is for use with "epslatex" only.'''

	def __init__(self, terminal='epslatex', fig_size=[8, 8], units='cm', 
			  	 color=True, colortext=True, standalone=False, border_line='solid'):

		self.terminal = terminal
		self.fig_size = fig_size
		self.units = units
		self.color = color
		self.colortext = colortext
		self.standalone = standalone
		self.border_line = border_line

class PlotParams:
	'''For holding the plotting parameters for Gnuplot.'''

	def __init__(self, plot_type='lines', color='black', line_type='solid', 
				 line_width=3, point_type='solid circle', notitle=True, 
				 line_dash='none', xlim=None, ylim=None, rotate_tick_vals=None,
				 xlabel=None, ylabel=None, xtick_label_format=None, 
				 ytick_label_format=None, error_bars=None, 
				 fit_type=None, graph_label=None, mxticks=None, myticks=None,
				 font_size=10):

		self.plot_type = plot_type
		self.color = color
		self.notitle = notitle
		self.line_type = line_type
		self.line_width = line_width
		self.line_dash = line_dash
		self.point_type = point_type
		self.xlim = xlim
		self.ylim = ylim
		self.rotate_tick_vals = rotate_tick_vals
		self.xlabel = xlabel
		self.ylabel = ylabel
		self.xtick_label_format = xtick_label_format
		self.ytick_label_format = ytick_label_format
		self.error_bars = error_bars
		self.fit_type = fit_type
		self.graph_label = graph_label
		self.mxticks = mxticks
		self.myticks = myticks
		self.font_size = font_size

class SpecialParams:
	'''
		Parameters that will override all other parameters. Note
		that "multi_color" is for setting the color of each plot 
		in a single figure.
	'''

	def __init__(self, multi_color=None):

		self.multi_color = multi_color

def _make_data_file(data, output_file, errors=None):
	'''Will write all data to a file so it can be sent to 
	   gunuplot later. File is written as a "txt" file. NOTE:
	   error bars are not supported yet.'''

	if errors == None:
		extension = '.data'
		file = open(output_file+extension, 'w')
		for val in np.arange(len(data[0])):
			temp = ' '
			for variable in np.arange(len(data)):
				temp += str(data[variable][val])
				if variable != (len(data) - 1):
					temp += '\t'
			temp += '\n'
			file.write(temp)
		return True, output_file+extension
	else:
		print('Sorry. Not supported yet.')
		return False, None


def gnuplot(fig_params, plot_params, data, output_file, special_params=None):
	'''Will pass arguments to Gnuplot to 
	   for plotting'''

	# fig_params.terminal == 'epslatex':
	# These dictionaries are for the use with "epslatex"
	ColorParams = {'black': 8, 'purple': 1, 'green': 2, 'light blue': 3,
	 			   'orange': 4, 'yellow': 5, 'dark blue': 6, 'red': 7}
	PointParams = {'plus': 1, 'cross': 2, 'plus and cross': 3, 'square and dot': 4,
				   'solid square': 5, 'circle and dot': 6, 'solid circle': 7,
				   'triangle and dot': 8, 'solid triangle': 9, 'inv solid triangle': 11}
	LineDashType = {'none': 1, 'single long': 1, 'single short': 3, 'dash dot': 4, 
					'double dot': 5}
	
	# Set figure parameters
	if fig_params.terminal == 'xterm':
		term_set = ('set terminal '+fig_params.terminal+' persist; ')
	elif fig_params.terminal == 'epslatex':
		term_set = ('set size square; set terminal '+fig_params.terminal+' size '+str(fig_params.fig_size[0])
					+fig_params.units+', '+str(fig_params.fig_size[1])+fig_params.units)
	elif fig_params.terminal == 'eps':
		term_set = ('set size square; set terminal postscript eps size '+str(fig_params.fig_size[0])
					+fig_params.units+', '+str(fig_params.fig_size[1])+fig_params.units+' font \', '
					+str(plot_params.font_size)+'\'')
	if fig_params.color == True:
		term_set += ' color'
	if fig_params.colortext == True:
		term_set += ' colortext '
	if fig_params.standalone == True and fig_params.terminal == 'epslatex':
		term_set += ' standalone'
	term_set += fig_params.border_line+'; '
	# term_set += 'set key font \', '+str(plot_params.font_size)+'\'; '
	print(term_set)
	# Set output file parameters
	if fig_params.terminal == 'epslatex':
		output = 'set output ' + '\'' + output_file + '.tex' + '\'' + '; '
	elif fig_params.terminal == 'eps':
		output = 'set output ' + '\'' + output_file + '.eps' + '\'' + '; '
	print(output)

	# Set plotting parameters
	args = ''
	if plot_params.mxticks:
		args += 'set mxtics '+str(plot_params.mxticks)+'; '
	if plot_params.myticks:
		args += 'set mytics '+str(plot_params.myticks)+'; '
	if plot_params.xlim:
		args += 'set xrange ['+str(plot_params.xlim[0])+':'+str(plot_params.xlim[1])+']; '
	if plot_params.ylim:
		args += 'set yrange ['+str(plot_params.ylim[0])+':'+str(plot_params.ylim[1])+']; '
	if plot_params.xlabel:
		args += 'set xlabel \''+plot_params.xlabel+'\'; '
	if plot_params.ylabel:
		args += 'set ylabel \''+plot_params.ylabel+'\' offset 2; '
	if plot_params.xtick_label_format:
		args += 'set format x \''+plot_params.xtick_label_format+'\'; '
	if plot_params.ytick_label_format:
		args += 'set format y \''+plot_params.ytick_label_format+'\'; '
	# If a function is given
	if len(data) == 1:
		plot = ('plot '+data+' with '+plot_params.plot_type+' lt '+str(PointParams[plot_params.point_type])
				+' lc '+str(ColorParams[plot_params.color])+' lw '+str(plot_params.line_width)+' dt '+str(LineDashType[plot_params.line_dash]))
	# If a list of data is given
	else:
		plot = ''
		number = 0
		write_data, data_file = _make_data_file(data=data, output_file=output_file, errors=plot_params.error_bars)
		for data_vars in np.arange(1, (len(data)), 2):
			if len(data[0]) == len(data[1]):
				if write_data == True:
					if data_vars == 1:
						plot += 'plot '
					plot += ('\''+data_file+'\' using '+str(int(data_vars))+':'+str(int(data_vars+1))+' with '+plot_params.plot_type+' lt '+
							str(PointParams[plot_params.point_type]))
					if special_params.multi_color:
						if data_vars == 1:
							plot += ' lc '+str(ColorParams[special_params.multi_color[number]])
						else:
							plot += ' lc '+str(ColorParams[special_params.multi_color[data_vars-(data_vars - number)]])
					else:
						plot += ' lc '+str(ColorParams[plot_params.color])
					plot += ' lw '+str(plot_params.line_width)+' dt '+str(LineDashType[plot_params.line_dash])
					if plot_params.notitle == True:
						plot += ' notitle'
					if data_vars != (len(data) - 1):
						plot += ',\\\n'
					else:
						plot += '; '
				else:
					print('Error writing data to file.')
					return 'Error writing to file.'
			else:
				print('X and Y must be same size.')
				return 'X and Y not the same size'
			number += 1
		print(plot)	
	# make final command strings
	if fig_params.terminal == 'epslatex' or fig_params.terminal == 'eps':
		cmd = ('gnuplot -e \"'+term_set+output+args+plot+' \"')
	elif fig_params.terminal == 'xterm':
		cmd = ('xterm -hold -e gnuplot -e \"'+term_set+args+plot+'\"')
	# launch gnuplot
	print(cmd)
	call(cmd, shell=True)
	return data
	