import networkx as nx
import matplotlib.pyplot as plt

# Função para desenhar o grafo, destacando a clique se fornecida
def draw_graph(G, clique=None, filename="weighted_graph.png"):
    pos = nx.spring_layout(G)  # Define as posições dos nós

    # Define as cores dos nós (vermelho para nós na clique, azul claro para os demais)
    node_colors = ['red' if node in clique else 'lightblue' for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors)

    # Desenha as arestas do grafo
    nx.draw_networkx_edges(G, pos, width=2)
    edge_labels = nx.get_edge_attributes(G, 'weight')  # Obtém os rótulos de peso das arestas
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)  # Desenha os rótulos de peso

    # Desenha os rótulos dos nós
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

    plt.axis('off')  # Oculta os eixos
    plt.savefig(filename)  # Salva o gráfico como uma imagem
    plt.clf()  # Limpa o gráfico para o próximo desenho
