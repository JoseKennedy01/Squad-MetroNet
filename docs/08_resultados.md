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
