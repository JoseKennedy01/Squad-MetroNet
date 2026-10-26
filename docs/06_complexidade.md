# 06 — Análise de Complexidade do MetroNet

## 1. Objetivo

Este documento descreve a complexidade assintótica das operações principais do grafo e dos algoritmos conforme estão implementados. A análise teórica é separada dos resultados experimentais: os testes funcionais não substituem o profiling de tempo e memória exigido pelo PDF.

## 2. Notação e representação

- `V`: número de pontos (vértices) do grafo.
- `E`: número de conexões (arestas) cadastradas. Em grafo não direcionado, cada conexão aparece nas listas de adjacência dos dois extremos.
- `grafo.adjacencias`: dicionário que associa cada ponto a uma lista de pares `(vizinho, peso)`.

O grafo usa lista de adjacência, não matriz de adjacência. Por isso, percorrer todos os vizinhos de um ponto custa proporcionalmente ao seu grau; percorrer a rede toda custa `O(V + E)`.

## 3. Operações da estrutura de grafo

| Operação | Complexidade esperada | Justificativa |
| --- | --- | --- |
| Cadastrar ponto | `O(1)` médio | Inserção em `set` e criação de entrada em dicionário, desconsiderando colisões raras. |
| Consultar se ponto existe | `O(1)` médio | Consulta em `set`. |
| Obter pontos ordenados | `O(V log V)` | A coleção precisa ser ordenada antes de ser retornada. |
| Obter vizinhos | `O(d(v))` | A lista dos vizinhos é copiada; `d(v)` é o grau do ponto. |
| Cadastrar conexão | `O(d(u))` | A implementação percorre os vizinhos da origem para verificar duplicidade. |
| Contar pontos | `O(1)` | Usa o tamanho do conjunto. |
| Contar conexões | `O(V + E)` | Percorre as listas de adjacência para somar seus tamanhos. |

O espaço da representação é `O(V + E)` para grafo direcionado. Em grafo não direcionado, cada aresta ocupa duas entradas de adjacência, mantendo a mesma ordem assintótica.

## 4. Busca em largura — BFS

**Implementação:** `src/algorithms/busca_largura.py`.

| Medida | Complexidade no pior caso |
| --- | --- |
| Tempo | `O(V + E)` |
| Espaço adicional | `O(V)` |

A BFS marca cada ponto descoberto uma vez e examina as listas de vizinhos dos pontos alcançados. A fila é implementada por lista com índice crescente, evitando remover o primeiro elemento da lista a cada passo. O conjunto de visitados e o dicionário de predecessores armazenam até `V` pontos.

A BFS minimiza o número de conexões, não a soma dos pesos.

## 5. Busca em profundidade — DFS

**Implementação:** `src/algorithms/busca_profundidade.py`.

| Medida | Complexidade no pior caso |
| --- | --- |
| Tempo | `O(V + E)` |
| Espaço adicional | `O(V)` |

A DFS usa uma pilha, um conjunto de visitados e um dicionário de predecessores. Cada ponto é marcado uma vez e cada conexão dos pontos alcançados é examinada no máximo uma quantidade constante de vezes. A DFS encontra um caminho válido, mas não garante o menor número de conexões nem o menor custo.

## 6. Dijkstra

**Implementação:** `src/algorithms/dijkstra.py`.

O algoritmo usa uma fila de prioridade binária fornecida pelo módulo padrão `heapq`. Quando uma distância melhora, uma nova entrada é colocada na heap; entradas antigas são ignoradas quando removidas. Essa estratégia evita a necessidade de uma operação de diminuição de prioridade.

| Medida | Complexidade no pior caso |
| --- | --- |
| Tempo | `O((V + E) log V)` para o grafo simples usado pelo projeto |
| Espaço auxiliar | `O(V + E)` |

Cada ponto pode ser processado e cada entrada de adjacência examinada. Cada melhoria de distância pode inserir uma entrada na heap, portanto podem existir `O(E)` entradas temporárias. Como a classe `Grafo` rejeita conexões duplicadas e laços, o grafo é simples e `E = O(V²)`; assim, o fator `log E` das operações da heap fica em `O(log V)`. O espaço auxiliar considera a possibilidade de entradas repetidas na heap. Distâncias e predecessores ocupam `O(V)`.

Dijkstra requer pesos não negativos. A classe `Grafo` rejeita pesos negativos e aceita peso zero, satisfazendo essa condição. O algoritmo minimiza o custo acumulado, que não é necessariamente o caminho com menor número de conexões.

## 7. Comparação

| Algoritmo | Critério da rota | Tempo | Espaço auxiliar |
| --- | --- | --- | --- |
| BFS | Menor número de conexões | `O(V + E)` | `O(V)` |
| DFS | Primeiro caminho encontrado segundo a ordem de exploração | `O(V + E)` | `O(V)` |
| Dijkstra | Menor soma dos pesos não negativos | `O((V + E) log V)` | `O(V + E)` |

As complexidades são limites teóricos para a representação e implementação atuais. Não são medições de velocidade.


## 8. Análise experimental

### 8.1. Metodologia

A análise experimental foi realizada com redes sintéticas geradas de forma determinística, permitindo repetir os experimentos com os mesmos dados.

Foram utilizadas três redes:

| Quantidade de pontos (V) | Quantidade de conexões (E) |
|---:|---:|
| 100 | 197 |
| 500 | 997 |
| 1.000 | 1.997 |

Os algoritmos BFS, DFS e Dijkstra foram executados com a mesma rede, origem e destino para cada tamanho testado.

Para medir o tempo, cada algoritmo foi executado 15 vezes por tamanho de rede. O resultado registrado corresponde à mediana dos tempos obtidos. Uma execução inicial de aquecimento foi realizada antes das medições.

O pico de memória rastreada foi medido separadamente com `tracemalloc`, evitando incluir o custo do rastreamento nas medições de tempo.

O script `reports/profiling/benchmark_algoritmos.py` gera os resultados em CSV e os gráficos comparativos. O script `reports/profiling/perfil_algoritmos.py` complementa a análise com informações de perfil de execução obtidas por `cProfile`.

### 8.2. Resultados de tempo

| Pontos | BFS (s) | DFS (s) | Dijkstra (s) |
|---:|---:|---:|---:|
| 100 | 0,00005030 | 0,00004520 | 0,00007800 |
| 500 | 0,00032760 | 0,00026620 | 0,00053810 |
| 1.000 | 0,00066620 | 0,00044560 | 0,00084930 |

Nas redes testadas, a DFS apresentou a menor mediana de tempo nas três configurações. Os tempos dos três algoritmos aumentaram conforme o tamanho da rede cresceu.

Esse resultado descreve apenas os experimentos realizados. Não significa que a DFS seja sempre mais rápida, pois o desempenho depende da estrutura do grafo, da ordem de exploração e da localização do destino.

### 8.3. Resultados de memória

| Pontos | BFS (KiB) | DFS (KiB) | Dijkstra (KiB) |
|---:|---:|---:|---:|
| 100 | 13,74 | 13,32 | 8,06 |
| 500 | 54,15 | 52,45 | 37,58 |
| 1.000 | 76,34 | 72,26 | 77,24 |

A medição representa o pico de memória rastreada pelo `tracemalloc` durante uma execução do algoritmo. Não representa o consumo total de memória do processo Python.

Na rede de 1.000 pontos, Dijkstra apresentou o maior pico de memória entre os três algoritmos. Entretanto, os resultados não permitem concluir que esse comportamento ocorrerá em todas as redes.

### 8.4. Perfil de execução

O `cProfile` foi utilizado para registrar chamadas de funções e auxiliar na identificação das operações executadas pelos algoritmos.

Nos relatórios, aparecem chamadas relacionadas à busca de vizinhos e à validação de identificadores do grafo. Em Dijkstra, também aparecem operações de inserção e remoção da fila de prioridade, implementada com `heapq`.

O perfilador adiciona custo à execução. Por isso, os tempos obtidos com `cProfile` não devem ser comparados diretamente com as medianas do benchmark.

### 8.5. Limitações

Os experimentos utilizaram redes sintéticas e três tamanhos de entrada. Portanto, os resultados não representam necessariamente o desempenho em uma rede real de transporte.

Os tempos são muito pequenos e podem sofrer influência do ambiente de execução. A mediana de 15 medições reduz a influência de variações isoladas, mas não elimina todos os fatores externos.

A memória foi observada por meio de alocações rastreadas pelo Python, e não por uma ferramenta de medição de memória total do processo.

A análise experimental complementa as complexidades teóricas apresentadas nas seções anteriores, mas não as substitui.
