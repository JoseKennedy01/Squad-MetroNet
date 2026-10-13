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

**Estado: planejada; ainda não implementada.**

A busca em profundidade (DFS, do inglês *Depth-First Search*) explora um caminho o máximo possível antes de voltar e seguir por outra conexão.

Assim como a BFS, a DFS pode ser usada para explorar a rede e verificar pontos alcançáveis. Porém, ela não garante encontrar um caminho com o menor número de conexões nem o caminho de menor custo.

Sua implementação deverá manter um conjunto de pontos visitados para evitar ciclos. Com lista de adjacência, sua complexidade esperada é `O(V + E)` no pior caso. A estrutura de apoio — pilha explícita ou recursão — será registrada quando a implementação for definida.

## 5. Algoritmo de Dijkstra

**Estado: planejado; ainda não implementado.**

Dijkstra será utilizado para encontrar um caminho cujo custo total seja mínimo. Diferentemente da BFS e da DFS, esse algoritmo compara os pesos das conexões.

A implementação do MetroNet rejeita pesos negativos e permite pesos zero, atendendo à restrição de Dijkstra de operar com pesos não negativos. A estrutura utilizada para selecionar o próximo ponto de menor custo influenciará a análise de complexidade. Essa escolha e a respectiva análise serão registradas junto à implementação.

## 6. Comparação dos algoritmos

| Algoritmo | Objetivo principal | Utiliza os pesos para escolher o caminho? | Garante o menor número de conexões? |
| --- | --- | --- | --- |
| BFS | Busca por níveis na rede | Não | Sim |
| DFS | Explora caminhos em profundidade | Não | Não |
| Dijkstra | Encontra o caminho de menor custo | Sim | Não necessariamente |

BFS e Dijkstra resolvem problemas diferentes: a BFS minimiza a quantidade de conexões, enquanto Dijkstra minimiza a soma dos custos.

## 7. Relação com os requisitos

- **RF05:** executar BFS — atendido pela busca em largura.
- **RF06:** executar DFS — pendente de implementação.
- **RF07:** executar Dijkstra — pendente de implementação.
- **RF08:** exibir o caminho encontrado — a BFS retorna a sequência de pontos; a interface poderá apresentá-la.
- **RF09:** informar o custo total — será atendido com o cálculo associado ao caminho de Dijkstra.
- **RF10:** informar quando não existir caminho — a BFS retorna `None` quando origem e destino existem, mas não são conectados por uma rota.

Para um caminho retornado como lista, o número de conexões percorridas é `quantidade de pontos no caminho - 1`. O custo total de uma rota ponderada é a soma dos pesos das conexões percorridas.