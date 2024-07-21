import os
from graph_utils import read_weighted_graph_from_csv_matrix, create_random_matrix
from draw_utils import draw_graph
from clique_algorithms import greedy_clique_weighted, ilp_clique_weighted, genetic_clique_weighted

# Função para listar arquivos em um diretório
def list_files_in_directory(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files

# Função para selecionar ou criar uma matriz
def select_matrix():
    print("Selecione um grafo ponderado existente ou crie um novo:")
    print("0. Criar nova matriz")
    
    files = list_files_in_directory('data')
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")
    
    choice = input("Digite o número da opção desejada: ")
    
    if choice == "0":
        size = int(input("\nDigite o tamanho da matriz: "))
        lower_bound = float(input("Digite o limite inferior: "))
        upper_bound = float(input("Digite o limite superior: "))
        decimal_places = int(input("Digite o número de casas decimais: "))
        same_function_block_size = int(input("Digite o tamanho do bloco de funcionários com a mesma função\n(quantidade de NULL nas arestas): "))
        return create_random_matrix(size, lower_bound, upper_bound, decimal_places, same_function_block_size)
    else:
        index = int(choice) - 1
        if 0 <= index < len(files):
            return os.path.join('data/', files[index])
        else:
            print("\nOpção inválida, por favor selecione uma opção válida.")
            return select_matrix()

# Função para exibir o menu de algoritmos
def menu_algorithms():
    print("\nSelecione um algoritmo para executar:")
    print("1. Executar algoritmo Greedy")
    print("2. Executar algoritmo ILP")
    print("3. Executar algoritmo Genético")
    print("4. Rodar todos os algoritmos")
    print("5. Sair")

    return input("Digite o número da opção desejada: ")

# Função para criar uma matriz
def criar_matriz():
    size = int(input("Digite o tamanho da matriz: "))
    lower_bound = float(input("Digite o limite inferior: "))
    upper_bound = float(input("Digite o limite superior: "))
    decimal_places = int(input("Digite o número de casas decimais: "))
    return create_random_matrix(size, lower_bound, upper_bound, decimal_places)

# Função para executar o algoritmo Greedy
def executar_greedy(G):
    clique_greedy = greedy_clique_weighted(G)
    print("Clique encontrado (Greedy):", clique_greedy)
    draw_graph(G, clique=clique_greedy, filename='results/greedy_clique_weighted.png')

# Função para executar o algoritmo ILP
def executar_ilp(G, w):
    clique_ilp = ilp_clique_weighted(G, w)
    print("Clique encontrado (ILP):", clique_ilp)
    draw_graph(G, clique=clique_ilp, filename='results/ilp_clique_weighted.png')

# Função para executar o algoritmo Genético
def executar_genetico(G):
    clique_genetic = genetic_clique_weighted(G)
    print("Clique encontrado (Genético):", clique_genetic)
    draw_graph(G, clique=clique_genetic, filename='results/genetic_clique_weighted.png')

# Função para executar todos os algoritmos
def executar_todos(G, w):
    executar_greedy(G)
    executar_ilp(G, w)
    executar_genetico(G)

if __name__ == "__main__":
    matriz_selecionada = select_matrix()
    if matriz_selecionada:
        G, w = read_weighted_graph_from_csv_matrix(matriz_selecionada)
        while True:
            option = menu_algorithms()

            if option == "1":
                executar_greedy(G)
            elif option == "2":
                executar_ilp(G, w)
            elif option == "3":
                executar_genetico(G)
            elif option == "4":
                executar_todos(G, w)
            elif option == "5":
                break
            else:
                print("Opção inválida, por favor selecione uma opção válida.")
