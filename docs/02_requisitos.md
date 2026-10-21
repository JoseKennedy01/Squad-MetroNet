# 02 — Requisitos do MetroNet

## 1. Objetivo

Este documento organiza os requisitos da especificação do MetroNet. Os requisitos funcionais e não funcionais abaixo foram extraídos principalmente do **Anexo A**, nas páginas 5 a 7 do PDF. As referências a página correspondem à paginação do arquivo recebido.

## 2. Problema e objetivo

O MetroNet deve representar uma rede de transporte urbano como um grafo e encontrar caminhos entre pontos da cidade. Os pontos são vértices; as conexões são arestas; e cada aresta possui um peso que representa custo, tempo ou distância. O resultado de uma rota deve permitir identificar a sequência de pontos e o custo ou a distância total (PDF, Anexo A, seções A.2–A.4, p. 5).

O PDF cita roteamento em redes intermodais como contexto do problema. A implementação atual permanece no núcleo acadêmico de grafos e algoritmos, sem integração com dados ou sistemas externos.

## 3. Requisitos funcionais explícitos

Os códigos RF01–RF10 estão listados na tabela da seção A.5 do PDF (p. 6).

| Código | Requisito da especificação | Relação com a implementação atual |
| --- | --- | --- |
| RF01 | Cadastrar um ponto de transporte | `Grafo.adicionar_ponto()` cadastra identificadores de pontos. |
| RF02 | Cadastrar uma conexão entre dois pontos | `Grafo.adicionar_conexao()` registra uma conexão entre pontos já cadastrados. |
| RF03 | Associar peso à conexão | A conexão é armazenada como par `(vizinho, peso)` na lista de adjacência. |
| RF04 | Consultar a rede | `obter_pontos()`, `obter_vizinhos()` e os métodos de contagem permitem consultar a estrutura. |
| RF05 | Executar BFS | Implementado em `src/algorithms/busca_largura.py`; encontra caminho com o menor número de conexões. |
| RF06 | Executar DFS | Implementado em `src/algorithms/busca_profundidade.py`; encontra um caminho, sem garantir que seja o mais curto ou barato. |
| RF07 | Executar Dijkstra | Implementado em `src/algorithms/dijkstra.py`; retorna caminho e custo mínimo para pesos não negativos. |
| RF08 | Exibir o caminho encontrado | Os algoritmos retornam a sequência de pontos; a apresentação desse retorno em uma interface/CLI precisa ser confirmada no fluxo final do projeto. |
| RF09 | Informar o custo total | Dijkstra retorna o custo total junto com o caminho. BFS e DFS não escolhem rotas pelo peso. |
| RF10 | Informar quando não existir caminho | BFS e DFS retornam `None` quando os pontos existem, mas não há rota; Dijkstra segue o mesmo contrato. |

### 3.1. Observação sobre a saída

O PDF lista como saída rota, distância/custo, número de conexões e sequência de nós (seção A.3, p. 5). O contrato implementado para Dijkstra é `(caminho, custo_total)`. A BFS e a DFS retornam o caminho; a quantidade de conexões pode ser calculada como `len(caminho) - 1`. A especificação não define um formato único de retorno para todos os algoritmos.

## 4. Requisitos não funcionais explícitos

Os códigos RNF01–RNF06 aparecem na seção A.6 do PDF (p. 6).

| Código | Requisito | Aplicação no projeto |
| --- | --- | --- |
| RNF01 | Código modular | Modelo do grafo, algoritmos, testes e documentação ficam separados. |
| RNF02 | Testes automatizados | A suíte usa `pytest`; cada algoritmo e a estrutura do grafo possuem testes. |
| RNF03 | Documentação | Os documentos em `docs/` registram requisitos, modelo, arquitetura, algoritmos, complexidade, testes e resultados. |
| RNF04 | Execução determinística com dados de teste | Os testes constroem grafos pequenos e explícitos, com resultados esperados. |
| RNF05 | Tratamento de entradas inválidas | A estrutura valida identificadores, existência dos pontos e pesos; os algoritmos tratam pontos inexistentes com `ValueError`. |
| RNF06 | Análise de complexidade | A complexidade teórica deve ser descrita e comparada a medições práticas, conforme a implementação real. |

## 5. Requisitos de entrega e qualidade do projeto

O documento principal também determina (p. 2–4 e 8–10):

- desenvolvimento em Python, uso de Git/GitHub, revisão por pares e testes automatizados;
- demonstração e defesa técnica individual;
- análise de complexidade e profiling, com experimentos de tempo e memória e gráficos de desempenho;
- entregáveis finais como código-fonte, README, documentação, testes, evidências de execução, análise Big-O, profiling, dados sintéticos, apresentação e demonstração;
- critério de conclusão que inclui implementação, execução, docstring, teste criado e executado, consideração de caso de borda, commit e revisão por outro integrante (Definition of Done, p. 8).

As medições de desempenho, gráficos e profiling ainda devem ser registrados apenas depois de serem realmente executados. Os tempos de uma execução do pytest não substituem esse experimento.

## 6. Tecnologias e dependências

O PDF lista como obrigatórios Python, estruturas de dados, algoritmos, Git/GitHub, `pytest`, `matplotlib`, `cProfile` e README (p. 10). `heapq` é usado pela fila de prioridade do Dijkstra e pertence à biblioteca padrão do Python; não é uma dependência para instalar.

No arquivo `requirements.txt`, `pytest` e `matplotlib` são dependências externas. `cProfile` e `heapq` já fazem parte da biblioteca padrão. O uso de `matplotlib` deve acompanhar a etapa de geração dos gráficos exigidos; sua presença na lista de dependências não significa que os gráficos já foram produzidos.

## 7. Classes sugeridas e itens opcionais

O PDF sugere as classes `No`, `Aresta`, `Grafo`, `Rota` e `Roteador` (seção A.7, p. 6). Sugestões de modelagem não exigem que todas essas classes existam: a implementação atual usa `Grafo`, tuplas `(vizinho, peso)` e funções de algoritmo. A necessidade de preencher `src/models/no.py` ainda não foi demonstrada.

Type hints, logging, configuração externa, integração contínua, melhorias de visualização e otimizações aparecem como opcionais para equipes avançadas (p. 10). Não são requisitos do núcleo atual.

## 8. Limites de escopo

O PDF exclui React, Angular, Django, Flask, FastAPI, microsserviços, Docker, Kubernetes, cloud, bancos de dados complexos e machine learning avançado (p. 2 e p. 10). O foco deve continuar em modelagem matemática, estruturas de dados, algoritmos e análise de desempenho.

## 9. Cronograma e referência de prazo

O PDF organiza o trabalho acadêmico pelas semanas 8 a 15: modelagem na semana 9, BFS/DFS na semana 10, Dijkstra na semana 11, validação na semana 12, análise de desempenho na semana 13, testes na semana 14 e release/demonstração na semana 15 (p. 4 e p. 8). Esse calendário da disciplina deve ser preservado como referência do documento. Um plano de seis semanas mencionado em outra conversa é um planejamento operacional distinto e não substitui silenciosamente o cronograma do PDF.

## 10. Pontos a confirmar

- A especificação propõe estrutura de repositório com `app.py`, serviços, dados, notebooks e relatórios (p. 2–3), mas os ZIPs recebidos não incluem todos esses itens. Confirmar com o grupo quais são obrigatórios para a entrega e quais são apenas estrutura de referência.
- O PDF pede uma saída de demonstração com origem `EST01`, destino `EST09`, rota `EST01 → EST04 → EST07 → EST09` e custo total `14` (seção A.11, p. 7). Os dados que produzem esse exemplo devem estar disponíveis e ser testados antes da defesa.
- A especificação descreve peso como custo, tempo ou distância. Para Dijkstra, o peso usado precisa representar uma grandeza aditiva e não negativa; essa interpretação deve ser explicada na apresentação.
