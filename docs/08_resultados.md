# 08 — Resultados do MetroNet

## 1. Objetivo

Este documento registra os resultados dos testes funcionais, da análise experimental de desempenho e do profiling dos algoritmos BFS, DFS e Dijkstra.

Os resultados devem ser interpretados considerando a versão integrada do projeto, o tamanho das redes utilizadas e as limitações das ferramentas de medição.

## 2. Validação funcional

A suíte automatizada utiliza `pytest` para verificar o comportamento do grafo, dos algoritmos e dos módulos de dados.

Na última execução registrada da versão integrada, o comando `python -m pytest -v` apresentou **77 testes aprovados em 0,22 segundo, sem falhas**.

Os cenários cobertos incluem:

- Cadastro e validação de pontos e conexões.
- Busca em largura (BFS) e busca em profundidade (DFS).
- Menor caminho por custo com Dijkstra.
- Origem igual ao destino.
- Caminhos diretos, indiretos e destinos inacessíveis.
- Pontos inexistentes e pesos inválidos.
- Pesos zero, decimais e empates de custo.
- Carregamento de redes por CSV.
- Rejeição de arquivos inválidos e conexões duplicadas.
- Geração determinística de redes sintéticas.

Na validação realizada durante esta revisão, o comando `python -m pytest -v` executou **77 testes, todos aprovados, em 0,24 segundo**. Esse resultado confirma que os cenários automatizados passaram na versão testada do projeto.

A aprovação dos testes confirma o comportamento dos cenários implementados, mas não garante a ausência de todos os defeitos possíveis.

## 3. Metodologia experimental

Para comparar os algoritmos, foram utilizadas redes sintéticas geradas de forma determinística pelo módulo `src/data/gerar_rede_sintetica.py`.

| Pontos (V) | Conexões (E) |
|---:|---:|
| 100 | 197 |
| 500 | 997 |
| 1.000 | 1.997 |

Os algoritmos foram executados nas mesmas redes, utilizando `EST001` como origem e o último ponto da rede como destino.

O script `reports/profiling/benchmark_algoritmos.py` realizou um aquecimento inicial e, em seguida, 15 medições de tempo para cada algoritmo e tamanho de rede. A mediana dos tempos foi utilizada como resultado representativo.

O pico de memória rastreada foi medido separadamente com `tracemalloc`. Essa medida corresponde às alocações de memória rastreadas pelo Python durante a execução, e não ao consumo total de memória do processo.

Os resultados foram registrados em `reports/profiling/resultados_benchmark.csv`, e os gráficos foram salvos na pasta `reports/profiling/`.

## 4. Resultados de tempo

Medianas de tempo de execução observadas no benchmark:

| Pontos | BFS (s) | DFS (s) | Dijkstra (s) |
|---:|---:|---:|---:|
| 100 | 0,00005030 | 0,00004520 | 0,00007800 |
| 500 | 0,00032760 | 0,00026620 | 0,00053810 |
| 1.000 | 0,00066620 | 0,00044560 | 0,00084930 |

Nas três redes testadas, a DFS apresentou a menor mediana de tempo, enquanto Dijkstra apresentou a maior mediana.
