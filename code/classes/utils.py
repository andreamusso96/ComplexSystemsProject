import networkx as nx
import numpy as np
import copy

from agent import Agent
from world import World


def construct_agents(names, thresholds, independence, news, graph):
    """
    Builds instances of Agent class from parameters

    :param names: list of integers, names of the agents
    :param thresholds: list of floats in [0,1], thresholds for the agents
    :param independence: list of floats in [0,1], independence of the agents
    :param news: dictionary, key = name of news, value = news object (see class News)
    :param graph: nx.DiGraph, a directed graph representing the connections between the agents
    :return: agents: a dictionary, key = name of agents, value = agent class
    """
    # Declare the states of all agents with respect to the news. By default all agents are ignorant wrt all news
    states = dict([(n.name, 0) for n in news.values()])

    agents = {}
    for name in names:
        providers = []
        weights_providers = {}
        # For each edge in the graph pointing towards the vertex with name = name of the agent, we add the tail of
        # the edge to the providers of the agent. We also add the weight of the edge to the weights_providers
        for edge in graph.in_edges(name):
            tail, point = edge
            providers.append(tail)
            weights_providers[tail] = graph.edges[edge]['weight']

        # For each edge in the graph pointing away from the vertex with name = name of the agent, we add the point
        # of the edge to the receivers of the agent. We also add the weight of the edge to the weights_receivers
        receivers = []
        weights_receivers = {}
        for edge in graph.out_edges(name):
            tail, point = edge
            receivers.append(point)
            weights_receivers[point] = graph.edges[edge]['weight']

        # Build an instance of the agent class
        agents[name] = Agent(name, copy.deepcopy(states), thresholds[name], independence[name],
                             providers, receivers, weights_providers, weights_receivers)

    return agents


def construct_agent_constant_parameters(number, threshold, independence, news, graph):
    """
    Builds instances of Agent class from constant parameters (i.e. same parameters for all the agents)

    :param number: integer, the number of agents
    :param threshold: float in [0,1], the common threshold of all the agents
    :param independence: float in [0,1], the common independence value of all agents of all the agents
    :param news: dictionary, key = name of news, value = news object (see class News)
    :param graph: nx.DiGraph, a directed graph representing the connections between the agents
    :return:  a dictionary, key = name of agents, value = agent class
    """
    # We construct list/dictionaries of length = number of agents and fill them with the parameter passed in argument
    names = list(range(number))
    thresholds_dict = dict.fromkeys(names, threshold)
    independence_dict = dict.fromkeys(names, independence)

    # We return call to construct_agents (see above)
    return construct_agents(names, thresholds_dict, independence_dict, news, graph)


def create_graph(num_nodes):
    """
    Creates directed graph with agents assigned to the nodes and trust values assigned to the edges

    :param num_nodes: integer, number of nodes in the graph
    :return: graph: nx.DiGraph, a directed graph representing the connections between the agents
    """
    graph = nx.powerlaw_cluster_graph(num_nodes, 3, 0.5)
    graph = graph.to_directed()

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


def construct_world(names_agents, thresholds, independence, news):
    """
    Constructs an instance of the World class from the parameters

    :param names_agents: list of integers, names of the agents
    :param thresholds: list of floats in [0,1], thresholds for the agents
    :param independence: list of floats in [0,1], independence of the agents
    :param news: dictionary, key = name of news, value = news object (see class News)
    :return: world: an instance of the World class, with agents, news and a graph
    """
    # Construct a graph
    graph = create_graph(len(names_agents))

    # Constrict the agents
    agents = construct_agents(names_agents, thresholds, independence, news, graph)

    # Construct the world
    world = World(agents, news, graph)
    return world


def construct_world_constant_parameters(number_agents, threshold, independence, news):
    """
    Constructs an instance of the World class from constant parameters (i.e. the same parameters for all agents)

    :param number_agents: integer, the number of agents
    :param threshold: float in [0,1], the common threshold of all the agents
    :param independence: float in [0,1], the common independence value of all agents of all the agents
    :param news: dictionary, key = name of news, value = news object (see class News)
    :return: world: an instance of the World class, with agents, news and a graph
    """
    # Construct a graph
    graph = create_graph(number_agents)

    # Constrict the agents
    agents = construct_agent_constant_parameters(number_agents, threshold, independence, news, graph)

    # Constrict the world
    world = World(agents, news, graph)
    return world
