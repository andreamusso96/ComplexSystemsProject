import networkx as nx
from matplotlib import pyplot as plt
import matplotlib.animation
from classes.graphplot import *  # import graph plot

# Create graph here
class Agent:
    def __init__(self):
        self.share_threshold = np.random.random()
n = 50
g = nx.powerlaw_cluster_graph(n, 3, 0.5)  # small graph
agents = [Agent() for _ in range(n)]
G = nx.Graph()  # generate graph with agents
G.add_nodes_from(agents)
for (a, b) in g.edges():
    G.add_edge(agents[a], agents[b], object=np.random.random())  # add edges with random edgeweights
labels = {}
for i in range(n):
    labels[agents[i]] = round(agents[i].share_threshold, 1)



# Configure plot
f = plt.figure(figsize=(17, 9), dpi=300)
ax = f.add_subplot(1, 1, 1)
positions = nx.spring_layout(G)

clr = lambda a: ColorMaps.plasma(a.share_threshold)
size = lambda a: G.degree[a] * 5
edge_clr = lambda u, v: ColorMaps.blackbody(G[u][v]["object"])


def update(n):
    '''
    Update the graph and draw the new version

    :param n: frame number n
    :return:
    '''
    ax.clear()

    #change graph here
    if n==50:
        G.clear()

    nx.draw_networkx(G,
                     pos=positions,
                     ax=ax,
                     with_labels=True,
                     labels=labels,
                     font_size=6,
                     label=str(n),
                     node_size=[size(a) for a in list(G.nodes())],
                     node_color=[clr(a) for a in list(G.nodes())],
                     edge_color=[edge_clr(u, v) for u, v in list(G.edges())]
                     )

animation = matplotlib.animation.FuncAnimation(f, update, frames=100, interval=10, repeat=False) # frames: amount of time steps,
# interval: length of one frame in ms

plt.show()
#animation.save('animation1.gif', writer='imagemagick')
animation.save('animation1.mp4', writer='ffmpeg')