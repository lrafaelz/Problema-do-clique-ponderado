import csv
import networkx as nx
import numpy as np
import pandas as pd
import string

def read_weighted_graph_from_csv_matrix(file_path):
    G = nx.Graph()
    # file_path = f'data/{file_path}'
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

def notE(V, E):
    nots = []
    for u in V:
        for v in V:
            if u == v: continue
            if not ((u, v) in E or (v, u) in E) and not ((u, v) in E or (v, u) in nots):
                nots.append((u, v))
    return nots

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

def create_random_matrix(size, lower_bound, upper_bound, decimal_places, same_function_block_size):
    matrix = np.zeros((size, size), dtype=object)

    for i in range(size):
        for j in range(size):
            if i == j:
                matrix[i, j] = 0
            elif abs(i - j) < same_function_block_size:
                matrix[i, j] = 'NULL'
            else:
                matrix[i, j] = round(np.random.uniform(lower_bound, upper_bound), decimal_places)

    labels = generate_labels(size)
    df = pd.DataFrame(matrix, index=labels, columns=labels)
    df.to_csv(f'data/matriz_{size}x{size}.csv', index=True, header=True)

    print("Grafo ponderado gerada e exportada com sucesso!")
    return f'data/matriz_{size}x{size}.csv'
