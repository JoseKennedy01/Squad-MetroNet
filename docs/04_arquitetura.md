
# 04 — Arquitetura do MetroNet

## 1. Objetivo

Este documento apresenta a organização lógica do MetroNet, descrevendo a responsabilidade das principais partes do sistema e como elas se relacionam.

A arquitetura busca manter a estrutura do grafo separada dos algoritmos que percorrem a rede. Essa separação facilita os testes, a manutenção e a evolução do projeto.

## 2. Princípios de organização

A arquitetura segue estes princípios:

- **Separação de responsabilidades:** cada módulo deve ter uma função bem definida.
- **Modularidade:** a estrutura do grafo e os algoritmos devem ficar em módulos separados.
- **Reutilização:** os algoritmos devem utilizar a interface pública da classe `Grafo`.
- **Testabilidade:** as funções principais devem poder ser verificadas por testes automatizados.
- **Simplicidade:** a solução deve permanecer adequada ao escopo acadêmico e aos requisitos do projeto.

## 3. Organização lógica

A arquitetura está separada em responsabilidades:

1. **Interface de terminal (`app.py`):** recebe comandos, chama o serviço de roteamento e apresenta os resultados.
2. **Serviço (`src/services/roteador.py`):** seleciona BFS, DFS ou Dijkstra e padroniza o retorno como caminho e custo.
3. **Modelo (`src/models/grafo.py`):** armazena pontos e conexões e valida os dados do grafo.
4. **Algoritmos (`src/algorithms/`):** percorrem a rede segundo critérios próprios, sem depender da interface.
5. **Entrada e dados (`src/utils/` e `src/data/`):** convertem pesos digitados e oferecem leitura de CSV e geração de redes sintéticas.
6. **Testes e documentação:** verificam e descrevem os módulos e seus contratos.

O aplicativo não duplica os algoritmos: encaminha as solicitações ao serviço, que usa as funções do núcleo.

## 4. Estrutura de diretórios

A estrutura observada nesta cópia do projeto é:

```text
Squad-MetroNet/
├── app.py
├── src/
│   ├── algorithms/
│   │   ├── busca_largura.py
│   │   ├── busca_profundidade.py
│   │   └── dijkstra.py
│   ├── data/
│   │   ├── carregar_rede.py
│   │   └── gerar_rede_sintetica.py
│   ├── models/
│   │   └── grafo.py
│   ├── services/
│   │   └── roteador.py
│   └── utils/
│       └── entrada_cli.py
├── tests/
│   ├── test_app.py
│   ├── test_busca_largura.py
│   ├── test_busca_profundidade.py
│   ├── test_dados.py
│   ├── test_dijkstra.py
│   ├── test_grafo.py
│   └── test_services.py
├── reports/
│   └── profiling/
└── docs/
    ├── 01_visao_produto.md
    ├── 02_requisitos.md
    ├── 03_modelagem_matematica.md
    ├── 04_arquitetura.md
    ├── 05_algoritmos.md
    ├── 06_complexidade.md
    ├── 07_testes.md
    ├── 07_execucao.md
    └── 08_resultados.md
```

Os documentos mantêm os nomes já adotados no repositório. O guia de execução foi acrescentado como `docs/07_execucao.md`; ele convive com `docs/07_testes.md` sem renomear nem mover arquivos existentes.

## 5. Modelo do grafo

O módulo `src/models/grafo.py` contém a classe `Grafo`.

Suas principais responsabilidades são:

- Armazenar os identificadores dos pontos.
- Registrar as conexões entre pontos.
- Associar um peso a cada conexão.
- Respeitar o modo direcionado ou não direcionado.
- Validar identificadores, conexões e pesos.
- Consultar pontos, vizinhos e quantidades.

A implementação utiliza um conjunto para armazenar os pontos e um dicionário de listas de adjacência para armazenar as conexões.

Cada entrada da lista de adjacência contém uma tupla no formato:

```python
("EST02", 5)
```

O primeiro elemento representa o vizinho e o segundo representa o peso da conexão.

## 6. Módulo de algoritmos

Os algoritmos ficam separados do modelo do grafo.

### Busca em largura — BFS

Arquivo: `src/algorithms/busca_largura.py`.

A BFS explora a rede por níveis e encontra um caminho com o menor número de conexões. Ela não utiliza os pesos para escolher a rota.

### Busca em profundidade — DFS

Arquivo: `src/algorithms/busca_profundidade.py`.

A DFS explora um caminho em profundidade antes de retornar para explorar alternativas. Ela encontra um caminho válido, mas não garante o menor número de conexões nem o menor custo.

### Dijkstra

Arquivo: `src/algorithms/dijkstra.py`.

Dijkstra utiliza os pesos não negativos das conexões e uma fila de prioridade `heapq` para encontrar um caminho de menor custo. A função `dijkstra(grafo, origem, destino)` retorna `(caminho, custo_total)` ou `None` quando não há rota; pontos inexistentes geram `ValueError`.

## 7. Fluxo de execução

1. `app.py` recebe a opção do menu e os dados digitados.
2. Para cadastrar, encaminha pontos e conexões ao modelo `Grafo`; para buscar, encaminha origem, destino e algoritmo ao serviço `executar_rota`.
3. O serviço chama BFS, DFS ou Dijkstra. Os algoritmos validam os pontos e consultam vizinhos pelo modelo.
4. O serviço retorna o caminho e o custo, ou `None` quando não existe rota.
5. A interface apresenta o resultado ou uma mensagem compreensível de erro.

A rede criada pelo menu é mantida em memória durante a execução do programa. A lógica de busca permanece fora da interface.

## 8. Testes automatizados

O diretório `tests/` contém testes para o modelo, algoritmos, serviço de roteamento, interface e módulos de dados. Os casos cobrem caminhos válidos, pontos inexistentes, destinos inacessíveis, ciclos, conexões direcionadas, pesos inválidos e integração da interface.

Para executar a suíte completa:

```bash
python -m pytest -v
```

## 9. Dependências entre módulos

Os algoritmos dependem da interface pública da classe `Grafo`, principalmente dos métodos de consulta de pontos e vizinhos.

Os testes dependem das classes e funções que verificam. A documentação registra como esses módulos devem se comportar, mas não deve ser tratada como substituta dos testes executados.

Essa organização reduz o acoplamento: alterações internas na representação do grafo podem ser realizadas com menor impacto, desde que sua interface pública e seu comportamento sejam preservados.

## 10. Estado atual da arquitetura

O modelo do grafo, BFS, DFS, Dijkstra, serviço de roteamento, conversão de entradas, interface de terminal, carregador de CSV e gerador de redes sintéticas estão implementados. A suíte integrada verifica esses módulos.

O menu não oferece opção para carregar CSV ou gerar redes; essas funções ficam disponíveis em `src/data/` para uso separado. Os scripts de benchmark e profiling estão em `reports/profiling/` e pertencem à frente de análise experimental.
