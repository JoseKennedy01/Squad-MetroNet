# 03 — Modelagem Matemática do MetroNet

## 1. Objetivo

Este documento apresenta a modelagem matemática utilizada pelo
MetroNet para representar uma rede de transporte e permitir a análise
de caminhos entre diferentes pontos.

A modelagem utiliza a teoria dos grafos, conjuntos, conexões e pesos.
Ela serve como base para a implementação dos algoritmos de busca e
roteamento exigidos pelo projeto.

## 2. Representação do grafo

A rede de transporte é representada por um grafo:

G = (V, E)

Onde:

- G representa o grafo que modela a rede.
- V representa o conjunto de vértices (pontos de transporte).
- E representa o conjunto de arestas (conexões entre os pontos).

Cada ponto cadastrado pertence ao conjunto V. As conexões entre os
pontos são representadas pelas arestas pertencentes a E.

## 3. Conjunto de vértices

O conjunto V armazena os pontos de transporte da rede.

Exemplo:

V = {EST01, EST02, EST03, EST04}

Nesse exemplo, existem quatro pontos cadastrados.

No código Python, o conjunto é representado pela estrutura set:

    self.pontos = set()

O uso de um conjunto evita que o mesmo identificador seja armazenado
mais de uma vez.

## 4. Conjunto de arestas

O conjunto E representa as conexões existentes entre os pontos.

Para o exemplo anterior, podemos considerar:

E = {
    (EST01, EST02),
    (EST02, EST03),
    (EST03, EST04)
}

Cada par representa uma conexão entre dois pontos.

Na implementação do MetroNet, as conexões também possuem pesos,
que são explicados na próxima seção.

Em um grafo não direcionado, uma conexão entre dois pontos permite
o percurso nos dois sentidos. Em um grafo direcionado, o sentido
da conexão é respeitado.

## 5. Pesos das conexões

Cada conexão possui um peso numérico não negativo.

O peso pode representar, conforme os dados utilizados pelo projeto,
uma medida como distância, tempo ou custo de deslocamento.

Exemplo:

- EST01 — EST02: peso 5
- EST02 — EST03: peso 3
- EST03 — EST04: peso 7

O peso representa o valor associado à conexão, e não a identificação
do ponto.

No código, cada conexão é armazenada em uma tupla:

    (vizinho, peso)

Por exemplo:

    ("EST02", 5)

Essa tupla indica uma conexão para EST02 com peso 5.

A implementação aceita pesos inteiros ou decimais, desde que sejam
válidos e não negativos.

## 6. Formalização do grafo ponderado

Como as conexões possuem pesos, o modelo pode ser escrito como:

G = (V, E, w)

Onde:

- V é o conjunto de pontos de transporte.
- E é o conjunto de conexões entre esses pontos.
- w é uma função que associa um custo numérico a cada conexão.

Para a configuração não direcionada padrão do MetroNet, uma conexão
entre u e v permite percorrer o trajeto nos dois sentidos. Assim,
se {u, v} pertence a E, a lista de adjacência registra v como vizinho
de u e u como vizinho de v.

O peso de cada conexão é definido por:

w: E → R≥0

Isso significa que cada conexão recebe um custo real não negativo.
A implementação também rejeita valores não finitos e aceita peso zero.

## 7. Representação por lista de adjacência

O MetroNet utiliza uma representação por lista de adjacência.

Nessa representação, cada ponto possui uma lista com suas conexões
diretas, incluindo o identificador do vizinho e o peso da conexão.

Exemplo simplificado:

    {
        "EST01": [("EST02", 5)],
        "EST02": [("EST01", 5), ("EST03", 3)],
        "EST03": [("EST02", 3)]
    }

Esse exemplo representa um grafo não direcionado com três pontos
e duas conexões.

No código Python, essa estrutura é armazenada em um dicionário:

    self.adjacencias = {}

Cada chave representa um ponto, e seu valor é uma lista de tuplas
com os vizinhos e os respectivos pesos.

## Caminhos e custo total

Um caminho entre dois pontos é uma sequência:

P = (v₀, v₁, ..., vₖ)

em que cada par consecutivo da sequência está conectado por uma aresta.
O custo total do caminho é a soma dos pesos dessas conexões:

C(P) = w(v₀, v₁) + w(v₁, v₂) + ... + w(vₖ₋₁, vₖ)

A BFS procura um caminho com o menor número de conexões, sem comparar
os pesos. O Dijkstra procura um caminho cujo custo total seja mínimo.
Como o MetroNet não permite pesos negativos, os pesos usados pelo
Dijkstra atendem à restrição necessária para esse algoritmo.

## 8. Relação entre a matemática e o código

| Conceito matemático | Representação no código |
| --- | --- |
| Grafo | Classe Grafo |
| Conjunto de vértices V | self.pontos |
| Conexões e vizinhos | self.adjacencias |
| Peso de uma conexão | Segundo elemento da tupla |
| Verificação de existência de ponto | possui_ponto() |
| Cadastro de ponto | adicionar_ponto() |
| Cadastro de conexão | adicionar_conexao() |
| Consulta de vizinhos | obter_vizinhos() |

Essa relação permite identificar como os conceitos matemáticos
são utilizados na implementação do sistema.

## 9. Validações e restrições

A estrutura atual do grafo aplica as seguintes regras:

- Um identificador deve ser um texto não vazio.
- Um ponto não pode ser cadastrado duas vezes.
- Os dois pontos de uma conexão precisam existir.
- Uma conexão não pode ser cadastrada novamente.
- Uma conexão não pode ligar um ponto a ele mesmo.
- Os pesos devem ser numéricos, finitos e não negativos.
- Uma conexão não direcionada é registrada nos dois sentidos.

Essas validações ajudam a manter a rede consistente antes da
execução dos algoritmos de busca e roteamento.

## 10. Utilização pelos algoritmos

A modelagem matemática serve de base para os algoritmos obrigatórios
do projeto:

- BFS: explora os pontos por níveis de distância em número de arestas.
- DFS: explora os pontos seguindo caminhos antes de retroceder.
- Dijkstra: encontra um caminho de menor custo em um grafo com pesos
  não negativos.

Esses algoritmos serão implementados em uma etapa posterior,
utilizando a estrutura do grafo.

## 11. Considerações finais

A modelagem por grafo ponderado permite representar os pontos,
as conexões e os custos associados à rede de transporte.

A lista de adjacência foi escolhida para armazenar as conexões de
cada ponto de forma organizada e permitir que os algoritmos consultem
seus vizinhos.

A implementação e os testes devem permanecer coerentes com essa
modelagem matemática.
