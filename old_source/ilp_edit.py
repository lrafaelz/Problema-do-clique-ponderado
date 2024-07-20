import numpy as np
import pandas as pd
import networkx as nx
import pulp
import os

# Função para ler a matriz do arquivo CSV e imprimir no console
def read_graph(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo, header=None, delimiter=';')
    matriz = []
    for row in df.values:
        nova_linha = []
        for value in row:
            if pd.isnull(value) or value == 'NULL':
                nova_linha.append(None)
            else:
                nova_linha.append(float(value))
        matriz.append(nova_linha)
    
    return matriz

# Função para traduzir a matriz para um grafo ponderado e imprimir a matriz do grafo
def matriz_para_grafo(matriz):
    G = nx.Graph()
    num_linhas = len(matriz)
    num_colunas = len(matriz[0])
    
    for i in range(num_linhas):
        linha = []
        for j in range(num_colunas):
            if matriz[i][j] is not None and i != j:
                peso = matriz[i][j]
                G.add_edge(i, j, weight=peso)  # Adiciona a aresta com peso ao grafo
                linha.append(peso)
            else:
                linha.append(None)
            
    # Adiciona atributo de peso aos nós do grafo
    for u, v, dados in G.edges(data=True):
        G.nodes[u]['weight'] = dados['weight']
        G.nodes[v]['weight'] = dados['weight']
    
    return G

def clique_ILP(graph, k):
    # Define o problema de otimização com o objetivo de maximizar
    prob = pulp.LpProblem("Clique_Ponderado", pulp.LpMaximize)

    # Cria variáveis binárias x[v] para cada vértice v no grafo
    # x[v] será 1 se o vértice v fizer parte do clique, caso contrário, será 0
    x = pulp.LpVariable.dicts("x", graph.nodes, 0, 1, pulp.LpBinary)

    # Função objetivo: maximizar a soma dos pesos dos vértices que fazem parte do clique
    # O peso de cada vértice é multiplicado pela variável binária x[v]
    objetivo = 0
    for v in graph.nodes:
        objetivo += x[v] * graph.nodes[v]['weight']
    prob += objetivo

    # Restrição 1: O clique deve ter exatamente k vértices
    # A soma das variáveis x[v] deve ser igual a k
    restricao_tamanho = 0
    for v in graph.nodes:
        restricao_tamanho += x[v]
    prob += restricao_tamanho == k

    # Restrição 2: Condição de clique
    # Para todo par de vértices v1 e v2, se não há aresta entre v1 e v2,
    # então x[v1] e x[v2] não podem ser ambos 1 ao mesmo tempo
    for v1 in graph.nodes:
        for v2 in graph.nodes:
            if v1 != v2 and not graph.has_edge(v1, v2):
                prob += x[v1] + x[v2] <= 1

    # Resolve o problema de otimização
    prob.solve()

    # Obtém os resultados, ou seja, os vértices que fazem parte do clique
    # Um vértice v faz parte do clique se x[v] é igual a 1
    clique = []
    for v in graph.nodes:
        if pulp.value(x[v]) == 1:
            clique.append(v)
    
    return clique



# Função para calcular o peso total de um clique
def calcular_peso_clique(grafo, clique):
    peso_total = 0
    for u in clique:
        for v in clique:
            if u != v and grafo.has_edge(u, v):
                peso_total += grafo[u][v]['weight']
    return round(peso_total / 2, 2)  # Arredondar para 2 casas decimais e dividir por 2 para evitar contagem dupla

# Função para verificar se um clique é válido e corresponde ao tamanho k
def verificar_clique(grafo, clique, k):
    if len(clique) != k:
        return False
    for i in range(len(clique)):
        for j in range(i + 1, len(clique)):
            if not grafo.has_edge(clique[i], clique[j]):
                return False
    return True

def main():
    caminho_arquivo = 'teste_3.csv'  # Caminho do arquivo CSV
    matriz = read_graph(caminho_arquivo)
    grafo = matriz_para_grafo(matriz)

    k = 3  # Tamanho do clique desejado
    clique = clique_ILP(grafo, k)
    
    if clique:
        if verificar_clique(grafo, clique, k):
            print(f"\nClique de tamanho {k} encontrado usando ILP:", clique)
            peso_clique = calcular_peso_clique(grafo, clique)
            print(f"Peso Total do Clique: {peso_clique}")
        else:
            print(f"Nenhum clique válido de tamanho {k} encontrado.")
    else:
        print(f"Nenhum clique de tamanho {k} encontrado.")

if __name__ == "__main__":
    main()
