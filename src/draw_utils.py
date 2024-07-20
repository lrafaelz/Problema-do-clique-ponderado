import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G, clique=None, filename="weighted_graph.png"):
    pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    node_colors = ['red' if node in clique else 'lightblue' for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors)

    # edges
    nx.draw_networkx_edges(G, pos, width=2)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

    plt.axis('off')  # Hide the axes
    plt.savefig(filename)
    plt.clf()  # Clear the plot for the next drawing
