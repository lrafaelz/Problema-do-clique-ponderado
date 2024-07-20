import csv
import networkx as nx
import matplotlib.pyplot as plt
from pulp import LpMaximize, LpProblem, LpStatus, LpVariable, lpSum, value
from deap import base, creator, tools, algorithms
import random
import os

def read_weighted_graph_from_csv_matrix(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)[1:]  # Skip the first column header
        w = {}
        for i, row in enumerate(reader):
            for j, value in enumerate(row[1:]):
                if value != 'NULL' and value != '0':
                    G.add_edge(headers[i], headers[j], weight=float(value))
                    # make a dictionary where ex.: {'a': 1.5, 'b': 3.0...'vertice': weight}
                    w[headers[i]] = w.get(headers[i], 0) + float(value)
                    w[headers[j]] = w.get(headers[j], 0) + float(value)
    return G, w

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


def greedy_clique_weighted(graph):
    cliques = list(nx.find_cliques(graph))
    max_clique = max(cliques, key=lambda clique: sum(graph[u][v]['weight'] for u in clique for v in clique if u != v))
    return max_clique



def notE(V, E):
    nots = []
    for u in V:
        for v in V:
            if u == v: continue
            if not ((u, v) in E or (v, u) in E) and not ((u, v) in E or (v, u) in nots):
                nots.append((u, v))
    return nots

def ilp_clique_weighted(graph, w):
    E = list(graph.edges)
    V = list(graph.nodes)

    print("Vertices und Gewicht:", w)
    print("Edges:               ", E)
    print("Missing edges:       ", notE(V, E))
    # print(V)

    model = LpProblem("MaxCliqueWeighted", LpMaximize)

    xv = {}

    for v in V:
        xv[v] = LpVariable(str(v), lowBound=0, cat='Binary')

    print(w)

    model += lpSum([w[v] * xv[v] for v in V]), "max me"

    nonEdges = notE(V, E)
    for noe in nonEdges:
        model += xv[noe[0]] + xv[noe[1]] <= 1

    model.solve()
    LpStatus[model.status]
    clique = []
    for v in V:
        if xv[v].varValue > 0:
            print(v, 'ist drin mit w =', w[v])
            clique.append(v)

    print('Soma total deste clique:', value(model.objective))

    return clique



def genetic_clique_weighted(graph):
    vertices = list(graph.nodes)
    n = len(vertices)

    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    def create_individual():
        return [random.randint(0, 1) for _ in range(n)]

    def evaluate(individual):
        clique = [vertices[i] for i in range(n) if individual[i] == 1]
        if all(graph.has_edge(i, j) for i in clique for j in clique if i != j):
            weight_sum = sum(graph[i][j]['weight'] for i in clique for j in clique if i != j)
            return (weight_sum,)
        else:
            return (0,)

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=50)
    algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=20, verbose=False)

    best_individual = tools.selBest(population, 1)[0]
    clique = [vertices[i] for i in range(n) if best_individual[i] == 1]
    return clique

if __name__ == "__main__":
    inputPath = os.path.join(os.path.dirname(__file__), '../data/graph.csv')
    outputPath = os.path.join(os.path.dirname(__file__), '../results/')

    print(f"Lendo arquivo: {inputPath}")
    G, w = read_weighted_graph_from_csv_matrix(inputPath)

    print(G)

    print('Greedy clique weighted:')
    clique_greedy = greedy_clique_weighted(G)
    print(clique_greedy)
    draw_graph(G, clique=clique_greedy, filename=(outputPath + 'greedy_clique_weighted.png'))

    print('ILP clique weighted:')
    clique_ilp = ilp_clique_weighted(G, w)
    print(clique_ilp)
    draw_graph(G, clique=clique_ilp, filename=(outputPath + 'ilp_clique_weighted.png'))

    print('Genetic clique weighted:')
    clique_genetic = genetic_clique_weighted(G)
    print(clique_genetic)
    draw_graph(G, clique=clique_genetic, filename=(outputPath + 'genetic_clique_weighted.png'))
