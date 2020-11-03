import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from code.classes.agent import Agent
from code.classes.news import News


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

        # Choose the agents that initially share the news
        initial_sharing = np.random.choice(self.graph.nodes(), num_sharing)
        for node in initial_sharing:
            self.graph.nodes[node]['agent'].update()

    def _create_agents(self):
        """ Creates the agents with random share_threshold and truth_weight values """
        # Choose the threshold values randomly
        share_thresholds = np.random.random(self.num_agents)
        truth_weights = np.random.random(self.num_agents)

        agents = []
        for i in range(self.num_agents):
            agents.append(Agent(share_thresholds[i], truth_weights[i]))

        return agents

    def _create_graph(self, m=5):
        """ Create directed graph with agents assigned to the nodes and trust values assigned to the edges """
        graph = nx.barabasi_albert_graph(len(self.agents), m)
        graph = graph.to_directed()

        # add agents to nodes
        for i, node in enumerate(graph.nodes()):
            graph.nodes[node]['agent'] = self.agents[i]

        # add weights to edges
        for edge in graph.edges():
            graph.edges[edge]['weight'] = np.random.random()

        # TODO: Normalize over in-going edges

        return graph

    def update(self, timesteps=1):
        """
        Simulates the given number of timesteps.

        :param timesteps: int
            Number of timesteps that are simulated
        """
        for i in range(timesteps):
            sharing_agents = []
            for node in self.graph.nodes():
                # Get agent of node
                agent = self.graph.nodes[node]['agent']

                # Go through in-going edges to get providers and trust values
                providers = []
                trust_in_providers = []
                for edge in self.graph.in_edges(node):
                    nbr_node, self_node = edge
                    providers.append(self.graph.nodes[nbr_node]['agent'])
                    trust_in_providers.append(self.graph.edges[edge]['weight'])

                # Check if agent shares the news
                if agent.is_sharing(self.news, providers, np.array(trust_in_providers)):
                    sharing_agents.append(node)

            # Update agents that share the news
            for node in sharing_agents:
                self.graph.nodes[node]['agent'].update()
            # Update new (increase time)
            self.news.update()

    def draw(self, sharing_color='red'):
        color_map = []
        for node in self.graph.nodes():
            if self.graph.nodes[node]['agent'].has_shared:
                color_map.append(sharing_color)
            else:
                color_map.append('blue')

        plt.figure()
        nx.draw_spectral(self.graph, node_color=color_map)

    def get_number_sharing_agents(self):
        """ Returns the number of agents that are currently sharing the news """
        return np.sum([1 for agent in self.agents if agent.has_shared])



