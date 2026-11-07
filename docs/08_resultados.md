# 08 — Resultados do MetroNet

## 1. Objetivo

Este documento registra os resultados dos testes funcionais, da análise experimental de desempenho e do profiling dos algoritmos BFS, DFS e Dijkstra.

Os resultados devem ser interpretados considerando a versão integrada do projeto, os tamanhos das redes utilizadas e as limitações das ferramentas de medição.

## 2. Validação funcional

A suíte automatizada utiliza `pytest` para verificar o comportamento do grafo, dos algoritmos e dos módulos de dados.

Na execução integrada desta revisão, em 07/11/2026, o comando `python -m pytest -q -p no:cacheprovider` apresentou **132 testes aprovados em 0,33 segundo, sem falhas**.

Os cenários cobertos incluem:

- Cadastro e validação de pontos e conexões.
- Busca em largura (BFS) e busca em profundidade (DFS).
- Menor caminho por custo com Dijkstra.
- Origem igual ao destino.
- Caminhos diretos e indiretos.
- Destinos inacessíveis.
- Pontos inexistentes e pesos inválidos.
- Pesos zero, decimais e empates de custo.
- Carregamento de redes por CSV.
- Rejeição de arquivos inválidos e conexões duplicadas.
- Geração determinística de redes sintéticas.
- Validação dos caminhos e resultados retornados pelos algoritmos.

A aprovação dos testes confirma o comportamento dos cenários automatizados implementados, mas não garante a ausência de todos os defeitos possíveis.

## 3. Metodologia experimental

Para comparar os algoritmos, foram utilizadas redes sintéticas geradas de forma determinística pelo módulo `src/data/gerar_rede_sintetica.py`.

| Pontos (V) | Conexões (E) |
|---:|---:|
| 100 | 197 |
| 500 | 997 |
| 1.000 | 1.997 |

Os algoritmos foram executados nas mesmas redes, utilizando `EST001` como origem e o último ponto da rede como destino.

O script `reports/profiling/benchmark_algoritmos.py` realizou uma execução inicial de aquecimento e, em seguida, 15 medições de tempo para cada algoritmo e tamanho de rede. A mediana dos tempos foi utilizada como resultado representativo.

A ordem de execução dos algoritmos foi alternada entre as rodadas para reduzir possíveis efeitos de uma ordem fixa nas medições.

O pico de memória rastreada foi medido separadamente com `tracemalloc`, utilizando cinco repetições por algoritmo e tamanho de rede. Essa medida representa o pico de alocações rastreadas pelo Python durante a execução, e não o consumo total de memória do processo.

Os resultados do benchmark foram registrados em `reports/profiling/resultados_benchmark.csv`.

Os gráficos comparativos foram salvos em:

- `reports/figures/tempo_algoritmos.png`
- `reports/figures/memoria_algoritmos.png`

## 4. Resultados de tempo

A tabela apresenta as medianas de tempo de execução observadas no benchmark.

| Pontos | BFS (s) | DFS (s) | Dijkstra (s) |
|---:|---:|---:|---:|
| 100 | 0,00004880 | 0,00004200 | 0,00008030 |
| 500 | 0,00025450 | 0,00021640 | 0,00041040 |
| 1.000 | 0,00052210 | 0,00042820 | 0,00082330 |

Nas três redes testadas, a DFS apresentou a menor mediana de tempo, enquanto Dijkstra apresentou a maior mediana.

Os tempos dos três algoritmos aumentaram conforme o tamanho da rede cresceu. Na comparação entre as redes de 100 e 500 pontos, o tempo aumentou aproximadamente cinco vezes. Entre as redes de 500 e 1.000 pontos, o aumento ficou próximo de duas vezes.

Esses resultados descrevem apenas os experimentos realizados. Não significam que a DFS seja sempre mais rápida ou que os algoritmos apresentem crescimento linear em qualquer rede, pois o desempenho depende da estrutura do grafo, da ordem de exploração e da localização do destino.

## 5. Resultados de memória

A tabela apresenta as medianas dos picos de memória rastreada pelo `tracemalloc`, em KiB.

| Pontos | BFS (KiB) | DFS (KiB) | Dijkstra (KiB) |
|---:|---:|---:|---:|
| 100 | 13,74 | 13,32 | 8,06 |
| 500 | 54,15 | 52,45 | 37,60 |
| 1.000 | 76,34 | 72,26 | 77,27 |

Nas redes de 100 e 500 pontos, Dijkstra apresentou o menor pico de memória entre os três algoritmos. Na rede de 1.000 pontos, apresentou o maior.

A medição representa o pico de memória rastreada pelo `tracemalloc` durante as execuções. Não representa o consumo total de memória do processo Python.

Os resultados não permitem concluir que um algoritmo sempre utilizará menos memória que os demais, pois o consumo depende das operações realizadas e das características da rede.

## 6. Perfil de execução

O `cProfile` foi utilizado para registrar chamadas de funções e auxiliar na identificação das operações executadas pelos algoritmos.

Foram gerados nove arquivos de perfil, correspondentes às combinações de três algoritmos e três tamanhos de rede:

- BFS: 100, 500 e 1.000 pontos.
- DFS: 100, 500 e 1.000 pontos.
- Dijkstra: 100, 500 e 1.000 pontos.

Os arquivos foram armazenados em `reports/profiling/`.

Nos relatórios, aparecem chamadas relacionadas à obtenção de vizinhos e à validação de identificadores do grafo. Na DFS, também aparecem operações relacionadas à pilha. Em Dijkstra, destacam-se as operações de inserção e remoção da fila de prioridade, implementada com `heapq`.

O perfilador adiciona custo à execução. Por isso, os tempos obtidos com `cProfile` não devem ser comparados diretamente com as medianas do benchmark.

## 7. Limitações dos experimentos

Os experimentos utilizaram redes sintéticas e três tamanhos de entrada. Portanto, os resultados não representam necessariamente o desempenho em uma rede real de transporte.

A topologia utilizada é específica e não permite generalizar os resultados para todas as configurações possíveis de grafos.

Os tempos são muito pequenos e podem sofrer influência do ambiente de execução. A mediana de 15 medições reduz a influência de variações isoladas, mas não elimina todos os fatores externos.

A memória foi observada por meio de alocações rastreadas pelo Python, e não por uma ferramenta de medição da memória total do processo.

A análise experimental complementa as complexidades teóricas apresentadas em `docs/06_complexidade.md`, mas não as substitui.