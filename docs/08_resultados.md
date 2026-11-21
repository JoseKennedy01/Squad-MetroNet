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

- Obter ou confirmar a versão da DFS que contém os 13 testes informados e integrar os arquivos atuais de BFS, DFS, Dijkstra e grafo sem sobrescrever o trabalho de nenhum integrante.
- Fazer revisão cruzada do código e da documentação.
- Executar `python -m pytest -v` na cópia integrada e registrar exatamente o resultado observado.
- Preparar grafos sintéticos determinísticos de tamanhos diferentes para a análise experimental.
- Medir tempo e memória, usar `cProfile` e produzir os gráficos exigidos pelo PDF.
- Registrar dados, ambiente e método usados para que os resultados possam ser explicados e reproduzidos.

## 6. Registro anterior à correção da rede de demonstração — 20/11/2026 (superado pela seção 8)

Na branch `nicolas-experimentos`, foi executada a suíte integrada com os testes da API e interface:

| Comando | Resultado | Observação |
| --- | --- | --- |
| `python -B -m pytest -q -p no:cacheprovider` | 61 aprovados em 0,36 s | Inclui testes do modelo, algoritmos e endpoints Flask. |
| `node --check app.js` | Sem erros | Verificação de sintaxe JavaScript. |
| `git diff --check` | Sem apontamentos | Verificação do diff local. |

Antes do alinhamento da rede ao PDF, entre `EST01` e `EST09`, BFS retornava `EST01 → EST04 → EST07 → EST09`, 3 conexões e custo 14; DFS retorna `EST01 → EST03 → EST05 → EST06 → EST07 → EST09`, 5 conexões e custo 16; Dijkstra retorna `EST01 → EST04 → EST07 → EST09`, 3 conexões e custo 14. A DFS pode variar conforme a ordem dos vizinhos. Esse snapshot foi substituído pelo cenário alinhado ao PDF, registrado na seção 8.

A camada Flask recebeu validação para exigir objetos JSON nos endpoints de cadastro. `GET /rota` agora informa explicitamente `conexoes`, e a tela apresenta esse valor. A verificação HTTP automatizada passou; a conferência visual no navegador permanece pendente.

## 7. Pendências de entrega

- Revisar a compatibilidade e a integração entre as branches; `app.py` foi criado de formas diferentes na branch Flask e na branch de terminal, então a integração precisa preservar uma decisão explícita sobre as duas entradas.
- Confirmar com o grupo/docente se a interface Flask adicional ao escopo do PDF será utilizada na apresentação.
- Fazer uma execução visual de ponta a ponta no navegador e ensaiar a demonstração escolhida.
- Revisar os slides/roteiro atuais quando forem fornecidos pela equipe.
- Criar e publicar a release apenas após revisão e autorização da equipe.

## 8. Resultado final da revisão — 20/11/2026

A rede padrão foi alinhada ao cenário de demonstração descrito no PDF: nove estações, com nove conexões: `EST01–EST04` (5), `EST04–EST07` (4), `EST07–EST09` (5), `EST01–EST02` (10), `EST02–EST09` (10), `EST04–EST05` (3), `EST05–EST06` (2), `EST06–EST08` (2) e `EST08–EST09` (6). `EST03` permanece isolada para reproduzir o caso sem caminho definido no PDF; as outras oito estações estão conectadas entre si. A ordem cadastrada permite reproduzir o caminho esperado na DFS.

| Algoritmo/cenário | Caminho | Conexões | Custo |
| --- | --- | ---: | ---: |
| BFS (`EST01` a `EST09`) | `EST01 → EST02 → EST09` | 2 | 20 |
| DFS (`EST01` a `EST09`) | `EST01 → EST04 → EST07 → EST09` | 3 | 14 |
| Dijkstra (`EST01` a `EST09`) | `EST01 → EST04 → EST07 → EST09` | 3 | 14 |
| Dijkstra (`EST01` a `EST03`) | Sem caminho | — | — |

A API também foi validada com o servidor Flask em execução: `GET /`, `/style.css` e `/app.js` retornaram HTTP 200; `/estacoes` retornou nove estações; `/conexoes` retornou nove conexões; as rotas acima e a ausência de caminho foram confirmadas. O comando de testes completo passou com **63 testes em 0,52 segundo**. A conferência visual manual no navegador segue pendente.

A revisão após reconectar as estações restantes atualizou a suíte para 63 testes aprovados; a rede continua mantendo EST03 isolada para o caso de ausência de rota do PDF. A interface comparativa agora mostra conexões no lugar do número de paradas, evitando confundir os dois valores.
