# 05 — Algoritmos do MetroNet

## 1. Objetivo

Este documento descreve os algoritmos de busca e roteamento previstos para o MetroNet, relacionando seu funcionamento à estrutura de grafo implementada em Python.

O projeto utiliza uma lista de adjacência para representar os pontos e suas conexões. A estrutura permite que os algoritmos consultem os vizinhos de cada ponto sem misturar a lógica de busca com o armazenamento da rede.

## 2. Dados utilizados pelos algoritmos

Os algoritmos recebem um grafo, um ponto de origem e, quando necessário, um ponto de destino.

A classe `Grafo` oferece métodos para consultar se um ponto existe e para obter seus vizinhos. Cada vizinho é retornado junto com o peso da conexão:

```python
("EST02", 5)
```

O peso representa o custo associado à conexão. Os algoritmos podem utilizá-lo de formas diferentes:

- BFS e DFS percorrem as conexões sem usar seus pesos para decidir a ordem da busca.
- Dijkstra utiliza os pesos para encontrar o caminho de menor custo.

## 3. Busca em largura — BFS

**Estado: implementada e testada.**

A busca em largura (BFS, do inglês *Breadth-First Search*) explora a rede por níveis. Primeiro visita os pontos alcançáveis por uma conexão; depois, os alcançáveis por duas conexões, e assim por diante.

Por essa ordem, a BFS encontra um caminho com o menor número de conexões entre a origem e o destino. Ela não encontra necessariamente o caminho de menor custo, pois não utiliza os pesos para escolher a rota.

### Estruturas utilizadas

- **Fila:** guarda os pontos que ainda serão explorados, na ordem em que foram descobertos.
- **Conjunto de visitados:** impede que um ponto seja processado mais de uma vez, inclusive quando existem ciclos.
- **Dicionário de predecessores:** registra de qual ponto viemos para chegar a cada ponto. Ele permite reconstruir o caminho depois da busca.

### Funcionamento

1. Verifica se origem e destino existem no grafo.
2. Coloca a origem na fila e marca-a como visitada.
3. Enquanto houver pontos na fila, retira logicamente o próximo ponto e consulta seus vizinhos.
4. Cada vizinho ainda não visitado é marcado, associado ao ponto atual no dicionário de predecessores e adicionado à fila.
5. Quando o destino é alcançado, reconstrói o caminho seguindo os predecessores até a origem.
6. Se o destino não for descoberto, informa que não existe caminho.

O algoritmo retorna uma lista de pontos. Se origem e destino forem iguais, retorna uma lista com esse único ponto. Se ambos existem, mas não há caminho entre eles, retorna `None`. Um ponto inexistente provoca `ValueError`.

Quando existem vários caminhos com a mesma quantidade mínima de conexões, a BFS retorna o primeiro que encontrar, de acordo com a ordem dos vizinhos fornecida pelo grafo.

### Complexidade

Com lista de adjacência, a BFS visita cada ponto alcançável e examina as conexões desses pontos. No pior caso:

- **Tempo:** `O(V + E)`.
- **Espaço adicional:** `O(V)`.

`V` representa o número de pontos e `E`, o número de conexões. Em um grafo não direcionado, cada conexão aparece nas listas de adjacência dos dois extremos, mas isso não altera a ordem de crescimento da complexidade.


## 4. Busca em profundidade — DFS

**Estado: implementada e testada.**

A busca em profundidade (DFS, do inglês *Depth-First Search*) explora um caminho o máximo possível antes de voltar e seguir por outra conexão.

Assim como a BFS, a DFS permite explorar a rede e verificar quais pontos podem ser alcançados a partir de uma origem. Entretanto, não garante encontrar o caminho com o menor número de conexões nem o caminho de menor custo.

### Estruturas utilizadas

- **Pilha:** controla os pontos que ainda serão explorados. O último ponto inserido é o primeiro a ser retirado.
- **Conjunto de visitados:** evita explorar repetidamente os mesmos pontos e impede que ciclos provoquem buscas intermináveis.
- **Dicionário de predecessores:** registra de qual ponto cada ponto foi alcançado, permitindo reconstruir o caminho encontrado.

### Funcionamento

1. Verifica se a origem e o destino estão cadastrados no grafo.
2. Inicializa a pilha com a origem.
3. Marca os pontos descobertos para evitar inserções repetidas.
4. Retira um ponto da pilha e consulta suas conexões.
5. Adiciona à pilha os vizinhos ainda não descobertos e registra seus predecessores.
6. Quando o destino é encontrado, reconstrói o caminho a partir do dicionário de predecessores.
7. Se o destino não puder ser alcançado, retorna `None`.

A função `busca_profundidade(grafo, origem, destino)`, localizada em `src/algorithms/busca_profundidade.py`, retorna uma lista de identificadores quando encontra um caminho. Quando origem e destino são iguais, retorna uma lista contendo apenas esse ponto. Se algum dos pontos não estiver cadastrado, gera `ValueError`.

A DFS não utiliza os pesos para decidir qual caminho explorar. Sua finalidade é encontrar um caminho válido, e não necessariamente o mais curto ou barato. Quando existem várias rotas possíveis, o caminho encontrado depende da ordem de exploração dos vizinhos.

### Complexidade

Considerando a representação por lista de adjacência:

- **Tempo:** `O(V + E)` no pior caso.
- **Espaço adicional:** `O(V)` para os pontos visitados, os predecessores e a estrutura de exploração.

`V` representa a quantidade de pontos e `E`, a quantidade de conexões. Cada ponto é descoberto uma vez e as conexões dos pontos alcançados são examinadas durante a busca.

### Testes relacionados

Os testes de `tests/test_busca_profundidade.py` verificam caminhos diretos e indiretos, origem igual ao destino, ausência de caminho, pontos inexistentes, grafos direcionados, ciclos, grafo vazio, ponto isolado, ramificações e validade das conexões do caminho retornado.


## 5. Algoritmo de Dijkstra

**Estado: implementado e testado na cópia integrada de revisão.**

Dijkstra encontra um caminho de menor custo acumulado entre a origem e o destino. Ao contrário da BFS e da DFS, ele usa os pesos das conexões para escolher qual ponto explorar em seguida. O algoritmo só é correto com pesos não negativos; a classe `Grafo` rejeita pesos negativos e permite peso zero.

**Arquivo:** `src/algorithms/dijkstra.py`.

### Estruturas utilizadas

- **Fila de prioridade (`heapq`):** fornece primeiro o ponto com menor custo acumulado conhecido.
- **Dicionário de distâncias:** guarda o melhor custo conhecido da origem até cada ponto.
- **Dicionário de predecessores:** registra o ponto anterior para reconstruir a rota.

`heapq` faz parte da biblioteca padrão do Python. Quando uma distância melhora, o algoritmo adiciona uma nova entrada à heap; entradas antigas são ignoradas quando retiradas.

### Funcionamento

1. Verifica se origem e destino estão cadastrados e normaliza espaços externos nos identificadores.
2. Define custo zero para a origem e inicia a fila de prioridade.
3. Retira da fila o ponto com menor custo conhecido.
4. Soma o custo atual ao peso de cada conexão e atualiza a distância e o predecessor quando encontra uma rota melhor.
5. Para quando o destino é retirado como menor custo da fila, ou quando a fila se esvazia.
6. Reconstrói a rota seguindo os predecessores do destino até a origem.

A função `dijkstra(grafo, origem, destino)` retorna `(caminho, custo_total)`. Se os pontos forem válidos mas não houver rota, retorna `None`. Se origem e destino forem iguais, retorna `([origem], 0)`. Um ponto inexistente gera `ValueError`.

### Complexidade

Com a lista de adjacência e a heap binária de `heapq` usada pela implementação:

- **Tempo:** `O((V + E) log V)` para o grafo simples utilizado pelo projeto.
- **Espaço auxiliar:** `O(V + E)`, incluindo entradas repetidas temporárias na heap.

A justificativa detalhada está em `docs/06_complexidade.md`. Esses limites são teóricos; não substituem as medições experimentais exigidas pela especificação.

### Testes relacionados

`tests/test_dijkstra.py` verifica caminho direto e indireto, escolha da rota mais barata, empate de custos, origem igual ao destino, destino inacessível, pontos inexistentes, direção das conexões, peso zero, custo decimal e soma dos pesos ao longo de rotas com várias conexões.

## 6. Comparação dos algoritmos

| Algoritmo | Objetivo principal | Utiliza os pesos para escolher o caminho? | Garante o menor número de conexões? |
| --- | --- | --- | --- |
| BFS | Busca por níveis na rede | Não | Sim |
| DFS | Explora caminhos em profundidade | Não | Não |
| Dijkstra | Encontra o caminho de menor custo | Sim | Não necessariamente |

BFS e Dijkstra resolvem problemas diferentes: a BFS minimiza a quantidade de conexões, enquanto Dijkstra minimiza a soma dos custos.

## 7. Relação com os requisitos

- **RF05:** executar BFS — atendido pela busca em largura.
- **RF06:** executar DFS — atendido pela busca em profundidade implementada e testada.
- **RF07:** executar Dijkstra — implementado em `src/algorithms/dijkstra.py`.
- **RF08:** exibir o caminho encontrado — BFS, DFS e Dijkstra retornam a sequência de pontos; uma interface ou demonstração deve apresentar esse retorno.
- **RF09:** informar o custo total — Dijkstra retorna o custo acumulado junto com o caminho.
- **RF10:** informar quando não existir caminho — os três algoritmos retornam `None` quando os pontos existem, mas não há rota.

Para um caminho retornado como lista, o número de conexões percorridas é `quantidade de pontos no caminho - 1`. O custo total de uma rota ponderada é a soma dos pesos das conexões percorridas.