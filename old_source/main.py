import os
from readCSVGraph import ler_matriz_csv, matriz_para_grafo
from guloso import encontrar_cliques_gulosos, calcular_peso_clique




if __name__ == "__main__":
    caminho_arquivo = os.path.join(os.path.dirname(__file__), '..\data\grafo_.csv')
    print(f"Lendo arquivo: {caminho_arquivo}")
    matriz = ler_matriz_csv(caminho_arquivo)
    grafo = matriz_para_grafo(matriz)
    cliques = encontrar_cliques_gulosos(grafo)
    
    print("\nCliques encontrados:")
    for clique in cliques:
        peso_clique = calcular_peso_clique(grafo, clique)
        print(f"Clique: {clique}, Peso Total: {peso_clique}")