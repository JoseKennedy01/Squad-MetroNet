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

## 8. Análise experimental pendente

O PDF pede comparar a análise teórica com medições de tempo e memória e produzir gráficos, incluindo profiling com `cProfile` (p. 4–5, p. 8 e p. 10). Essa etapa ainda não está registrada como executada neste documento.

Para uma comparação válida, deve-se definir conjuntos de grafos determinísticos de tamanhos diferentes, executar os algoritmos em condições equivalentes, registrar as medidas e explicar as limitações dos resultados. Os tempos da suíte `pytest` informados em `docs/08_resultados.md` medem a execução dos testes e não devem ser apresentados como benchmark dos algoritmos.
