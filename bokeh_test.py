from bokeh.io import output_notebook,show,reset_output

import bokeh

from bokeh.plotting import figure

import numpy as np
import  pandas as pd

from vega_datasets import  data as vds

reset_output()

from bokeh.sampledata import  iris
iris_dataset = iris.flowers
print(iris_dataset)


from  bokeh.models import  HoverTool



x_line = np.arange(10)
y_line =np.random.rand (10)

line_plot = figure(plot_width =500,plot_height=325, title='LINE_PLOT', x_axis_label= 'x', y_axis_label = 'Y' )
line_plot.line(x_line,y_line,legend_label ='line',line_width=2)

line_plot.add_tools(HoverTool())


show(line_plot)