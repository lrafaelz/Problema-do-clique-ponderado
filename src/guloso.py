

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


