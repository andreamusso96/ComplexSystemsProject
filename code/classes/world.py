import networkx as nx
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .agent import Agent
from .news import News
from .graphplot import ColorMaps, plot


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

        # Attributes for the simulation
        self.next_nodes = []

        # Choose the agents that initially share the news
        initial_sharing = np.random.choice(self.graph.nodes(), num_sharing)
        for node in initial_sharing:
            node.activate()
            # Add out-going nodes to next_nodes
            for (self_node, nbr_node) in self.graph.edges(node):
                self.next_nodes.append(nbr_node)

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

        # Add edges to graph
        for (a, b) in small_graph.edges():
            graph.add_edge(self.agents[a], self.agents[b])

        # Set weights on edges
        for node in graph.nodes():
            # Set out-degree as weight on out-going edges
            out_degree = graph.out_degree[node]
            for edge in graph.edges(node):
                graph.edges[edge]['weight'] = out_degree

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
            for node in self.next_nodes:
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

            # Empty next_nodes
            self.next_nodes = []
            
            # Stop the news spreading if during last step no node changed his state
            if not activating_nodes :break
            # Activate all nodes which active this round
            for node in activating_nodes:
                node.activate()
                # Add out-going nodes to next_nodes
                for (self_node, nbr_node) in self.graph.edges(node):
                    self.next_nodes.append(nbr_node)

            # Update the time in the news
            self.news.update()

    def draw(self, node_color_function=lambda a: ColorMaps.coolwarm(1 if a.is_active else 0),
             node_size_function=lambda a: 200, edge_color_function=lambda x, y: (0, 0, 0)):

        if self.graph_layout is None:
            self.graph_layout = nx.spring_layout(self.graph)
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
        self.draw()
        self.ax.set_title('Frame ' + str(n))

    def animate(self, frames=10, interval=1000, path='animation'):
        """ Runs the animation. """
        if self.fig is None:
            self.fig = plt.figure(figsize=(17, 9), dpi=300)
        if self.ax is None:
            self.ax = self.fig.add_subplot(1, 1, 1)

        text = "Agents: " + str(self.num_agents) + " news fitness: " + str(self.news.fitness) + " news truth: " + str(self.news.truth_value)
        plt.gcf().text(0.4, 0.07, text, fontsize=14)

        animation = FuncAnimation(self.fig, self._next_frame, frames=frames, interval=interval, repeat=False)
        animation.save(path + str('.mp4'), writer='ffmpeg')

    def get_number_active_agents(self):
        """ Returns the number of agents that are currently sharing the news """
        return np.sum([1 for agent in self.agents if agent.is_active])
		
	def get_expected_number_of_influenced_agents(self, start_agent, probs):
		"""calculate expected number of influenced agents, discounting any agents that are already influenced (stored in probabilities)"""
		queue = [(start_agent, 1.0)]
		expected = 0.0
		#Problem with this BFS: agents can have pairwise bidirectional influences on each other so which one can influence which is arbitrary here
		#one workaround could be to use a Priority Queue
		while len(queue) > 0: 
			agent, p = queue.pop(0)
			additional_influence = p if 1.0 - probs[agent] >= p else 1.0 - probs[agent]
			expected += additional_influence
			probs[agent] += additional_influence
			# probs[agent] = probability of agent becoming active given start_agent started sending news
			for x, neighbour in self.graph.out_edges(agent):
				if probs[neighbour] < 1.0: # what condition here?
					influence = 0 #how is this calculated
					queue.append(neighbour, influence)
		return (expected, probs) 
	
	def approx_most_influential(self, k):
		"""approximate k-set of most influential nodes"""
		most_influential = []
		probs = dict()
		for i in range(k):
			best = None
			probscopy = None
			expected_reached = -1
			for agent in self.agents:
				n, n_probs = get_expected_number_of_influenced_agents(agent, probs.copy())
				if (n > expected_reached):
					best = agent
					probscopy = n_probs
					expected_reached = n
			most_influential.append(best)
			probs = probscopy
		return most_influential
