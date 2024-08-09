import unittest
import os
from src.graph_utils import read_weighted_graph_from_csv_matrix
from src.draw_utils import draw_graph

class TestDrawUtils(unittest.TestCase):

    def test_draw_graph(self):
        # Testando a função de desenho de grafo
        file_path = 'data/graph.csv'
        G, w = read_weighted_graph_from_csv_matrix(file_path)
        output_path = 'results/test_graph.png'
        draw_graph(G, clique=None, filename=output_path)
        self.assertTrue(os.path.exists(output_path))

if __name__ == '__main__':
    unittest.main()
