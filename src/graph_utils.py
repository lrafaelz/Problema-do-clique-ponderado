import csv
import networkx as nx
import numpy as np
import pandas as pd
import string

# Função para ler um grafo ponderado a partir de uma matriz em um arquivo CSV
def read_weighted_graph_from_csv_matrix(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)[1:]  # Pula o cabeçalho da primeira coluna
        w = {}
        for i, row in enumerate(reader):
            for j, value in enumerate(row[1:]):
                if value != 'NULL' and value != '0':
                    G.add_edge(headers[i], headers[j], weight=float(value))
                    # Cria um dicionário com os pesos dos vértices
                    w[headers[i]] = w.get(headers[i], 0) + float(value)
                    w[headers[j]] = w.get(headers[j], 0) + float(value)
    return G, w

# Função que retorna todas as não-arestas de um grafo
def notE(V, E):
    nots = []
    for u in V:
        for v in V:
            if u == v: continue
            if not ((u, v) in E or (v, u) in E) and not ((u, v) in E or (v, u) in nots):
                nots.append((u, v))
    return nots

# Função para gerar rótulos de vértices de tamanho arbitrário
def generate_labels(size):
    labels = []
    for i in range(size):
        if i < 26:
            labels.append(string.ascii_lowercase[i])
        else:
            first = string.ascii_lowercase[(i // 26) - 1]
            second = string.ascii_lowercase[i % 26]
            labels.append(first + second)
    return labels

# Função para criar uma matriz aleatória e exportá-la como arquivo CSV
def create_random_matrix(size, lower_bound, upper_bound, decimal_places, same_function_block_size):
    matrix = np.zeros((size, size), dtype=object)

    for i in range(size):
        for j in range(i, size):
            if i == j:
                matrix[i, j] = 0
            elif abs(i - j) < same_function_block_size:
                matrix[i, j] = 'NULL'
                matrix[j, i] = 'NULL'
            else:
                value = round(np.random.uniform(lower_bound, upper_bound), decimal_places)
                matrix[i, j] = value
                matrix[j, i] = value

    labels = generate_labels(size)
    df = pd.DataFrame(matrix, index=labels, columns=labels)
    df.to_csv(f'data/matriz_{size}x{size}.csv', index=True, header=True)

    print("Grafo ponderado gerado e exportado com sucesso!")
    return f'data/matriz_{size}x{size}.csv'
