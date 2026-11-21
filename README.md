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
- Informar a quantidade de conexões da rota;
- Informar o custo total da rota;
- Identificar quando não existe caminho entre dois pontos.

---

## 🧮 Algoritmos

O núcleo implementa BFS, DFS e Dijkstra com heap como fila de prioridade. A análise teórica está em `docs/06_complexidade.md`; os experimentos disponíveis estão documentados em `docs/08_resultados.md` e organizados na pasta `experimentos/`.

---

## 🏗️ Estrutura do projeto

```text
Squad-MetroNet/
├── app.py
├── app.js
├── index.html
├── style.css
├── requirements.txt
├── src/
│   ├── models/grafo.py
│   └── algorithms/
├── tests/
│   ├── test_grafo.py
│   ├── test_busca_largura.py
│   ├── test_busca_profundidade.py
│   ├── test_dijkstra.py
│   └── test_api.py
├── data/raw/rede_demo.csv
├── experimentos/
│   ├── gerador.py
│   ├── medir.py
│   ├── grafico.py
│   └── resultado_desempenho.png
└── docs/
    └── 09_demonstracao.md
```

---

## 🛠️ Tecnologias

- **Python**
- **Flask** (API local para a demonstração web)
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

O checkout inclui scripts de geração, medição e criação de gráficos em `experimentos/`, além de `experimentos/resultado_desempenho.png`. Consulte `docs/08_resultados.md` para entender o alcance e as limitações dos dados; não interprete tempos da suíte de testes como benchmarks dos algoritmos.

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

O MetroNet inclui uma interface demonstrativa servida pelo Flask. A rede começa com dados de exemplo; estações e conexões alteradas ficam em memória enquanto o servidor estiver executando.

### Instalação

```bash
git clone <URL_DO_REPOSITORIO>

cd Squad-MetroNet

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

### Interface web

Na raiz do projeto, com o ambiente virtual ativado e as dependências instaladas, inicie o servidor. Ele atende a interface e a API no mesmo processo; mantenha essa janela aberta durante a demonstração:

```bash
python app.py
```

Abra `http://127.0.0.1:5000` no navegador. A interface consulta `/rota`, `/estacoes` e `/conexoes` no mesmo servidor Flask.

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

Na branch `nicolas-experimentos`, a suíte integrada passou com 63 testes em 20/11/2026. A interface Flask e os artefatos de experimento estão presentes. Revisão visual no navegador, integração segura das branches, apresentação da equipe e publicação da release `v1.0.0` permanecem pendentes.

- [x] Modelagem do grafo
- [x] Implementação de BFS, DFS e Dijkstra
- [x] Interface Flask e API local
- [x] Testes automatizados do núcleo e da API
- [x] Análise de complexidade e artefatos experimentais presentes
- [ ] Revisão visual da interface e ensaio final
- [ ] Integração das branches após decisão da equipe
- [ ] Apresentação e defesa individual
- [ ] Release `v1.0.0`

Execução de revisão em 20/11/2026: `python -B -m pytest -q -p no:cacheprovider` — **63 testes aprovados em 0,52 segundo**. `node --check app.js` e `git diff --check` também passaram. O tempo informado corresponde à suíte, não ao desempenho isolado dos algoritmos.

---

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos no contexto da disciplina de **Matemática Computacional**.

A licença MIT está especificada no arquivo `LICENSE`.
