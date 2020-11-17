import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from agent import Agent
from news import News


class World:
    """
    Represents the world in which the agents live and interact.

    Attributes:
        num_agents: int
            Number of agents
        news: News
            news that is shared in the network
        agents: list of Agents
        graph: nx.DiGraph
            Represents the interaction between the agents
        graph_layout:
            Graph layout which is used to make sure that successive graphs share the same layout

    Methods:
        update()
            Simulate the agent interactions
        get_number_sharing_agents()
            Return the number of agents that currently share the news

    """

    def __init__(self, num_agents=50, num_sharing=1, news_fitness=0.5, news_truth=1, agents=None, graph=None):
        """
        Represents the world in which the agents live and interact.

        :param num_agents: int
            Number of agents
        :param num_sharing: int
            Number of agents that initially share the news (has to be smaller than num_agents)
        :param news_fitness: float in [0, 1]
            Fitness of news
        :param news_truth: float in [0, 1]
            Truth value of news
        """
        assert num_sharing <= num_agents, f'Invalid value for num_sharing. Value has to be smaller than num_agents'
        assert 0 <= news_fitness <= 1, 'Invalid value for news_fitness. Value has to be between 0 and 1'
        assert 0 <= news_truth <= 1, 'Invalid value for news_truth. Value has to be between 0 and 1'

        self.num_agents = num_agents
        self.news = News(news_fitness, news_truth)
        self.agents = agents if agents is not None else self._create_agents()
        self.graph = graph if graph is not None else self._create_graph()

        # Attributes for rendering
        self.graph_layout = None
        self.fig = None
        self.ax = None

        # Choose the agents that initially share the news
        initial_sharing = np.random.choice(self.graph.nodes(), num_sharing)
        for node in initial_sharing:
            node.is_active = True

    def _create_agents(self):
        """ Creates the agents with random share_threshold and truth_weight values """
        # Choose the threshold values randomly
        share_thresholds = np.random.random(self.num_agents)
        truth_weights = np.random.random(self.num_agents)

        agents = []
        for i in range(self.num_agents):
            agents.append(Agent(str(i), share_thresholds[i], truth_weights[i]))

        return agents

    def _create_graph(self):
        """ Create directed graph with agents assigned to the nodes and trust values assigned to the edges """
        small_graph = nx.powerlaw_cluster_graph(len(self.agents), 3, 0.5)
        small_graph = small_graph.to_directed()

        graph = nx.DiGraph()
        graph.add_nodes_from(self.agents)

        # Same weight for all edges
        for (a, b) in small_graph.edges():
            graph.add_edge(self.agents[a], self.agents[b], weight=1.0)

        # Normalize over in-going edges
        for node in graph.nodes():
            sum_ingoing = np.sum(attr['weight'] for a, b, attr in graph.in_edges(node, data=True))
            for edge in graph.in_edges(node):
                graph.edges[edge]['weight'] /= sum_ingoing

        return graph

    def update(self, time_steps=1):
        """
        Simulates the given number of timesteps.

        :param time_steps: int
            Number of timesteps that are simulated
        """
        for i in range(time_steps):
            activating_nodes = []
            # Go through all the nodes
            for node in self.graph.nodes():

                # Update the status of each node in order

                # Go through in-going edges to get providers and trust values
                providers = []
                trust_in_providers = {}
                for edge in self.graph.in_edges(node):
                    nbr_node, self_node = edge
                    providers.append(nbr_node)
                    trust_in_providers[nbr_node.name] = self.graph.edges[edge]['weight']

                # Check if the node activates
                if node.activates(self.news, providers, trust_in_providers):
                    activating_nodes.append(node)

            # Activate all nodes which should be active this round
            for node in activating_nodes:
                node.is_active = True

            # Update the time in the news
            self.news.update()

    def draw(self, node_color_function=lambda a: ColorMaps.coolwarm(1 if a.has_shared else 0),
             node_size_function=lambda a: 200, edge_color_function=lambda x, y: (0, 0, 0), new_figure=True):

        if self.graph_layout is None:
            self.graph_layout = nx.spring_layout(self.graph)
        if new_figure:
            plt.figure()

        plot(self.graph,
             pos=self.graph_layout,
             clr=node_color_function,
             size=node_size_function,
             edge_clr=edge_color_function,
             ax=self.ax)

    def _next_frame(self, n):
        """Calls update function and then draws the graph at frame n as part of the animation."""
        if n > 0:
            self.update()

        self.ax.clear()
        self.draw(new_figure=False)
        self.ax.set_title('Frame ' + str(n))

    def animate(self, frames=10, interval=100, path='animation'):
        """Runs the animation."""
        if self.fig is None:
            self.fig = plt.figure(figsize=(17, 9), dpi=300)
        if self.ax is None:
            self.ax = self.fig.add_subplot(1, 1, 1)

        text = "Agents: " + str(self.num_agents) + " news fitness: " + str(self.news.fitness) + " news truth: " + str(
            self.news.truth_value)
        plt.gcf().text(0.4, 0.07, text, fontsize=14)

        animation = FuncAnimation(self.fig, self._next_frame, frames=frames, interval=interval, repeat=False)
        animation.save(path + str('.mp4'), writer='ffmpeg')

    def get_number_active_agents(self):
        """ Returns the number of agents that are currently sharing the news """
        return np.sum([1 for agent in self.agents if agent.is_active])
