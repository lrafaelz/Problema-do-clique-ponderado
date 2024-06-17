import pulp

def clique_ILP(graph, k):
    # Cria um problema de otimização
    prob = pulp.LpProblem("Clique_Problem", pulp.LpMaximize)

    # Cria variáveis binárias para cada vértice
    x = pulp.LpVariable.dicts("x", graph.keys(), 0, 1, pulp.LpBinary)

    # Função objetivo: queremos maximizar a soma das variáveis, mas fixamos para o clique de tamanho k
    prob += pulp.lpSum(x[v] for v in graph.keys()) == k

    # Restrições: para todo par de vértices, se ambos estão no clique, eles devem ser adjacentes
    for v1 in graph.keys():
        for v2 in graph.keys():
            if v1 != v2 and v2 not in graph[v1]:
                prob += x[v1] + x[v2] <= 1

    # Resolve o problema
    prob.solve()

    # Obtém os resultados
    clique = [v for v in graph.keys() if pulp.value(x[v]) == 1]
    return clique

# Exemplo de grafo representado como um dicionário de adjacências
graph = {
    1: [2, 3, 4],
    2: [1, 3, 4],
    3: [1, 2],
    4: [1, 2],
    5: [6],
    6: [5]
}

k = 3
clique = clique_ILP(graph, k)
print(f"Clique de tamanho {k} encontrado:", clique)