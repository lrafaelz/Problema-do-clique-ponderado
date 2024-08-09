import unittest
from src.main import select_matrix, executar_greedy, executar_ilp, executar_genetico, executar_todos
from src.graph_utils import read_weighted_graph_from_csv_matrix

class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.matriz_selecionada = 'data/graph.csv'
        cls.G, cls.w = read_weighted_graph_from_csv_matrix(cls.matriz_selecionada)

    def test_selecao_matriz(self):
        # Testando a seleção de uma matriz
        matriz = select_matrix()
        self.assertTrue(matriz.endswith('.csv'))

    def test_executar_greedy(self):
        # Testando a execução do algoritmo Greedy
        executar_greedy(self.G)

    def test_executar_ilp(self):
        # Testando a execução do algoritmo ILP
        executar_ilp(self.G, self.w)

    def test_executar_genetico(self):
        # Testando a execução do algoritmo Genético
        executar_genetico(self.G)

    def test_executar_todos(self):
        # Testando a execução de todos os algoritmos
        executar_todos(self.G, self.w)

if __name__ == '__main__':
    unittest.main()
