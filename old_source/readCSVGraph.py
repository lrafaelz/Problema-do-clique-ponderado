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
    
    print("Matriz lida do arquivo CSV:")
    for linha in matriz:
        print(linha)
    
    return matriz

# Função para traduzir a matriz para um grafo ponderado e imprimir a matriz do grafo
def matriz_para_grafo(matriz):
    G = nx.Graph()
    num_linhas = len(matriz)
    num_colunas = len(matriz[0])
    
    print("\nMatriz do grafo (pesos das arestas):")
    for i in range(num_linhas):
        linha = []
        for j in range(num_colunas):
            if matriz[i][j] is not None and i != j:
                G.add_edge(i, j, weight=matriz[i][j])
                linha.append(matriz[i][j])
            else:
                linha.append(None)
        print(linha)
    
    return G