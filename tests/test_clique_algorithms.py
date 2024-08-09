import unittest
from src.graph_utils import read_weighted_graph_from_csv_matrix
from src.clique_algorithms import greedy_clique_weighted, ilp_clique_weighted, genetic_clique_weighted

class TestCliqueAlgorithms(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file_path = 'data/graph.csv'
        cls.G, cls.w = read_weighted_graph_from_csv_matrix(cls.file_path)

    def test_greedy_clique_weighted(self):
        # Testando o algoritmo Greedy
        clique = greedy_clique_weighted(self.G)
        self.assertIsNotNone(clique)
        self.assertTrue(len(clique) > 0)

    def test_ilp_clique_weighted(self):
        # Testando o algoritmo ILP
        clique = ilp_clique_weighted(self.G, self.w)
        self.assertIsNotNone(clique)
        self.assertTrue(len(clique) > 0)

    def test_genetic_clique_weighted(self):
        # Testando o algoritmo Genético
        clique = genetic_clique_weighted(self.G)
        self.assertIsNotNone(clique)
        self.assertTrue(len(clique) > 0)

if __name__ == '__main__':
    unittest.main()
