import networkx as nx
from graphplot import ColorMaps
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import ArrowStyle


class World:
    def __init__(self, agents, news, graph):
        """
        :param news: dictionary, key = name of news, value = news object (see class News)
        :param agents: dictionary, key = name of the agent, value = agent object (see class Agent)
        :param graph: nx.DiGraph, a directed graph representing the connections between the agents
        """
        self.agents = agents
        self.news = news
        self.graph = graph
        self.time = 0

        # Attributes for rendering
        self.graph_layout = None
        self.fig = None
        self.ax = None

    def update(self):
        """
        Update function of the class world. When called it executes one time step.
        """

        # First, we update the parameters of the news.
        for nw in self.news.values():
            nw.update()

        # Second we identify which agents are changing state a time self.time
        agents_changing_state = {}

        for agent in self.agents.values():  # Iterate through the agents
            updated_states = agent.updated_states(self.news, self.agents)  # Compute the updated states of the agents
            if agent.states != updated_states:  # If the updated states differ from the current states
                agents_changing_state[
                    agent.name] = updated_states  # Add the agent to the agents which are changing state

        # Third we modify the states of the agents who's states should be modified
        for agent_name in agents_changing_state:
            self.agents[agent_name].states = agents_changing_state[agent_name]

        # Note: we first find the agents that should change state and then we modify their states
        # We do so in order to not have some weird cycles in which changing the state of an agent impacts if the states
        # of other agents should be changed

        self.time = self.time + 1

    def draw(self, node_color_function=lambda a: ColorMaps.coolwarm(1 if a.is_active() else 0),
             node_size_function=lambda a: 25, edge_color_function=lambda x, y: (0, 0, 0), show=False):
        if self.fig is None:  # add figure if this is called outside of animation
            self.fig = plt.figure(figsize=(17, 9), dpi=300)
        if self.ax is None:  # add subplot if this is called outside of animation
            self.ax = self.fig.add_subplot(1, 1, 1)
        if self.graph_layout is None:
            self.graph_layout = nx.spring_layout(self.graph)

        self.plot(self.graph,
                  pos=self.graph_layout,
                  clr=node_color_function,
                  size=node_size_function,
                  edge_clr=edge_color_function,
                  ax=self.ax)
        if show:
            self.fig.show()
            plt.show()

    def _next_frame(self, n):
        """Calls update function and then draws the graph at frame n as part of the animation."""
        if n > 0:
            self.update()

        self.ax.clear()
        self.draw()
        self.ax.set_title('Frame ' + str(n))

    def animate(self, frames=10, interval=1000, path='animation'):
        """ Runs the animation. """
        if self.fig is None:
            self.fig = plt.figure(figsize=(17, 9), dpi=300)
        if self.ax is None:
            self.ax = self.fig.add_subplot(1, 1, 1)

        text = "Agents: " + str(len(self.agents)) 
        plt.gcf().text(0.4, 0.07, text, fontsize=14)

        animation = FuncAnimation(self.fig, self._next_frame, frames=frames, interval=interval, repeat=False)
        animation.save(path + str('.mp4'), writer='ffmpeg')

    def plot(self, graph, pos=None, clr=lambda a: (0.0, 0.0, 0.0), size=lambda a: 200,
             edge_clr=lambda u, v: (0.0, 0.0, 0.0),
             ax=None):
        """
        function to plot a networkx network.
        arguments:
            graph: the network that should be plotted
            pos (optional): dictionary providing the positions of each node
            clr (optional): a lambda function that returns a rgb tuple when called on a node. should have the form 'lambda a: <return rgb tuple>'
                use the ColorMaps class to convert values in [0,1) into colors
            size (optional): lambda function that returns the diameter of a node when called on it. should have the form 'lambda a: <return size>'
            edge_clr (optional): lambda function that returns the color of the edge between two nodes when called on them.
                form 'lambda u, v: <return rgb tuple>' (see also clr argument)
            ax (optional): specify a matplotlib axis object to draw into (if not specified, a new figure will be created)
        """
        if ax is None:
            f = plt.figure(figsize=(17, 9), dpi=300)
            ax = f.add_subplot(1, 1, 1)
        if pos is None:
            pos = nx.spring_layout(graph)

        nx.draw_networkx(graph,
                         pos=pos,
                         ax=ax,
                         arrowstyle=ArrowStyle.CurveFilledB(head_length=0.2, head_width=0.1),
                         arrowsize=max(-0.04 * graph.order() + 10, 1),
                         with_labels=False,
                         node_size=[size(self.agents[a]) for a in list(graph.nodes())],
                         node_color=[clr(self.agents[a]) for a in list(graph.nodes())],
                         edge_color=[edge_clr(u, v) for u, v in list(graph.edges())],
                         alpha=0.8,
                         linewidths=0.0,
                         width=0.2
                         )
