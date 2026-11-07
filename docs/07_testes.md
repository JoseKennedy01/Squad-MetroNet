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

- `tests/test_grafo.py` testa a estrutura e as validações do grafo.
- `tests/test_busca_largura.py` testa a busca em largura.
- `src/models/grafo.py` contém a implementação da estrutura de grafo.
- `src/algorithms/busca_largura.py` contém a implementação da BFS.
- `tests/test_busca_profundidade.py` testa a busca em profundidade.
- `src/algorithms/busca_profundidade.py` contém a implementação da DFS.
- `tests/test_dijkstra.py` testa as rotas e os custos calculados pelo Dijkstra.
- `src/algorithms/dijkstra.py` contém a implementação do Dijkstra.


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

Os resultados acima pertencem às versões indicadas. A execução de 50 testes confirma apenas os arquivos que estavam nos dois ZIPs integrados; a suíte final com a versão da DFS que contém os 13 testes informados ainda precisa ser executada. Os tempos variam conforme o ambiente e medem a suíte, não o desempenho isolado dos algoritmos.

## 7. Limites da cobertura atual

Os testes cobrem cenários da estrutura do grafo e dos três algoritmos, incluindo entradas inválidas, ausência de caminho, ciclos, conexões direcionadas e cálculo do custo da rota.

A aprovação dos testes não garante a ausência de todos os defeitos possíveis. A cobertura deve continuar evoluindo conforme novos requisitos e algoritmos forem implementados.

Após receber a versão atualizada da DFS, deve-se executar novamente a suíte integrada e substituir ou complementar o registro acima com a saída observada.

A análise de complexidade e o profiling devem ser documentados com base na implementação e em medições efetivamente realizadas.

## 8. Considerações finais

Os testes automatizados permitem verificar o comportamento esperado dos módulos e identificar regressões durante o desenvolvimento.

A suíte completa deve ser executada novamente após alterações relevantes no grafo, nos algoritmos ou nos testes. Os resultados registrados devem corresponder a execuções reais e identificáveis.