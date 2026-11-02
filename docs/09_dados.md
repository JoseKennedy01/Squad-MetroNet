# 09 — Dados e Geração de Redes do MetroNet

## 1. Objetivo

Este documento descreve como o MetroNet carrega redes de transporte a partir de arquivos CSV e como gera redes sintéticas para testes e experimentos de desempenho.

Os módulos de dados permitem trabalhar com entradas reproduzíveis e validar informações antes de utilizá-las nos algoritmos de grafos.

## 2. Arquivo CSV de demonstração

O arquivo `data/raw/rede_demo.csv` contém as conexões utilizadas para representar uma rede de demonstração.

O arquivo utiliza três colunas:

| Coluna | Descrição |
|---|---|
| `origem` | Identificador do primeiro ponto da conexão. |
| `destino` | Identificador do segundo ponto da conexão. |
| `peso` | Custo numérico associado à conexão. |

O cabeçalho esperado é `origem,destino,peso`, nessa ordem.

Exemplo de conteúdo:

```csv
origem,destino,peso
Estacao_A,Estacao_B,2.5
Estacao_A,Estacao_C,4.0
Estacao_B,Estacao_C,1.0
Estacao_B,Estacao_D,3.5
Estacao_C,Estacao_D,1.5
Estacao_D,Estacao_E,2.0
```

Cada linha representa uma conexão. Na rede não direcionada utilizada pelo projeto, a conexão pode ser percorrida nos dois sentidos.

Os pesos representam custos abstratos e não correspondem necessariamente a minutos, quilômetros ou valores monetários.

## 3. Carregamento e validação

O módulo `src/data/carregar_rede.py` é responsável por ler o arquivo CSV e construir a representação do grafo utilizada pelo sistema.

Durante o carregamento, são verificadas condições como:

- Existência do arquivo;
- Presença do cabeçalho esperado;
- Ordem correta das colunas;
- Existência dos campos obrigatórios;
- Ausência de campos vazios;
- Ausência de colunas adicionais;
- Validade numérica dos pesos;
- Utilização de pesos finitos;
- Ausência de conexões de um ponto para ele mesmo;
- Validações aplicadas pela classe `Grafo`.

Os identificadores dos pontos são tratados para remover espaços externos. O carregador também oferece suporte a arquivos UTF-8 com marca de ordem de bytes (BOM).

Quando uma entrada inválida é identificada, o carregador informa o problema para facilitar a correção do arquivo. Para erros associados a uma linha, a mensagem pode indicar sua posição no CSV.

Essas validações reduzem a possibilidade de que dados inconsistentes sejam utilizados pelos algoritmos de busca e roteamento.

## 4. Geração de redes sintéticas

O módulo `src/data/gerar_rede_sintetica.py` cria redes sintéticas de forma determinística.

A função `gerar_rede_sintetica(quantidade)` recebe a quantidade desejada de pontos. Os identificadores seguem o padrão `EST001`, `EST002` e assim por diante.

Para redes com pelo menos dois pontos, a geração cria conexões entre pontos consecutivos e adiciona conexões que ligam pontos separados por um identificador intermediário. Os pesos são calculados de maneira determinística.

A geração valida a quantidade informada, rejeitando valores que não representem um inteiro positivo válido.

Como a construção é determinística, chamadas repetidas com a mesma quantidade produzem a mesma estrutura de pontos, vizinhos e pesos. Isso facilita a reprodução dos testes e a comparação dos algoritmos em condições equivalentes.

## 5. Uso nos testes e experimentos

Os dados são utilizados em testes automatizados e na análise experimental dos algoritmos BFS, DFS e Dijkstra.

O arquivo CSV permite verificar o carregamento de uma rede conhecida, enquanto o gerador sintético permite variar o tamanho da entrada sem depender de dados externos.

Nos experimentos registrados pelo projeto, foram utilizadas redes de 100, 500 e 1.000 pontos, com as seguintes quantidades de conexões:

| Quantidade de pontos | Quantidade de conexões |
|---:|---:|
| 100 | 197 |
| 500 | 997 |
| 1.000 | 1.997 |

A geração determinística permite comparar os algoritmos usando as mesmas redes para cada tamanho testado.

## 6. Testes automatizados

Os testes do módulo de dados estão organizados em `tests/test_dados.py`.

Os cenários cobrem o carregamento de arquivos válidos e inválidos, a validação de pesos e campos, o tratamento de arquivos ausentes, a rejeição de conexões inválidas e o comportamento do gerador de redes sintéticas.

Também são verificados aspectos como a reprodução dos resultados, os pesos das conexões e a quantidade de conexões em redes de tamanhos conhecidos.

Os testes automatizados ajudam a verificar o comportamento esperado dos módulos, mas não substituem a análise teórica de complexidade nem os experimentos de desempenho.

## 7. Estrutura dos arquivos relacionados

```text
data/
└── raw/
    └── rede_demo.csv

src/
└── data/
    ├── __init__.py
    ├── carregar_rede.py
    └── gerar_rede_sintetica.py

tests/
└── test_dados.py
```

## 8. Considerações finais

A separação entre carregamento de dados, geração sintética e algoritmos facilita a manutenção do MetroNet e a execução de testes reproduzíveis.

As validações do CSV ajudam a identificar entradas inconsistentes, enquanto as redes sintéticas permitem analisar o comportamento dos algoritmos em diferentes tamanhos de entrada.

A documentação deve ser atualizada caso o formato do arquivo, as regras de validação ou a estratégia de geração das redes sejam modificados.