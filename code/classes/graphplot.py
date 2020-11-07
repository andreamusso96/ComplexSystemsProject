import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import csv

"""
class that has some static methods to compute the rgb value for a value x in [0.0,1.0)
for different color maps
use ColorMaps.<map-function>(x), where <map-function> is one of the implemented functions in the class:
plasma, blackbody
"""
class ColorMaps:
	plasma_map = None #static
	blackbody_map = None #static

	@staticmethod
	def plasma(x):
		assert 0.0 <= x < 1.0, "x has to be in [0.0, 1.0)"
		if ColorMaps.plasma_map is None:
			ColorMaps.plasma_map = readCMap("cmaps/plasma_float_0256")
		i = int(len(ColorMaps.plasma_map) * x) #TODO interpolate
		return ColorMaps.plasma_map[i]
	
	@staticmethod	
	def blackbody(x):
		assert 0.0 <= x < 1.0, "x has to be in [0.0, 1.0)"
		if ColorMaps.blackbody_map is None:
			ColorMaps.blackbody_map = readCMap("cmaps/blackbody_float_0256")
		i = int(len(ColorMaps.blackbody_map) * x) #TODO interpolate
		return ColorMaps.blackbody_map[i]

"""
function that reads triples of values from a .csv file into a list
"""
def readCMap(name):
	map = []
	with open(name + ".csv") as cmap:
		reader = csv.reader(cmap, delimiter=',')
		for row in reader:
			if "#" in row[0]: #comment
				continue
			map.append((float(row[1]), float(row[2]), float(row[3])))
	return map

"""
function to plot a networkx network.
arguments:
	graph: the network that should be plotted
	clr (optional): a lambda function that returns a rgb tuple when called on a node. should have the form 'lambda a: <return rgb tuple>'
		use the ColorMaps class to convert values in [0,1) into colors
	size (optional): lambda function that returns the diameter of a node when called on it. should have the form 'lambda a: <return size>'
	edge_clr (optional): lambda function that returns the color of the edge between two nodes when called on them. 
			form 'lambda u, v: <return rgb tuple>' (see also clr argument)
	ax (optional): specify a matplotlib axis object to draw into (if not specified, a new figure will be created)
"""
def plot(graph, clr = lambda a: (0.0, 0.0, 0.0), size = lambda a: 200, edge_clr = lambda u, v: (0.0, 0.0, 0.0), ax = None):
	if ax == None:
		f = plt.figure(figsize=(17, 9), dpi = 300)
		ax = f.add_subplot(1,1,1)
	nx.draw_networkx(graph, 
					pos = nx.spring_layout(graph),
					ax = ax,
					with_labels = False, 
					node_size = [size(a) for a in list(graph.nodes())],
					node_color = [clr(a) for a in list(graph.nodes())],
					edge_color = [edge_clr(u, v) for u, v in list(graph.edges())]
					)
	
	plt.show()