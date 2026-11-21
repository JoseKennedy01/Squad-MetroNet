# 08 — Resultados do MetroNet

## 1. Objetivo e critério de registro

Este documento registra resultados de execução relatados para versões identificáveis do projeto e separa esses resultados de medições de desempenho. Um resultado de teste não é uma medição de Big-O, tempo de rota ou uso de memória.

Os dois ZIPs recebidos em 14/10/2026 representam snapshots diferentes. Um contém a versão mais recente da DFS e seus documentos, mas não inclui Dijkstra. O outro contém Dijkstra e seus testes, mas não inclui a DFS mais recente. Portanto, os resultados abaixo não devem ser somados nem apresentados como se viessem de uma única suíte integrada.

## 2. Testes funcionais informados

Os resultados foram informados pelos integrantes do projeto; os tempos indicados são os tempos apresentados pelo `pytest` naquela execução.

| Snapshot/escopo relatado | Comando | Resultado informado | Observação |
| --- | --- | --- | --- |
| Dijkstra | `python -m pytest -v tests/test_dijkstra.py` | 12 aprovados em 0,13 s | Execução específica da versão de testes de Dijkstra reforçada com empate, direção e custo decimal. |
| Dijkstra, BFS e grafo | `python -m pytest -v` | 38 aprovados em 0,22 s | Execução informada antes da inclusão do teste adicional mais recente da DFS. |
| DFS mais recente, BFS e grafo | `python -m pytest -v tests/test_busca_profundidade.py` | 13 testes da DFS aprovados | Resultado informado pelo integrante responsável pela DFS. |
| DFS mais recente, BFS e grafo | `python -m pytest -v` | 39 aprovados, sem falhas | Execução informada para o snapshot que contém a DFS atual, mas não contém o Dijkstra do outro ZIP. |
| Arquivos dos dois ZIPs recebidos integrados nesta cópia de revisão | `python -m pytest -v` | 50 aprovados em 0,25 s | Execução realizada nesta revisão. O ZIP da DFS contém 12 casos de teste da DFS, embora a atualização mais recente informe 13. |

Essas execuções demonstram que os cenários testados passaram nos respectivos snapshots. A suíte de 50 testes foi executada após combinar os arquivos de Dijkstra de um ZIP com os arquivos de DFS do outro. Ela não contém o décimo terceiro teste mencionado na atualização mais recente do integrante responsável pela DFS; portanto, a suíte final com a DFS mais atual ainda precisa ser executada.

## 3. Cobertura funcional observada

Os testes disponibilizados cobrem a estrutura e as validações do grafo, casos de BFS e DFS e, no snapshot de Dijkstra, rotas diretas/indiretas, menor custo, empate, origem igual ao destino, destino inacessível, pontos inexistentes, direção, peso zero e soma decimal aproximada.

A aprovação da suíte cobre os casos implementados, mas não prova ausência de todos os defeitos possíveis. A revisão cruzada e a execução final da suíte integrada continuam necessárias.

## 4. Análise de desempenho ainda pendente

Não há neste registro medições controladas de tempo ou memória dos algoritmos, gráficos de desempenho ou perfil produzido por `cProfile`. Essas atividades são entregáveis explícitos no PDF (p. 4–5, p. 8 e p. 10) e devem ser executadas antes de declarar concluída a análise experimental.

Os tempos de 0,13 s, 0,22 s e os tempos apresentados para outras execuções do `pytest` são tempos da suíte de testes. Eles variam por ambiente e não devem ser usados como evidência de que um algoritmo é mais rápido que outro.

## 5. Pendências para a versão final

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