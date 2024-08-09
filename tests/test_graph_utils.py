import unittest
import os
from src.graph_utils import read_weighted_graph_from_csv_matrix, create_random_matrix

class TestGraphUtils(unittest.TestCase):

    def test_read_weighted_graph_from_csv_matrix(self):
        # Testando a leitura de um grafo do CSV
        file_path = 'data/graph.csv'
        G, w = read_weighted_graph_from_csv_matrix(file_path)
        self.assertIsNotNone(G)
        self.assertIsNotNone(w)
        self.assertTrue(len(G.nodes) > 0)
        self.assertTrue(len(G.edges) > 0)

    def test_create_random_matrix(self):
        # Testando a criação de uma matriz aleatória
        size = 5
        lower_bound = -20.0
        upper_bound = 20.0
        decimal_places = 1
        same_function_block_size = 2
        file_path = create_random_matrix(size, lower_bound, upper_bound, decimal_places, same_function_block_size)
        self.assertTrue(os.path.exists(file_path))
        G, w = read_weighted_graph_from_csv_matrix(file_path)
        self.assertIsNotNone(G)
        self.assertIsNotNone(w)
        self.assertTrue(len(G.nodes) == size)
        self.assertTrue(len(G.edges) > 0)

if __name__ == '__main__':
    unittest.main()
