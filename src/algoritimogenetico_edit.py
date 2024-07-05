import sys
import os
import pandas as pd
import numpy as np
import random
import networkx as nx
from PyQt5 import QtCore, QtGui, QtWidgets


# Funções de processamento dos dados --------------------------------------------------------

def read_graph(caminho_arquivo):
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
    return matriz


def matriz_para_grafo(matriz):
    G = {}
    num_linhas = len(matriz)
    for i in range(num_linhas):
        G[i] = {}
        for j in range(num_linhas):
            if matriz[i][j] is not None and i != j:
                G[i][j] = matriz[i][j]
    return G


def is_clique(graph, nodes):
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if nodes[j] not in graph[nodes[i]]:
                return False
    return True


def fitness(individual, graph):
    # Encontrar os nós presentes no indivíduo (que estão marcados como 1)
    nodes = []
    for i, bit in enumerate(individual):
        if bit == 1:
            nodes.append(i)
    
    # Verificar se os nós formam um clique válido
    if len(nodes) < 3 or not is_clique(graph, nodes):
        # Se não formarem um clique válido, retornar um valor de aptidão muito baixo
        return -float('inf')
    
    # Calcular o peso total do clique (soma dos pesos das arestas)
    clique_weight = 0
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if j in graph[nodes[i]]:
                clique_weight += graph[nodes[i]][j]
    
    return clique_weight


def initialize_population(pop_size, num_nodes):
    population = []
    for i in range(pop_size):
        individual = np.random.randint(2, size=num_nodes)
        population.append(individual)
    return population


def tournament_selection(population, fitnesses, k=5):
    selected = []
    
    # Itera sobre todos os indivíduos na população
    for i in range(len(population)):
        # Seleciona aleatoriamente k indivíduos da população
        aspirants = random.sample(list(zip(population, fitnesses)), k)
        
        # Encontra o aspirante com a maior aptidão
        best_individual = None
        best_fitness = -float('inf')
        for ind, fit in aspirants:
            if fit > best_fitness:
                best_fitness = fit
                best_individual = ind
        
        # Adiciona o melhor indivíduo encontrado à lista de selecionados
        selected.append(best_individual)
    
    return selected


def crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        point = random.randint(1, len(parent1) - 1)
        child1 = np.concatenate((parent1[:point], parent2[point:]))
        child2 = np.concatenate((parent2[:point], parent1[point:]))
        return child1, child2
    else:
        return parent1, parent2


def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]


def genetic_algorithm(graph, pop_size, num_generations, crossover_rate=0.8, mutation_rate=0.01):
    num_nodes = len(graph)
    population = initialize_population(pop_size, num_nodes)
    best_solution = None
    best_fitness = -float('inf')

    for generation in range(num_generations):
        fitnesses = [fitness(ind, graph) for ind in population]

        if max(fitnesses) > best_fitness:
            best_fitness = max(fitnesses)
            best_solution = population[np.argmax(fitnesses)]

        selected = tournament_selection(population, fitnesses)
        next_population = []

        for i in range(0, len(selected), 2):
            parent1 = selected[i]
            if i + 1 < len(selected):
                parent2 = selected[i + 1]
                child1, child2 = crossover(parent1, parent2, crossover_rate)
                next_population.extend([child1, child2])
            else:
                next_population.append(parent1)

        for individual in next_population:
            mutate(individual, mutation_rate)

        population = next_population

    return best_solution, best_fitness


# Classe da interface PyQt5 ----------------------------------------------------------------

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(640, 480)
        self.verticalLayoutWidget = QtWidgets.QWidget(Frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 70, 181, 211))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.l_arquivo = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.l_arquivo.setObjectName("l_arquivo")
        self.verticalLayout.addWidget(self.l_arquivo)
        self.b_escolher = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.b_escolher.setObjectName("b_escolher")
        self.verticalLayout.addWidget(self.b_escolher)
        self.s_tamanho = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.s_tamanho.setObjectName("s_tamanho")
        self.verticalLayout.addWidget(self.s_tamanho)
        self.c_linear = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.c_linear.setObjectName("c_linear")
        self.verticalLayout.addWidget(self.c_linear)
        self.c_genetico = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.c_genetico.setObjectName("c_genetico")
        self.verticalLayout.addWidget(self.c_genetico)
        self.c_guloso = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.c_guloso.setObjectName("c_guloso")
        self.verticalLayout.addWidget(self.c_guloso)
        self.b_iniciar = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.b_iniciar.setObjectName("b_iniciar")
        self.verticalLayout.addWidget(self.b_iniciar)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Frame)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(239, 19, 381, 431))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.tb_matriz = QtWidgets.QTextBrowser(self.verticalLayoutWidget_2)
        self.tb_matriz.setObjectName("tb_matriz")
        self.verticalLayout_2.addWidget(self.tb_matriz)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.tb_resultado = QtWidgets.QTextBrowser(self.verticalLayoutWidget_2)
        self.tb_resultado.setObjectName("tb_resultado")
        self.verticalLayout_2.addWidget(self.tb_resultado)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

        # Conectar botão de escolher arquivo à função para abrir arquivo CSV
        self.b_escolher.clicked.connect(self.abrir_arquivo)

        # Conectar botão iniciar à função principal de processamento
        self.b_iniciar.clicked.connect(self.iniciar_processamento)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.l_arquivo.setText(_translate("Frame", "Nenhum arquivo"))
        self.b_escolher.setText(_translate("Frame", "Escolher arquivo"))
        self.c_linear.setText(_translate("Frame", "Linear"))
        self.c_genetico.setText(_translate("Frame", "Genetico"))
        self.c_guloso.setText(_translate("Frame", "Guloso"))
        self.b_iniciar.setText(_translate("Frame", "INICIAR"))
        self.label.setText(_translate("Frame", "Matriz:"))
        self.label_2.setText(_translate("Frame", "Resultado:"))

    def abrir_arquivo(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        
        if fileName:
            self.l_arquivo.setText(fileName)
            caminho_arquivo = fileName
            matriz = read_graph(caminho_arquivo)
            
            # Construir uma string formatada para exibir a matriz
            texto_matriz = ""
            for linha in matriz:
                texto_matriz += " ".join(str(valor) if valor is not None else "-" for valor in linha) + "\n"
            
            self.tb_matriz.setText(texto_matriz)

    def iniciar_processamento(self):
        caminho_arquivo = self.l_arquivo.text()
        if caminho_arquivo:
            matriz = read_graph(caminho_arquivo)
            grafo = matriz_para_grafo(matriz)
            
            # Processamento de clique linear (exemplo)
            if self.c_linear.isChecked():
                # Implementar processamento de clique linear aqui
                pass
            
            # Processamento de clique genético
            if self.c_genetico.isChecked():
                pop_size = len(grafo) * 5  # Exemplo: pode ser ajustado conforme necessário
                num_generations = len(grafo) * 10  # Exemplo: pode ser ajustado conforme necessário
                crossover_rate = 0.8
                mutation_rate = 0.01
                
                best_solution, best_fitness = genetic_algorithm(grafo, pop_size, num_generations, crossover_rate, mutation_rate)
                
                resultado = f"\nMelhor clique encontrado (genético):\n{best_solution}\nAptidão: {best_fitness}\n"
                self.tb_resultado.append(resultado)
            
            # Processamento de clique guloso
            if self.c_guloso.isChecked():
                G = nx.Graph()
                num_linhas = len(matriz)
                num_colunas = len(matriz[0])
                
                for i in range(num_linhas):
                    for j in range(num_colunas):
                        if matriz[i][j] is not None and i != j:
                            G.add_edge(i, j, weight=matriz[i][j])
                
                cliques = set(nx.find_cliques(G))
                resultado = "\nCliques encontrados (guloso):\n"
                for clique in cliques:
                    resultado += f"Clique: {clique}, Peso Total: {calcular_peso_clique(G, clique)}\n"
                
                self.tb_resultado.append(resultado)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
