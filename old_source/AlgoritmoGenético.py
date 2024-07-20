import numpy as np
import pandas as pd
import random

# Parâmetros do AG
TAM_POPULACAO = 100  # Tamanho da população
NUM_GERACOES = 1000  # Número de gerações
TAXA_CROSSOVER = 0.8  # Taxa de crossover
TAXA_MUTACAO = 0.01  # Taxa de mutação
TAM_TORNEIO = 5  # Tamanho do torneio para seleção

def aptidao(individuo, grafo):
    """
    Calcula a aptidão de um indivíduo.
    A aptidão é a soma dos pesos das arestas entre os vértices selecionados,
    mas penaliza se os vértices não formarem um clique.
    """
    valor_aptidao = 0  # Inicializa o valor de aptidão
    n = len(individuo)  # Obtém o número de vértices no grafo
    for i in range(n):
        if individuo[i] == 1:  # Verifica se o vértice i está selecionado
            for j in range(i + 1, n):
                if individuo[j] == 1:  # Verifica se o vértice j está selecionado
                    if not np.isnan(grafo[i][j]):  # Verifica se há uma aresta entre i e j
                        valor_aptidao += grafo[i][j]  # Adiciona o peso da aresta à aptidão
                    else:
                        return -float('inf')  # Penaliza se não há aresta (não forma clique)
    return valor_aptidao  # Retorna o valor de aptidão calculado

def inicializar_populacao(tam_populacao, num_vertices):
    """
    Inicializa a população com indivíduos aleatórios.
    """
    return [np.random.randint(2, size=num_vertices) for _ in range(tam_populacao)]

def selecao_torneio(populacao, aptidoes, k=TAM_TORNEIO):
    """
    Seleção por torneio para escolher os indivíduos para reprodução.
    """
    selecionados = []
    for _ in range(len(populacao)):
        aspirantes = random.sample(list(zip(populacao, aptidoes)), k)  # Seleciona k indivíduos aleatórios
        selecionados.append(max(aspirantes, key=lambda x: x[1])[0])  # Seleciona o indivíduo com maior aptidão
    return selecionados  # Retorna a lista de indivíduos selecionados para reprodução

def crossover(pai1, pai2):
    """
    Realiza o cruzamento entre dois pais para gerar filhos.
    """
    if random.random() < TAXA_CROSSOVER:  # Verifica se ocorre crossover com base na taxa de crossover
        ponto_corte = random.randint(1, len(pai1) - 1)  # Ponto de corte para crossover
        filho1 = np.concatenate((pai1[:ponto_corte], pai2[ponto_corte:]))  # Gera o primeiro filho
        filho2 = np.concatenate((pai2[:ponto_corte], pai1[ponto_corte:]))  # Gera o segundo filho
        return filho1, filho2  # Retorna os filhos gerados
    else:
        return pai1, pai2  # Retorna os pais sem crossover

def mutacao(individuo):
    """
    Realiza a mutação em um indivíduo.
    """
    for i in range(len(individuo)):
        if random.random() < TAXA_MUTACAO:  # Verifica se ocorre mutação com base na taxa de mutação
            individuo[i] = 1 - individuo[i]  # Realiza a mutação no gene do indivíduo

def algoritmo_genetico(grafo, tam_populacao=TAM_POPULACAO, num_geracoes=NUM_GERACOES):
    """
    Implementa o algoritmo genético para encontrar a melhor solução.
    """
    num_vertices = grafo.shape[0]  # Obtém o número de nós (vértices) no grafo
    populacao = inicializar_populacao(tam_populacao, num_vertices)  # Inicializa a população inicial
    melhor_solucao = None  # Melhor solução encontrada
    melhor_aptidao = -float('inf')  # Melhor valor de aptidão encontrado

    for geracao in range(num_geracoes):  # Loop pelas gerações
        aptidoes = [aptidao(ind, grafo) for ind in populacao]  # Calcula a aptidão de cada indivíduo

        if max(aptidoes) > melhor_aptidao:  # Verifica se encontrou uma nova melhor solução
            melhor_aptidao = max(aptidoes)  # Atualiza o melhor valor de aptidão
            melhor_solucao = populacao[np.argmax(aptidoes)]  # Atualiza a melhor solução encontrada

        selecionados = selecao_torneio(populacao, aptidoes)  # Seleciona os indivíduos para reprodução
        proxima_populacao = []

        for i in range(0, len(selecionados), 2):  # Loop para realizar o crossover
            pai1 = selecionados[i]
            if i + 1 < len(selecionados):
                pai2 = selecionados[i + 1]
                filho1, filho2 = crossover(pai1, pai2)  # Realiza o crossover entre os pais
                proxima_populacao.extend([filho1, filho2])  # Adiciona os filhos à próxima população
            else:
                proxima_populacao.append(pai1)  # Adiciona o pai sem par para a próxima população

        for individuo in proxima_populacao:
            mutacao(individuo)  # Realiza a mutação nos indivíduos da próxima população

        populacao = proxima_populacao  # Atualiza a população para a próxima geração

    return melhor_solucao, melhor_aptidao  # Retorna a melhor solução encontrada e sua aptidão

def ler_grafo(nome_arquivo):
    # Lê o grafo de um arquivo CSV
    df = pd.read_csv(nome_arquivo, delimiter=';', index_col=0, na_values=['NULL'])  # Lê o arquivo CSV
    grafo = df.to_numpy()  # Converte o DataFrame para uma matriz numpy
    return grafo  # Retorna a matriz do grafo

def main():
    # Função principal
    nome_arquivo = 'input_graph.csv'  # Nome do arquivo do grafo
    grafo = ler_grafo(nome_arquivo)  # Lê o grafo do arquivo
    melhor_solucao, melhor_aptidao = algoritmo_genetico(grafo)  # Executa o algoritmo genético

    print("Melhor solução encontrada:")  # Imprime a melhor solução
    print(melhor_solucao)  # Imprime a melhor solução encontrada
    print("Aptidão da melhor solução: {:.1f}".format(melhor_aptidao))  # Imprime a aptidão da melhor solução

if __name__ == "__main__":
    main()  # Executa a função principal 
