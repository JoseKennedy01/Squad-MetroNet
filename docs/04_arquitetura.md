
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

A arquitetura pode ser compreendida pelas seguintes responsabilidades:

1. **Modelo do grafo:** armazena os pontos, as conexões e os pesos.
2. **Algoritmos:** percorrem o grafo e encontram caminhos de acordo com seus critérios.
3. **Testes automatizados:** verificam o comportamento do modelo e dos algoritmos.
4. **Documentação e análise:** registram a modelagem matemática, o funcionamento, a complexidade e os resultados experimentais.

Uma camada de aplicação poderá coordenar operações e validações adicionais se isso se tornar necessário para atender aos requisitos. Ela não deve duplicar a lógica dos algoritmos.

## 4. Estrutura de diretórios

A estrutura relevante do projeto é organizada da seguinte forma:

```text
Squad-MetroNet/
├── src/
│   ├── models/
│   │   └── grafo.py
│   └── algorithms/
│       ├── busca_largura.py
│       ├── busca_profundidade.py
│       └── dijkstra.py
├── tests/
│   ├── test_grafo.py
│   ├── test_busca_largura.py
│   ├── test_busca_profundidade.py
│   └── test_dijkstra.py
└── docs/
    ├── 01_visao_produto.md
    ├── 02_requisitos.md
    ├── 03_modelagem_matematica.md
    ├── 04_arquitetura.md
    ├── 05_algoritmos.md
    ├── 06_complexidade.md
    ├── 07_testes.md
    └── 08_resultados.md
```

A lista representa a organização prevista dos módulos. Arquivos como `dijkstra.py` e `test_dijkstra.py` devem ser confirmados no repositório antes de serem considerados existentes ou concluídos.

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

Arquivo previsto: `src/algorithms/dijkstra.py`.

Dijkstra deverá utilizar os pesos das conexões para encontrar um caminho de menor custo. Sua descrição final deverá refletir a implementação efetivamente adotada e o formato de retorno definido no projeto.

## 7. Fluxo de execução lógico

O fluxo esperado para uma operação de busca é:

1. Receber o grafo, a origem e o destino.
2. Validar se os pontos existem.
3. Consultar as conexões por meio dos métodos públicos de `Grafo`.
4. Executar o algoritmo correspondente.
5. Reconstruir o caminho quando houver rota.
6. Retornar o resultado ou indicar que não existe caminho.
7. Permitir que a camada responsável pela apresentação exiba o resultado, caso exista uma interface de execução.

A lógica de busca não deve ser duplicada na interface.

## 8. Testes automatizados

O diretório `tests/` contém os testes do projeto.

Os testes verificam tanto o comportamento da classe `Grafo` quanto os resultados dos algoritmos. Eles devem cobrir caminhos válidos, pontos inexistentes, destinos inacessíveis, ciclos, conexões direcionadas e outras situações relevantes.

O comando utilizado para executar a suíte é:

```bash
python -m pytest -v
```

## 9. Dependências entre módulos

Os algoritmos dependem da interface pública da classe `Grafo`, principalmente dos métodos de consulta de pontos e vizinhos.

Os testes dependem das classes e funções que verificam. A documentação registra como esses módulos devem se comportar, mas não deve ser tratada como substituta dos testes executados.

Essa organização reduz o acoplamento: alterações internas na representação do grafo podem ser realizadas com menor impacto, desde que sua interface pública e seu comportamento sejam preservados.

## 10. Estado e evolução da arquitetura

A classe `Grafo`, a BFS e a DFS fazem parte da implementação já relatada como existente no projeto.

A implementação do Dijkstra, uma eventual camada de aplicação e outras partes da arquitetura devem ser registradas como concluídas somente após a verificação dos arquivos, dos testes e dos requisitos correspondentes.

A arquitetura deverá ser revisada quando os algoritmos restantes forem integrados e quando a implementação final permitir confirmar o fluxo completo de execução.
