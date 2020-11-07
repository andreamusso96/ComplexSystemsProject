import networkx as nx
from matplotlib import pyplot as plt

from classes.graphplot import * #import graph plot 

#just a little dummy class for testing
class Agent:
	def __init__(self):
		self.share_threshold = np.random.random()
	
def main():
	n = 50
	g = nx.powerlaw_cluster_graph(n, 3, 0.5) #small graph
	agents = [Agent() for _ in range(n)]
	G = nx.Graph() #generate graph with agents
	G.add_nodes_from(agents)
	for (a, b) in g.edges():
		G.add_edge(agents[a], agents[b], object = np.random.random()) #add edges with random edgeweights
	plot(G, clr = lambda a: ColorMaps.plasma(a.share_threshold), # determine node color in dependence of some agent attribute
			size = lambda a: G.degree[a] * 5, 						# determine node size with its degree
			edge_clr = lambda u, v: ColorMaps.blackbody(G[u][v]["object"])) # convert edgeweights into color using ColorMaps class
	
main()