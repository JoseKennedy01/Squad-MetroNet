# 08 — Resultados do MetroNet

## 1. Objetivo

Este documento registra os resultados dos testes funcionais, da análise experimental de desempenho e do profiling dos algoritmos BFS, DFS e Dijkstra.

Os resultados devem ser interpretados considerando a versão integrada do projeto, o tamanho das redes utilizadas e as limitações das ferramentas de medição.

## 2. Validação funcional

A suíte automatizada utiliza `pytest` para verificar o comportamento do grafo, dos algoritmos e dos módulos de dados.

Na execução mais recente, o comando `python -m pytest -v` apresentou **109 testes aprovados em 0,27 segundo, sem falhas**.

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

Os resultados foram registrados em `reports/profiling/resultados_benchmark.csv`. Os gráficos comparativos foram salvos em `reports/figures/`:

- `reports/figures/tempo_algoritmos.png`
- `reports/figures/memoria_algoritmos.png`

## 4. Resultados de tempo

A tabela apresenta as medianas de tempo de execução observadas na execução mais recente do benchmark registrada nesta revisão.

| Pontos | BFS (s) | DFS (s) | Dijkstra (s) |
|---:|---:|---:|---:|
| 100 | 0,00004730 | 0,00004040 | 0,00007690 |
| 500 | 0,00025370 | 0,00034030 | 0,00042200 |
| 1.000 | 0,00050800 | 0,00042190 | 0,00079610 |

Nas redes testadas, a DFS apresentou a menor mediana de tempo para 100 e 1.000 pontos. Na rede de 500 pontos, a BFS apresentou a menor mediana.

Dijkstra apresentou a maior mediana nas três configurações testadas.

Esses resultados descrevem somente as redes e condições avaliadas. Não demonstram que um algoritmo será sempre mais rápido que os demais, pois o desempenho depende da estrutura da rede, da ordem de exploração, da posição do destino e do ambiente de execução.

## 5. Resultados de memória

A tabela apresenta os picos de memória rastreada observados durante as medições com `tracemalloc`.

| Pontos | BFS (KiB) | DFS (KiB) | Dijkstra (KiB) |
|---:|---:|---:|---:|
| 100 | 13,74 | 13,32 | 8,06 |
| 500 | 54,15 | 52,45 | 37,60 |
| 1.000 | 76,34 | 72,26 | 77,27 |

Nas redes de 100 e 500 pontos, a BFS apresentou o maior pico de memória entre os três algoritmos. Na rede de 1.000 pontos, Dijkstra apresentou o maior pico.

A memória registrada corresponde ao pico de alocações rastreadas durante a execução do algoritmo. Ela não representa o consumo total de memória do processo Python nem inclui necessariamente todas as alocações realizadas fora do rastreamento.

Os valores observados não permitem concluir que um algoritmo sempre consumirá mais memória que os demais. O comportamento pode variar conforme o tamanho e a estrutura do grafo.

## 6. Profiling com cProfile

O profiling complementa o benchmark ao registrar informações sobre as chamadas de funções durante a execução dos algoritmos.

O script `reports/profiling/perfil_algoritmos.py` utiliza `cProfile` e `pstats` para apresentar estatísticas de execução e identificar funções relevantes para a análise de desempenho.

Os arquivos de perfil são salvos em `reports/profiling/`, com nomes associados ao algoritmo e ao tamanho da rede, como `perfil_bfs_100.prof`.

Esses arquivos permitem consultar posteriormente as estatísticas detalhadas de cada execução.

O profiling introduz uma sobrecarga na execução. Por isso, os tempos medidos com `cProfile` não devem ser comparados diretamente com as medianas obtidas pelo benchmark sem instrumentação.

## 7. Análise dos resultados

Os resultados mostram que o tempo de execução aumentou conforme o tamanho da rede cresceu nas configurações testadas. Entretanto, as diferenças observadas entre os algoritmos variaram conforme o tamanho da entrada.

A BFS e a DFS apresentaram medianas próximas em algumas configurações, enquanto Dijkstra registrou os maiores tempos nas três redes avaliadas.

Em relação à memória, BFS apresentou os maiores picos nas redes de 100 e 500 pontos, enquanto Dijkstra apresentou o maior valor na rede de 1.000 pontos.

Essas observações devem ser interpretadas em conjunto com a análise teórica de complexidade documentada em `docs/06_complexidade.md`. Medições experimentais descrevem o comportamento observado em condições específicas e não substituem os limites teóricos dos algoritmos.

## 8. Limitações

Os experimentos utilizaram redes sintéticas determinísticas e três tamanhos de entrada. Portanto, os resultados não representam necessariamente o desempenho em uma rede real de transporte urbano.

Os tempos medidos são muito pequenos e podem sofrer influência do ambiente de execução, das condições do sistema e de variações entre execuções. A utilização da mediana de 15 medições reduz a influência de valores isolados, mas não elimina todos os fatores externos.

A memória foi observada por meio das alocações rastreadas pelo Python, e não por uma ferramenta de medição de memória total do processo.

## 9. Conclusão

O benchmark e o profiling permitem observar o comportamento dos algoritmos BFS, DFS e Dijkstra em redes sintéticas de diferentes tamanhos.

Os resultados experimentais complementam a análise teórica de complexidade, auxiliando na compreensão das diferenças de tempo e memória entre as implementações.

As conclusões permanecem limitadas às redes, às medições e às condições de execução avaliadas. Experimentos adicionais com outras estruturas de grafos e tamanhos de entrada podem ampliar a análise.