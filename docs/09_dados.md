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

A rede de demonstração possui cinco estações e seis conexões. Sua estrutura permite visualizar caminhos alternativos e comparar os resultados dos algoritmos BFS, DFS e Dijkstra.

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
- Ausência de conexões duplicadas;
- Validações aplicadas pela classe `Grafo`.

Os identificadores dos pontos são tratados para remover espaços externos. O carregador também oferece suporte a arquivos UTF-8 com marca de ordem de bytes (BOM).

Os pesos são convertidos para números do tipo `float`. A validação de valores negativos e de conexões duplicadas é centralizada na classe `Grafo`, mantendo as regras de integridade do modelo em um único local.

Em redes não direcionadas, conexões como `A,B` e `B,A` representam a mesma ligação. Por isso, a segunda ocorrência é rejeitada como duplicada.

O carregador também rejeita arquivos que possuam apenas o cabeçalho, sem nenhuma conexão registrada.

Quando uma entrada inválida é identificada, o carregador informa o problema para facilitar a correção do arquivo. Para erros associados a uma linha, a mensagem pode indicar sua posição no CSV.

Essas validações reduzem a possibilidade de que dados inconsistentes sejam utilizados pelos algoritmos de busca e roteamento.

## 4. Geração de redes sintéticas

O módulo `src/data/gerar_rede_sintetica.py` cria redes sintéticas de forma determinística.

A função `gerar_rede_sintetica(quantidade_pontos)` recebe a quantidade desejada de pontos. Os identificadores seguem o padrão `EST001`, `EST002` e assim por diante.

A geração valida a quantidade informada, rejeitando valores que não representem um inteiro positivo válido. Valores booleanos também são rejeitados, mesmo sendo tratados como inteiros pela linguagem Python.

Para redes com pelo menos dois pontos, a geração cria conexões entre pontos consecutivos e adiciona conexões que ligam pontos separados por um identificador intermediário.

### 4.1. Quantidade de conexões

A estratégia de geração utiliza duas etapas:

- Conecta cada ponto ao seguinte, criando uma cadeia principal com `V - 1` conexões.
- Adiciona conexões extras entre pontos separados por uma posição, totalizando `V - 2` conexões adicionais.

Dessa forma, para redes com pelo menos dois pontos, a quantidade total de conexões é calculada por:

\[
E=(V-1)+(V-2)
\]

Simplificando:

\[
E=2V-3
\]

Onde:

- `V` representa a quantidade de pontos;
- `E` representa a quantidade de conexões.

Para uma rede com apenas um ponto, a quantidade de conexões é zero.

Essa estratégia garante que a rede gerada seja conectada, pois a cadeia principal permite alcançar todos os pontos.

### 4.2. Determinação dos pesos

Os pesos são calculados de maneira determinística, utilizando o índice de cada conexão durante a geração.

Para as conexões entre pontos consecutivos, é utilizada a fórmula:

\[
peso=(indice \bmod 9)+1
\]

Para as conexões extras, é utilizada a fórmula:

\[
peso=((indice+3)\bmod 9)+1
\]

Os índices começam em zero, e os resultados são convertidos para `float`.

Assim, os pesos gerados variam entre `1.0` e `9.0`, sem utilização de valores aleatórios.

Como a construção é determinística, chamadas repetidas com a mesma quantidade de pontos produzem a mesma estrutura de pontos, vizinhos e pesos. Isso facilita a reprodução dos testes e a comparação dos algoritmos em condições equivalentes.

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

A rede de demonstração e as redes sintéticas possuem finalidades diferentes: a primeira facilita a apresentação e compreensão dos algoritmos, enquanto as demais permitem realizar testes com diferentes tamanhos de entrada e analisar o comportamento dos algoritmos.

## 6. Testes automatizados

Os testes do módulo de dados estão organizados em `tests/test_dados.py`.

Os cenários cobrem o carregamento de arquivos válidos e inválidos, a validação de pesos e campos, o tratamento de arquivos ausentes, a rejeição de conexões inválidas e o comportamento do gerador de redes sintéticas.

Também são verificados aspectos como:

- Arquivos com cabeçalho inválido;
- Arquivos sem conexões;
- Pesos negativos e não finitos;
- Conexões duplicadas;
- Campos ausentes ou adicionais;
- Identificadores com espaços;
- Arquivos com BOM UTF-8;
- Reprodução dos resultados da geração;
- Pesos das conexões;
- Quantidade de conexões em redes de tamanhos conhecidos.

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

A utilização de uma rede pequena para demonstração e de redes sintéticas para experimentos mantém as finalidades dos dados bem definidas.

A documentação deve ser atualizada caso o formato do arquivo, as regras de validação ou a estratégia de geração das redes sejam modificados.