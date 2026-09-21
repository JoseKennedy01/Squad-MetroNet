# MetroNet

> **Sistema de Roteamento Inteligente para Mobilidade Urbana**

Projeto desenvolvido pelo **Squad 1** como parte da plataforma conceitual **UrbanTech**, na disciplina de **Matemática Discreta e Algoritmos**.

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

O MetroNet deverá permitir:

- Cadastrar pontos de transporte;
- Cadastrar conexões entre pontos;
- Associar pesos às conexões;
- Consultar a rede de transporte;
- Executar **BFS**;
- Executar **DFS**;
- Executar **Dijkstra**;
- Exibir o caminho encontrado;
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

O projeto contará com testes automatizados utilizando **pytest**.

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

---

## 📊 Análise de desempenho

O projeto também realizará uma análise da eficiência dos algoritmos.

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

A documentação do projeto será mantida na pasta `docs/`, contendo informações sobre:

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

> Esta seção será atualizada conforme a implementação do projeto for concluída.

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

### Execução

```bash
python app.py
```

### Testes

```bash
pytest
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

**Em desenvolvimento**

- [ ] Modelagem do grafo
- [ ] Implementação das estruturas de dados
- [ ] Implementação de BFS
- [ ] Implementação de DFS
- [ ] Implementação de Dijkstra
- [ ] Validações e tratamento de exceções
- [ ] Testes automatizados
- [ ] Análise de complexidade
- [ ] Profiling
- [ ] Gráficos de desempenho
- [ ] Documentação
- [ ] Release `v1.0.0`

---

## 📄 Licença

Este projeto está sendo desenvolvido para fins acadêmicos no contexto da disciplina de **Matemática Discreta e Algoritmos**.

A licença do projeto será definida posteriormente.