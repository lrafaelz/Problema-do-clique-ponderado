# Problema-do-clique-ponderado

Este repositório contém a implementação de três técnicas diferentes para resolver o problema do Clique Ponderado em grafos: Programação Linear Inteira, Algoritmos Genéticos e Método Guloso. Trabalho desenvolvido em grupo para o trabalho de implementação da disciplina de Análise e Projetos de Algoritmos do curso de Engenharia de Computação da Universidade Federal do Pampa (UNIPAMPA).

**Descrição do Problema:** O problema do Clique Ponderado consiste em encontrar um conjunto de vértices em um grafo, onde cada vértice possui um peso associado, de modo que a soma dos pesos das arestas entre os vértices do clique seja maximizada. O objetivo é encontrar um clique ponderado de peso máximo.

## Técnicas de Resolução:

### Programação Linear Inteira:

- Descrição da técnica e sua aplicação para resolver o problema do Clique Ponderado. (INSERIR)
- Formulação do problema como um problema de Programação Linear Inteira. (INSERIR)
- Instruções de uso e execução do algoritmo. (INSERIR)

### Algoritmos Genéticos:

- Descrição da técnica e sua aplicação para resolver o problema do Clique Ponderado. (INSERIR)
- Detalhes sobre a estrutura do cromossomo e a função de fitness. (INSERIR)
- Instruções de uso e execução do algoritmo. (INSERIR)

### Método Guloso:

- Descrição da técnica e sua aplicação para resolver o problema do Clique Ponderado. (INSERIR)
- Explicação da heurística gulosa utilizada. (INSERIR)
- Instruções de uso e execução do algoritmo. (INSERIR)

## Estrutura do Repositório:

```
Problema-do-clique-ponderado/
│
├── data/
│   └── graph.csv
│
├── results/
│
├── src/
│   ├── graph_utils.py
│   ├── draw_utils.py
│   ├── clique_algorithms.py
│   └── main.py
│
├── requirements.txt
└── README.md
```

src/: Contém o código-fonte das implementações dos três métodos, da leitura do csv de entrada e o `main.py` que reune as três abordagens.
data/: Diretório para armazenar os arquivos de entrada (csv) com as informações do grafo e pesos das arestas.
results/: Local para armazenar os resultados obtidos pela execução dos algoritmos.

1. Clone o repositório em sua máquina local.

```sh
git clone git@github.com:lrafaelz/Problema-do-clique-ponderado.git
```

2. Instale as dependências listadas no `requirements.txt`, use o seguinte comando:

```sh
pip install -r requirements.txt
```

3. Insira os dados do grafo e pesos das arestas no formato adequado dentro do diretório data/.
4. Execute os algoritmo `main.py`, e escolha a abordagem para a resolução do problema
5. Os resultados de cada método serão armazenados no diretório results/.

Referências:
