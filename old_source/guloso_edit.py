import os
import pandas as pd
import networkx as nx

# Função para ler a matriz do arquivo CSV e imprimir no console
def ler_matriz_csv(caminho_arquivo):
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
                G.add_edge(i, j, weight=matriz[i][j])
                linha.append(matriz[i][j])
            else:
                linha.append(None)
            
    return G

# Função para verificar se um conjunto de vértices forma um clique
def forma_clique(grafo, conjunto):
    for u in conjunto:
        for v in conjunto:
            if u != v and not grafo.has_edge(u, v):
                return False
    return True

# Função para encontrar todos os cliques usando abordagem gulosa
def encontrar_cliques_gulosos(grafo):
    cliques = set()
    
    # Iterar sobre cada nó no grafo
    for no in grafo.nodes:
        # Ordenar vizinhos por peso da aresta em ordem decrescente
        vizinhos = sorted(
            (vizinho for vizinho in grafo[no] if grafo[no][vizinho]['weight'] is not None),
            key=lambda x: grafo[no][x]['weight'], reverse=True
        )
        
        # Inicializar clique atual com o nó principal
        clique_atual = {no}
        
        # Iterar sobre os vizinhos ordenados
        for vizinho in vizinhos:
            pode_adicionar = True
            
            # Verificar se o vizinho pode ser adicionado ao clique atual
            for membro in clique_atual:
                if not grafo.has_edge(vizinho, membro) or grafo[vizinho][membro]['weight'] is None:
                    pode_adicionar = False
                    break
            
            # Se o vizinho está conectado a todos os membros do clique atual, adicione ao clique
            if pode_adicionar:
                clique_atual.add(vizinho)
        
        # Após verificar todos os vizinhos, garantir que o conjunto atual forma um clique
        if forma_clique(grafo, clique_atual):
            cliques.add(frozenset(clique_atual))
    
    return cliques

# Função para calcular o peso total de um clique
def calcular_peso_clique(grafo, clique):
    peso_total = 0
    for u in clique:
        for v in clique:
            if u != v and grafo.has_edge(u, v):
                peso_total += grafo[u][v]['weight']
    return round(peso_total / 2, 2)  # Arredondar para 2 casas decimais e dividir por 2 para evitar contagem dupla

if __name__ == "__main__":
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'teste_2.csv')
    matriz = ler_matriz_csv(caminho_arquivo)
    grafo = matriz_para_grafo(matriz)
    cliques = encontrar_cliques_gulosos(grafo)
    
    print("\nCliques encontrados:")
    for clique in cliques:
        peso_clique = calcular_peso_clique(grafo, clique)
        print(f"Clique: {clique}, Peso Total: {peso_clique}")
