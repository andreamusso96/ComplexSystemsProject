import networkx as nx
import numpy as np
import copy

from .agent import Agent, AgentState
from .world import World


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
    states = dict([(n.name, AgentState.IGNORANT) for n in news.values()])

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
    
def reachable(network, starting_set):
    """
    does DFS over network and counts how many nodes are reachable form the nodes in the starting set
    
    :param network: networkx network
    :param starting_set: the set of nodes of the network from which reachability is tested
    :return: integer: the number of agents that are reachable form the starting set    
    """
    vis = {} #use map to tag visited nodes
    reached = 0
    #init
    for agent in network.nodes(): 
        vis[agent] = False
    for agent in starting_set:
        vis[agent] = True
        reached += 1
    #iterative DFS
    stack = starting_set.copy() #copy so that starting_set is not changed
    while len(stack) > 0: #while stack not empty
        v = stack.pop()
        for n in network[v]: #for every neighbour
            if not vis[n]: #if it is not visited
                vis[n] = True #tag as visited
                reached += 1
                stack.append(n) #push onto stack
    return reached
    
def get_expected_number_of_influenced_agents(world, start_agents, n_iterations):
    """
    calculate expected number of influenced agents (average over n_iterations)
    :param world: world
    :param start_agents: list of agents whose influence should be approximated
    :param n_iterations: number of iterations that are made (more means more accurate approximation)
    :return: double: expected number of agents influenced if news starts at agents in stating set
    """
    expected = 0
    for iter in range(n_iterations):
        sample_graph = nx.DiGraph() 
        sample_graph.add_nodes_from(world.graph.nodes())
        for a in sample_graph.nodes():
            providers = world.agents[a].providers.copy()
            pr = [world.agents[a].independence * world.agents[a].weights_providers[prov] for prov in providers] #also a copy
            pr.append(1.0 - sum(pr))
            providers.append(None)
            c = np.random.choice(providers, p=pr)
            if c is not None:
                sample_graph.add_edge(c, a)
        expected += reachable(sample_graph, start_agents)
    return expected / n_iterations
    
def approx_most_influential(world, k, sample_size=100, verbose=True):
    """
    approximate k-set of most influential nodes
    :param world: world
    :param k: integer: gives the size of the set that is sought
    :param sample_size: integer: the number of times a graph is sampled, higher means more accurate approximation
    :return: list: k-set of agents that are expected to be the k most influential nodes in the network (approximation)
    """
    most_influential = []
    for i in range(k):
        best = None
        expected_reached = -1
        for a in world.agents.keys():
            most_influential.append(a) #add current agent
            e = get_expected_number_of_influenced_agents(world, most_influential, sample_size) #sample graphs
            if e > expected_reached:
                best = a
                expected_reached = e
            most_influential.pop() #remove current agent
        most_influential.append(best) #add best agent
        if verbose: 
            print(world.agents[most_influential[-1]].name)
    return [world.agents[a] for a in most_influential]
