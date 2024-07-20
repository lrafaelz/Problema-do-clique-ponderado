import networkx as nx
from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value, LpStatus
from deap import base, creator, tools, algorithms
import random
from graph_utils import notE

def greedy_clique_weighted(graph):
    cliques = list(nx.find_cliques(graph))
    max_clique = max(cliques, key=lambda clique: sum(graph[u][v]['weight'] for u in clique for v in clique if u != v))
    return max_clique

def ilp_clique_weighted(graph, w):
    E = list(graph.edges)
    V = list(graph.nodes)

    model = LpProblem("MaxCliqueWeighted", LpMaximize)

    xv = {v: LpVariable(str(v), lowBound=0, cat='Binary') for v in V}

    model += lpSum([w[v] * xv[v] for v in V]), "max me"

    nonEdges = notE(V, E)
    for noe in nonEdges:
        model += xv[noe[0]] + xv[noe[1]] <= 1

    model.solve()
    LpStatus[model.status]
    clique = [v for v in V if xv[v].varValue > 0]

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
