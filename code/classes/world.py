import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation

from .agent import Agent
from .news import News


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
    def __init__(self, num_agents=50, num_sharing=1, news_fitness=0.5, news_truth=1):
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
        assert num_sharing <= num_agents, f'Invalid value for num_sharing. Value has to be smaller than num_agents={num_agents}'
        assert 0 <= news_fitness <= 1, 'Invalid value for news_fitness. Value has to be between 0 and 1'
        assert 0 <= news_truth <= 1, 'Invalid value for news_truth. Value has to be between 0 and 1'

        self.num_agents = num_agents
        self.news = News(news_fitness, news_truth)
        self.agents = self._create_agents()
        self.graph = self._create_graph()
        self.graph_layout = None
        self.fig = None
        self.ax = None

        # Choose the agents that initially share the news
        initial_sharing = np.random.choice(self.graph.nodes(), num_sharing)
        for node in initial_sharing:
            node.update()

    def _create_agents(self):
        """ Creates the agents with random share_threshold and truth_weight values """
        # Choose the threshold values randomly
        share_thresholds = np.random.random(self.num_agents)
        truth_weights = np.random.random(self.num_agents)

        agents = []
        for i in range(self.num_agents):
            agents.append(Agent(share_thresholds[i], truth_weights[i]))

        return agents

    def _create_graph(self):
        """ Create directed graph with agents assigned to the nodes and trust values assigned to the edges """
        small_graph = nx.powerlaw_cluster_graph(len(self.agents), 3, 0.5)
        small_graph = small_graph.to_directed()

        graph = nx.DiGraph()
        graph.add_nodes_from(self.agents)

        for (a, b) in small_graph.edges():
            graph.add_edge(self.agents[a], self.agents[b], weight=np.random.random())

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
            sharing_agents = []
            for node in self.graph.nodes():
                # Go through in-going edges to get providers and trust values
                providers = []
                trust_in_providers = []
                for edge in self.graph.in_edges(node):
                    nbr_node, self_node = edge
                    providers.append(nbr_node)
                    trust_in_providers.append(self.graph.edges[edge]['weight'])

                # Check if agent shares the news
                if node.is_sharing(self.news, providers, np.array(trust_in_providers)):
                    sharing_agents.append(node)

            # Update agents that share the news
            for node in sharing_agents:
                node.update()
            # Update new (increase time)
            self.news.update()

    def draw(self, sharing_color='red', new_figure=True):
        if self.graph_layout is None:
            self.graph_layout = nx.spring_layout(self.graph)

        color_map = []
        for node in self.graph.nodes():
            if node.has_shared:
                color_map.append(sharing_color)
            else:
                color_map.append('blue')
        if new_figure:
            plt.figure()
        nx.draw_networkx(self.graph, pos=self.graph_layout, node_color=color_map, with_labels=False)

    def update_plot(self, n):
        """Calls update function and then draws the graph at frame n as part of the animation."""
        if n > 0:
            self.update()

        self.ax.clear()
        self.draw(new_figure=False)
        self.ax.set_title('Frame ' + str(n))

    def animate(self, frames=10, interval=100, path='animation.mp4'):
        """Runs the animation."""
        if self.fig is None:
            self.fig = plt.figure(figsize=(17, 9), dpi=300)
        if self.ax is None:
            self.ax = self.fig.add_subplot(1, 1, 1)

        if self.graph_layout is None:
            self.graph_layout = nx.spring_layout(self.graph)

        text = "Agents: " + str(self.num_agents) + " news fitness: " + str(self.news.fitness) + " news truth: " + str(self.news.truth_value)
        plt.gcf().text(0.4, 0.07, text , fontsize=14)

        animation = matplotlib.animation.FuncAnimation(self.fig, self.update_plot, frames=frames, interval=interval, repeat=False)
        animation.save(path + str('.mp4'), writer='ffmpeg')

    def get_number_sharing_agents(self):
        """ Returns the number of agents that are currently sharing the news """
        return np.sum([1 for agent in self.agents if agent.has_shared])



