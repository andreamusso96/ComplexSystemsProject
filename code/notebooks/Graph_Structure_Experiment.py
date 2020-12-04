import numpy as np
import networkx as nx


def build_graph(num_nodes, number_of_additional_edges, centralisation):
    #make sure number_of_additional_edges edges can be added to the graph
    assert 2 * num_nodes + number_of_additional_edges <= num_nodes*(num_nodes - 1), 'not possible'

    # Nodes
    names = range(num_nodes)
    # Graph
    graph = nx.DiGraph()
    graph.add_nodes_from(names)

    # Connect agents in a Circle in both directions so graph is connected
    if num_nodes > 1:
        graph.add_edge(names[0], names[-1])
        graph.add_edge(names[-1], names[0])
        if num_nodes > 2:
            for i in range(num_nodes - 1):
                graph.add_edge(names[i], names[i + 1])
                graph.add_edge(names[i + 1], names[i])

    # Add additional edges according to centralisation
    current_information_provider = None
    for n in range(number_of_additional_edges):
        if n==0:
            # Choose provider and receiver randomly
            current_information_provider = np.random.choice(names)
            information_receiver = np.random.choice([a for a in names if (a != current_information_provider and (not graph.has_edge(current_information_provider, a)))])
            graph.add_edge(current_information_provider, information_receiver)
        else:
            # Change provider with Probability 1 - centralisation
            if np.random.random() > centralisation:
                current_information_provider = np.random.choice([a for a in names if a != current_information_provider])
            # Make sure receiver can be selected
            while len([a for a in names if (a != current_information_provider and (not graph.has_edge(current_information_provider, a)))]) == 0:
                current_information_provider = np.random.choice([a for a in names if a != current_information_provider])
            #Choose receiver randomly
            information_receiver = np.random.choice([a for a in names if (a != current_information_provider and (not graph.has_edge(current_information_provider, a)))])
            graph.add_edge(current_information_provider, information_receiver)

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


