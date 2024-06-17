import os
from .guloso import guloso



if __name__ == "__main__":
    caminho_arquivo = os.path.join(os.path.dirname(__file__), 'grafo_.csv')
    matriz = ler_matriz_csv(caminho_arquivo)
    grafo = matriz_para_grafo(matriz)
    cliques = encontrar_cliques_gulosos(grafo)
    
    print("\nCliques encontrados:")
    for clique in cliques:
        peso_clique = calcular_peso_clique(grafo, clique)
        print(f"Clique: {clique}, Peso Total: {peso_clique}")