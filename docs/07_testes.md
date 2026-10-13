# 07 — Testes do MetroNet

## 1. Objetivo

Este documento apresenta os testes automatizados utilizados para verificar a estrutura de grafo do MetroNet e a busca em largura (BFS).

Os testes verificam o cadastro de pontos, o registro de conexões, as validações, as consultas, a integridade da estrutura e os caminhos encontrados pela BFS.

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

Os testes da BFS verificam os caminhos retornados, o caso em que origem e destino são o mesmo ponto e a situação em que não há rota.

## 6. Resultado da execução

Na execução informada em 13/10/2026, o comando `python -m pytest -v` apresentou:

- Testes aprovados: 26.
- Testes com falha: 0.
- Tempo informado pelo pytest: 0,07 segundo.

O tempo pode variar entre execuções e ambientes. O resultado confirma que os testes executados passaram naquela execução.

## 7. Limites da cobertura atual

A suíte verifica os casos básicos da estrutura do grafo e da BFS. Para completar os cenários de teste indicados na especificação, ainda é recomendável incluir:

- Uma rede com mais de um caminho possível entre a origem e o destino, verificando que a BFS retorna um caminho mínimo em número de conexões.
- Uma rede maior, verificando que a busca termina e encontra o resultado esperado sem depender de um exemplo pequeno.

Ainda faltam os testes específicos de DFS e Dijkstra, que serão acrescentados quando esses algoritmos forem implementados. A análise de complexidade e o profiling também serão registrados em suas etapas próprias.

## 8. Considerações finais

Os testes automatizados ajudam a identificar erros durante o desenvolvimento e a verificar se alterações preservam os comportamentos esperados.

A suíte deve ser executada novamente sempre que houver alterações relevantes na implementação do MetroNet.