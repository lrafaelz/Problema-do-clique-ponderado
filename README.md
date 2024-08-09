# Problema-do-clique-ponderado

Este repositório contém a implementação de três técnicas diferentes para resolver o problema do Clique Ponderado em grafos: Programação Linear Inteira, Algoritmos Genéticos e Método Guloso. Trabalho desenvolvido em grupo para o trabalho de implementação da disciplina de Análise e Projetos de Algoritmos do curso de Engenharia de Computação da Universidade Federal do Pampa (UNIPAMPA).

**Descrição do Problema:** O problema do Clique Ponderado consiste em encontrar um conjunto de vértices em um grafo, onde cada vértice possui um peso associado, de modo que a soma dos pesos das arestas entre os vértices do clique seja maximizada. O objetivo é encontrar um clique ponderado de peso máximo.

## Técnicas de Resolução:

Programação Linear Inteira, Algoritmos Genéticos e Método Guloso.

## Estrutura do Repositório:

```
Problema-do-clique-ponderado/
│
├── src/
│   ├── clique_algorithms.py
│   ├── draw_utils.py
│   ├── graph_utils.py
│   ├── main.py
│
├── data/
│   ├── graph.csv
│   ├── ...
│
├── results/
│   ├── ...
│
├── README.md
├── requirements.txt

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
4. Execute os algoritmo `main.py` com o comando abaixo:
  
  ```sh
  python src/main.py
  ``` 
    
5. Escolha o grafo desejado de entrada, ou crie um através da interface.
6. Escolha a(s) abordagem(ns) para a resolução do problema, os resultados de cada método serão armazenados no diretório results/.

