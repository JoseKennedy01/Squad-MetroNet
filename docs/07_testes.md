# 07 — Testes do MetroNet

## 1. Objetivo

Este documento apresenta os testes automatizados utilizados para verificar a estrutura de grafo do MetroNet e os algoritmos BFS, DFS e Dijkstra.

Os testes verificam o cadastro de pontos, o registro de conexões, as validações, as consultas, a integridade da estrutura e os caminhos encontrados pelos algoritmos.

Os testes são escritos com a biblioteca `pytest`.

## 2. Como executar os testes

Na pasta raiz do projeto, execute:

```text
python -m pytest -v
```

O parâmetro `-v` apresenta o resultado individual de cada teste, facilitando a identificação de possíveis falhas.

## 3. Arquivos de teste e implementação

- `tests/test_grafo.py` verifica a estrutura e as validações do grafo.
- `tests/test_busca_largura.py` verifica a BFS.
- `tests/test_busca_profundidade.py` verifica a DFS.
- `tests/test_dijkstra.py` verifica rotas e custos do Dijkstra.
- `tests/test_services.py` verifica a integração dos algoritmos pelo roteador.
- `tests/test_app.py` verifica a interface de terminal.
- `tests/test_dados.py` verifica o carregamento de CSV e a geração de redes sintéticas.
- As implementações correspondentes ficam em `src/models/`, `src/algorithms/`, `src/services/`, `src/utils/`, `src/data/` e na raiz em `app.py`.

## 4. Cenários testados

### Estrutura do grafo

| Cenário | Objetivo |
| --- | --- |
| Grafo vazio | Verificar se o grafo começa sem pontos nem conexões |
| Ponto duplicado | Impedir o cadastro repetido do mesmo identificador |
| Identificador com espaços | Verificar a remoção de espaços extras |
| Identificadores inválidos | Rejeitar textos vazios e valores de outros tipos |
| Conexão não direcionada | Verificar o registro nos dois sentidos |
| Conexão direcionada | Verificar o registro em apenas um sentido |
| Ponto inexistente | Impedir conexões com origem ou destino não cadastrados |
| Conexão de um ponto consigo mesmo | Rejeitar uma conexão com origem igual ao destino |
| Pesos inválidos | Rejeitar valores negativos, textos, booleanos, `NaN` e infinito |
| Peso zero e decimal | Confirmar a aceitação de pesos válidos |
| Conexão duplicada | Impedir o cadastro repetido de uma conexão |
| Conexão inversa duplicada | Impedir duplicação no grafo não direcionado |
| Consulta de ponto inexistente | Rejeitar a consulta de vizinhos de um ponto não cadastrado |
| Ordenação dos pontos | Verificar o retorno dos identificadores em ordem |
| Contagem de pontos e conexões | Conferir as quantidades armazenadas |
| Cópia dos vizinhos | Garantir que alterar a lista retornada não modifique o grafo |


### Busca em profundidade

| Cenário | Objetivo |
| --- | --- |
| Caminho direto | Verificar a localização de um destino conectado diretamente à origem |
| Caminho indireto | Verificar a localização de um destino por conexões intermediárias |
| Origem igual ao destino | Retornar uma lista com apenas o ponto informado |
| Destino inacessível | Retornar `None` quando não houver caminho |
| Origem ou destino inexistente | Verificar o tratamento de pontos não cadastrados |
| Grafo direcionado | Respeitar o sentido das conexões |
| Ciclos | Verificar se a busca termina e não repete pontos no caminho retornado |
| Grafo vazio | Verificar o tratamento de origem inexistente |
| Ponto isolado | Confirmar que um ponto sem rota para o destino não produz caminho |
| Ramificações | Verificar se a busca encontra um caminho em uma rede com alternativas |
| Validade do caminho | Conferir se o caminho começa na origem, termina no destino e utiliza conexões existentes |


### Busca em largura

| Cenário | Objetivo |
| --- | --- |
| Caminho direto | Encontrar uma rota formada por uma conexão |
| Caminho indireto | Encontrar uma rota com mais de uma conexão |
| Origem igual ao destino | Retornar uma lista contendo somente esse ponto |
| Destino inacessível | Retornar `None` quando não houver rota |
| Origem ou destino inexistente | Rejeitar pontos que não estejam cadastrados |
| Grafo direcionado | Respeitar o sentido das conexões |
| Menor número de conexões | Preferir o caminho com menos arestas, mesmo quando outro caminho tem custo menor |


### Dijkstra

| Cenário | Objetivo |
| --- | --- |
| Caminho direto e indireto | Verificar a rota e a soma dos pesos |
| Alternativas de rota | Selecionar o menor custo entre caminhos disponíveis |
| Custos empatados | Aceitar qualquer rota válida com custo mínimo |
| Origem igual ao destino | Retornar o ponto e custo zero |
| Destino inacessível | Retornar `None` quando não houver rota |
| Ponto inexistente | Gerar `ValueError` para origem ou destino não cadastrado |
| Grafo direcionado | Respeitar a direção das conexões |
| Peso zero e decimais | Calcular custo com pesos permitidos, comparando decimais com tolerância |
| Validade do resultado | Conferir as conexões percorridas e a soma dos pesos |

### Aplicativo de terminal e serviço de roteamento

| Cenário | Arquivo | O que verifica |
| --- | --- | --- |
| Cadastro e busca com BFS | `tests/test_app.py` | Apresentação do caminho e do custo |
| Busca com DFS | `tests/test_app.py` | Integração da opção DFS com a interface |
| Busca de menor custo com Dijkstra | `tests/test_app.py` | Exibição da rota de menor custo e seu custo total |
| Destino sem rota e ponto inexistente | `tests/test_app.py` | Mensagens de ausência de caminho e tratamento de `ValueError` |
| Peso decimal com vírgula e peso negativo | `tests/test_app.py` | Conversão de entrada e mensagem de validação sem encerrar o menu |
| Opção de menu/algoritmo inválida, inclusive dígito Unicode não conversível | `tests/test_app.py` | Mensagem apropriada e continuidade do programa |
| Contratos dos algoritmos | `tests/test_services.py` | Disponibilidade de BFS/DFS/Dijkstra, custo, rota mínima, ausência de rota e origem igual ao destino |

### Carregamento de dados e geração de redes

| Cenário | Arquivo | O que verifica |
| --- | --- | --- |
| CSV válido, inválido ou inexistente | `tests/test_dados.py` | Cabeçalho, campos, pesos, conexões e erros de leitura |
| Geração de redes pequenas | `tests/test_dados.py` | Quantidade de pontos e conexões e conectividade |
| Geração repetida | `tests/test_dados.py` | Determinismo para a mesma entrada |

## 5. Técnicas utilizadas

### 5.1. Testes de condições

As verificações utilizam `assert` para comparar os resultados obtidos com os resultados esperados.

### 5.2. Testes de exceções

A instrução `pytest.raises(ValueError)` verifica se operações inválidas geram a exceção esperada.

### 5.3. Testes com diferentes valores

Listas, parametrização e laços são utilizados para testar vários valores sem repetir blocos de código desnecessariamente.

### 5.4. Testes de integridade

Alguns testes verificam o estado do grafo depois de uma operação, garantindo que uma tentativa inválida não altere indevidamente os pontos ou as conexões.

### 5.5. Testes de caminhos

Os testes dos algoritmos verificam caminhos retornados, o caso em que origem e destino são o mesmo ponto e situações em que não há rota. Para Dijkstra, também conferem o custo total pela soma dos pesos.

## 6. Resultado da execução

As execuções informadas ou realizadas em 14/10/2026 correspondem a snapshots diferentes do projeto. Por isso, os totais não devem ser somados como se pertencessem à mesma execução.

| Snapshot e comando | Resultado | Origem/observação |
| --- | --- | --- |
| Dijkstra: `python -m pytest -v tests/test_dijkstra.py` | 12 aprovados em 0,13 s | Informado pelo responsável pelo Dijkstra. |
| Suíte sem a extensão mais recente da DFS: `python -m pytest -v` | 38 aprovados em 0,22 s | Informado pelo responsável pelo Dijkstra. |
| DFS mais recente, sem Dijkstra: `python -m pytest -v tests/test_busca_profundidade.py` | 13 testes da DFS aprovados | Informado pelo responsável pela DFS; tempo não informado. |
| Suíte da DFS mais recente, sem Dijkstra: `python -m pytest -v` | 39 aprovados, sem falhas | Informado pelo responsável pela DFS. |
| Cópia integrada dos arquivos presentes nos dois ZIPs: `python -m pytest -v` | 50 aprovados em 0,18 s | Executado nesta revisão; o ZIP da DFS contém 12 casos, não os 13 informados depois. |

Os resultados acima pertencem às versões indicadas e são históricos. A cópia atual, que contém as versões integradas dos módulos, foi testada depois; o resultado mais recente está na seção 9. Não se somam totais de snapshots diferentes. Os tempos variam conforme o ambiente e medem a suíte, não o desempenho isolado dos algoritmos.

## 7. Limites da cobertura atual

Os testes cobrem cenários da estrutura do grafo e dos três algoritmos, incluindo entradas inválidas, ausência de caminho, ciclos, conexões direcionadas e cálculo do custo da rota.

A aprovação dos testes não garante a ausência de todos os defeitos possíveis. A cobertura deve continuar evoluindo conforme novos requisitos e algoritmos forem implementados.

Após qualquer alteração posterior, execute novamente a suíte integrada e registre a saída observada, mantendo os resultados históricos identificados por snapshot.

A análise de complexidade e o profiling devem ser documentados com base na implementação e em medições efetivamente realizadas.

## 8. Considerações finais

Os testes automatizados permitem verificar o comportamento esperado dos módulos e identificar regressões durante o desenvolvimento.

A suíte completa deve ser executada novamente após alterações relevantes no grafo, nos algoritmos ou nos testes. Os resultados registrados devem corresponder a execuções reais e identificáveis.

## 9. Atualização da suíte integrada — 02/11/2026

A execução completa mais recente nesta cópia foi realizada com:

```text
python -m pytest -q -p no:cacheprovider
```

Resultado observado na execução integrada após a revisão do aplicativo: **102 testes aprovados em 0,31 segundo**, sem falhas. O tempo difere entre execuções porque depende do ambiente. A opção `-p no:cacheprovider` desativa o plugin de cache do pytest nesta execução; ela não altera os testes executados.

A suíte inclui o teste de ciclo da BFS, o caso da DFS que demonstra que ela não garante o caminho com menos conexões, o ciclo de peso zero no Dijkstra e o teste da interface para entrada Unicode não conversível na seleção do algoritmo, além dos demais fluxos de integração e entradas inválidas. Esse resultado atualiza os registros históricos das seções anteriores; totais de snapshots diferentes não devem ser somados.

## 10. Execução integrada atualizada — 03/11/2026

A suíte integrada foi executada na pasta original do MetroNet com:

```text
python -B -m pytest -q -p no:cacheprovider
```

Resultado observado: **116 testes aprovados em 1,05 segundo**, sem falhas. A execução inclui os testes atuais do grafo, BFS, DFS, Dijkstra, serviço de roteamento, interface de terminal e módulos de dados.

A primeira tentativa no ambiente restrito aprovou 96 testes, mas 20 testes de dados não conseguiram criar diretórios temporários (`tmp_path`). A suíte foi repetida com permissão para criar esses arquivos temporários e todos os testes passaram. Essa diferença foi causada pelo ambiente da primeira execução; o resultado de 116 aprovados corresponde à execução completa bem-sucedida.

A opção `-B` evita a gravação de arquivos de bytecode e `-p no:cacheprovider` desativa o cache do pytest. Essas opções não alteram os cenários executados.

A suíte também inclui os testes recentes da interface para identificador vazio e peso não numérico, além da integração da DFS e da seleção do caminho de menor custo pelo Dijkstra.
## 11. Testes isolados após as metas 17 a 22 — 03/11/2026

Após a execução integrada registrada na seção 10, foram acrescentados sete testes aos módulos do grafo, Dijkstra e aplicação. Os resultados abaixo correspondem a execuções isoladas realizadas separadamente:

| Arquivo | Comando | Resultado observado |
| --- | --- | --- |
| `tests/test_app.py` | `python -B -m pytest -v -p no:cacheprovider tests/test_app.py` | 16 aprovados em 0,08 s |
| `tests/test_grafo.py` | `python -B -m pytest -v -p no:cacheprovider tests/test_grafo.py` | 21 aprovados em 0,08 s |
| `tests/test_dijkstra.py` | `python -B -m pytest -v -p no:cacheprovider tests/test_dijkstra.py` | 16 aprovados em 0,07 s |

Os novos cenários verificam as descrições do menu, entradas vazias, erros de Dijkstra pela interface, integridade do grafo após conexões com extremos inexistentes, uma rede determinística com 100 pontos e identificadores com espaços externos no Dijkstra.

Esses resultados são de execuções isoladas; seus tempos não devem ser somados nem comparados como desempenho dos algoritmos. A suíte completa ainda precisa ser executada novamente após esses acréscimos. O resultado integrado de 116 testes da seção 10 é anterior a eles e não representa o total atual.
## 12. Testes da interface após as metas 25 a 28 — 03/11/2026

A execução mais recente dos testes da interface foi realizada com:

```text
python -B -m pytest -v -p no:cacheprovider tests/test_app.py
```

Resultado observado: **19 testes aprovados em 0,10 segundo**, sem falhas. Os novos cenários verificam a consulta de uma rede vazia e de uma rede com conexão, a rejeição de cadastros repetidos e a rejeição de pesos `NaN`, infinito e infinito negativo. Os testes também confirmam que a interface continua funcionando após apresentar essas mensagens.

O texto do custo exibido foi ajustado para “Custo da rota encontrada”. Nos testes da interface, a mensagem é conferida para os caminhos calculados por BFS, DFS e Dijkstra.

A suíte completa ainda precisa ser executada novamente na Meta 30. O último resultado integrado de 116 testes, registrado na seção 10, antecede as alterações das metas 25 a 28 e não representa o total atual.

## 13. Suíte integrada desta revisão — 07/11/2026

A suíte foi executada na pasta raiz com:

```text
python -m pytest -q -p no:cacheprovider
```

Resultado observado: **132 testes aprovados em 0,33 segundo**, sem falhas. A primeira tentativa nesta sessão não conseguiu criar os diretórios temporários de 20 testes de dados no ambiente restrito; a repetição autorizada com acesso aos temporários executou a suíte completa. O resultado de 132 testes corresponde à execução bem-sucedida. O tempo é da suíte funcional, não dos benchmarks dos algoritmos.
