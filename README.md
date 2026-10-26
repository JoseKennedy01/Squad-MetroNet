# MetroNet

> **Sistema de Roteamento Inteligente para Mobilidade Urbana**

Projeto desenvolvido pelo **Squad 1** como parte da plataforma conceitual **UrbanTech**, na disciplina de **Matemática Computacional**.

O MetroNet tem como objetivo representar uma rede de transporte urbano utilizando **grafos** e aplicar algoritmos para encontrar caminhos eficientes entre diferentes pontos da cidade.

---

## 📌 Sobre o projeto

O sistema representa uma rede de transporte como um **grafo ponderado**, onde:

- **Vértices (V)** representam estações ou pontos de transporte;
- **Arestas (E)** representam conexões entre os pontos;
- **Pesos** representam custo, tempo ou distância.

A partir dessa representação, o sistema permite consultar a rede e executar algoritmos de busca e roteamento.

---

## 🎯 Objetivos

O núcleo implementado permite:

- Cadastrar pontos de transporte;
- Cadastrar conexões entre pontos;
- Associar pesos às conexões;
- Consultar a rede de transporte;
- Executar **BFS**;
- Executar **DFS**;
- Executar **Dijkstra**;
- Retornar a sequência do caminho encontrado;
- Informar o custo total da rota;
- Identificar quando não existe caminho entre dois pontos.

---

## 🧮 Algoritmos

O núcleo do projeto utiliza algoritmos e estruturas de dados relacionados a grafos:

- **BFS (Breadth-First Search)** — busca em largura;
- **DFS (Depth-First Search)** — busca em profundidade;
- **Dijkstra** — busca pelo caminho de menor custo;
- **Heap** — utilizada como fila de prioridade.

Também serão analisadas as complexidades dos algoritmos e seu comportamento conforme o tamanho da rede aumenta.

---

## 🏗️ Estrutura do projeto

> A árvore abaixo é a estrutura de referência do projeto. A cópia integrada revisada ainda não contém todos os diretórios e arquivos listados, como `app.py`; confira o conteúdo efetivo da pasta antes de tentar executá-los.

```text
urban-tech-metronet/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── docs/
│   ├── 01_visao_produto.md
│   ├── 02_requisitos.md
│   ├── 03_modelagem_matematica.md
│   ├── 04_arquitetura.md
│   ├── 05_algoritmos.md
│   ├── 06_complexidade.md
│   ├── 07_testes.md
│   └── 08_resultados.md
│
├── src/
│   ├── __init__.py
│   ├── models/
│   ├── data/
│   ├── algorithms/
│   ├── services/
│   └── utils/
│
├── tests/
│   ├── test_models.py
│   ├── test_algorithms.py
│   ├── test_services.py
│   └── test_edge_cases.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── exploration.ipynb
│
├── reports/
│   ├── complexity/
│   ├── profiling/
│   └── figures/
│
└── app.py
```

---

## 🛠️ Tecnologias

- **Python**
- **pytest**
- **matplotlib**
- **cProfile**
- **Git**
- **GitHub**

### Tecnologias opcionais

Dependendo da evolução do projeto, poderão ser utilizados:

- Type hints;
- Logging;
- Configurações externas;
- Integração contínua (CI);
- Melhorias de visualização;
- Otimizações adicionais.

---

## 🧪 Testes

O projeto possui testes automatizados utilizando **pytest**.

Entre os cenários previstos estão:

- Grafo vazio;
- Um único nó;
- Origem igual ao destino;
- Caminho direto;
- Caminho indireto;
- Múltiplos caminhos;
- Destino inacessível;
- Peso inválido;
- Nó inexistente;
- Redes maiores.
- Custo mínimo, empates de custo e pesos decimais no Dijkstra.

---

## 📊 Análise de desempenho

O projeto documenta a complexidade teórica dos algoritmos. A análise experimental de eficiência ainda precisa ser realizada.

Serão considerados:

- Complexidade teórica;
- Tempo de execução;
- Consumo de memória;
- Profiling;
- Gráficos de desempenho;
- Comparação entre comportamento teórico e experimental.

---

## 🌿 Git e GitHub

O desenvolvimento seguirá uma estratégia baseada em branches:

```text
main
│
├── feature/modelagem
├── feature/algoritmo
├── feature/testes
└── feature/interface
```

Fluxo de desenvolvimento:

```text
Criar branch
     ↓
Desenvolver
     ↓
Testar
     ↓
Commit
     ↓
Pull Request
     ↓
Code Review
     ↓
Merge
```

---

## 📚 Documentação

A documentação do projeto está organizada na pasta `docs/` e contém informações sobre:

- Visão do produto;
- Requisitos;
- Modelagem matemática;
- Arquitetura;
- Algoritmos;
- Complexidade;
- Testes;
- Resultados.

---

## 🚀 Execução

> O repositório integrado revisado não contém `app.py` nem outra interface de execução. A demonstração dos algoritmos por uma interface ainda precisa ser definida pela equipe.

### Instalação

```bash
git clone <URL_DO_REPOSITORIO>

cd urban-tech-metronet

python -m venv venv
```

Ativação do ambiente virtual no Windows:

```bash
venv\Scripts\activate
```

Instalação das dependências:

```bash
pip install -r requirements.txt
```

### Testes

```bash
python -m pytest -v
```

---

## 👥 Equipe

**Squad 1 — MetroNet**

| Integrante         | Função |
|---|---|
| José Kennedy       | Código |
| Mateus Souza       | Código |
| Nicolas Gabriel    | Código |
| Erysson Roberto    | Código |
| Marcus Vinícius    | Artigo |
| Miguel Gonçalves   | Artigo |
| Leonardo Junior    | Artigo |
| David Dias         | Artigo |

---

## 📌 Status do projeto

**Núcleo de grafo e algoritmos implementado; validação final e análise experimental pendentes.**

- [x] Modelagem do grafo
- [x] Implementação das estruturas de dados
- [x] Implementação de BFS
- [x] Implementação de DFS
- [x] Implementação de Dijkstra
- [x] Validações e tratamento de exceções
- [x] Testes automatizados criados e executados na cópia integrada de revisão
- [x] Análise de complexidade teórica
- [ ] Profiling
- [ ] Gráficos de desempenho
- [x] Documentação do produto, requisitos, modelagem, arquitetura, algoritmos, complexidade, testes e resultados
- [ ] Release `v1.0.0`

Na cópia integrada formada pelos ZIPs recebidos, a última execução apresentou **50 testes aprovados em 0,18 segundo**. Esse snapshot contém 12 testes da DFS; o integrante responsável informou depois uma versão com 13. A suíte final precisa ser executada novamente com a DFS atualizada antes do commit.

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos no contexto da disciplina de **Matemática Computacional**.

A licença MIT está especificada no arquivo `LICENSE`.

---

## Atualização complementar — resultados reunidos da equipe 

Esta seção complementa o registro anterior sem substituir seu conteúdo. Os resultados abaixo vêm de execuções e snapshots diferentes; por isso, não devem ser somados nem tratados como uma única execução.

### Testes automatizados

Na cópia do repositório conferida em 26/10/2026, a suíte completa apresentou **67 testes aprovados em 0,62 segundo**. O pytest exibiu um aviso por não conseguir gravar o cache em `.pytest_cache`, mas não houve falha de teste.

A suíte coletada nessa cópia se distribui assim:

| Área | Casos coletados |
|---|---:|
| Aplicação de terminal | 4 |
| BFS | 10 |
| DFS | 13 |
| Dijkstra | 12 |
| Grafo e validações | 16 |
| Serviços de roteamento | 12 |
| **Total** | **67** |

O integrante responsável pela DFS informou **13 testes específicos da DFS aprovados**. O integrante responsável pelo Dijkstra informou **12 testes específicos do Dijkstra aprovados em 0,13 segundo**. Esses testes já estão incluídos na contagem da suíte integrada de 67; não devem ser somados novamente.

Também foi informado um resultado de **77 testes aprovados em 0,24 segundo** para uma versão mais recente. Esse número não foi reproduzido na cópia conferida nesta data, que coletou 67 casos. Ele fica registrado como resultado de outro snapshot e precisa ser associado à versão correspondente antes de ser apresentado como resultado da suíte atual.

### Experimentos de desempenho informados pela equipe

A equipe informou a geração de redes determinísticas e conectadas com estas quantidades:

| Pontos | Conexões |
|---:|---:|
| 100 | 197 |
| 500 | 997 |
| 1.000 | 1.997 |

Também foram informadas 15 medições de tempo por algoritmo e tamanho de rede, após aquecimento, resumidas pela mediana:

| Pontos | BFS (s) | DFS (s) | Dijkstra (s) |
|---:|---:|---:|---:|
| 100 | 0,00005030 | 0,00004520 | 0,00007800 |
| 500 | 0,00032760 | 0,00026620 | 0,00053810 |
| 1.000 | 0,00066620 | 0,00044560 | 0,00084930 |

Nessas redes e condições relatadas, a DFS apresentou a menor mediana e Dijkstra a maior. Essa observação se limita aos casos medidos e não garante a mesma ordem para outras redes. A equipe também informou a medição separada do pico de memória com `tracemalloc`, que acompanha alocações rastreadas pelo Python e não equivale ao uso total de memória do processo.

**Estado dos artefatos nesta cópia:** não foram encontrados os módulos e resultados citados pela equipe — `src/data/gerar_rede_sintetica.py`, `reports/profiling/benchmark_algoritmos.py`, `reports/profiling/perfil_algoritmos.py`, `reports/profiling/resultados_benchmark.csv`, os gráficos ou os arquivos `.prof`. Portanto, os comandos para reproduzir os experimentos e os valores de memória ainda não estão confirmados aqui. A equipe informou que o profiling usa `cProfile`/`pstats` e gera perfis para três algoritmos em três tamanhos; os tempos do perfilador incluem sobrecarga e não são diretamente comparáveis às medianas do benchmark.
