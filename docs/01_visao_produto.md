# 01 — Visão do Produto MetroNet

## 1. Visão geral

O MetroNet é um projeto acadêmico desenvolvido em Python para representar uma rede de transporte como um grafo ponderado e aplicar algoritmos de busca e roteamento.

A rede é formada por pontos de transporte conectados por arestas. Cada conexão possui um peso numérico não negativo, que pode representar uma medida de deslocamento, como distância, tempo ou custo, conforme os dados utilizados.

O projeto relaciona conceitos de Matemática Discreta, estruturas de dados e algoritmos à resolução de problemas de caminhos em grafos.

## 2. Problema abordado

Em uma rede de transporte, diferentes pontos podem estar conectados por várias rotas. Para analisar essas conexões, é necessário representar a rede de maneira organizada e utilizar algoritmos capazes de encontrar caminhos.

O MetroNet busca demonstrar como uma estrutura de grafo pode representar essa rede e como diferentes algoritmos podem resolver problemas de busca e roteamento.

## 3. Objetivo geral

Desenvolver uma implementação modular em Python que permita cadastrar e consultar pontos e conexões de uma rede de transporte, executar algoritmos de busca e calcular rotas conforme os critérios definidos para cada algoritmo.

## 4. Objetivos específicos

- Cadastrar pontos de transporte.
- Cadastrar conexões entre pontos.
- Associar pesos às conexões.
- Consultar os pontos e seus vizinhos.
- Executar busca em largura (BFS).
- Executar busca em profundidade (DFS).
- Implementar Dijkstra para encontrar caminhos de menor custo.
- Reconstruir e apresentar os caminhos encontrados.
- Identificar quando não existe caminho entre origem e destino.
- Desenvolver testes automatizados.
- Documentar a modelagem matemática e a arquitetura.
- Analisar a complexidade teórica e o desempenho experimental dos algoritmos.

## 5. Público e contexto de utilização

O público principal do projeto é acadêmico, especialmente estudantes e avaliadores interessados em Matemática Discreta, teoria dos grafos, algoritmos e estruturas de dados.

O sistema serve como demonstração prática da representação de uma rede e da aplicação de algoritmos para explorar suas conexões.

## 6. Funcionalidades previstas

O MetroNet contempla as seguintes funcionalidades:

1. Cadastro e consulta de pontos.
2. Cadastro e consulta de conexões ponderadas.
3. Busca de caminhos utilizando BFS.
4. Busca de caminhos utilizando DFS.
5. Busca de caminhos de menor custo utilizando Dijkstra.
6. Retorno do caminho encontrado ou indicação de que não existe rota.
7. Cálculo do custo total para os caminhos ponderados.
8. Testes automatizados e análise de complexidade.

As funcionalidades devem ser consideradas concluídas somente quando estiverem implementadas, testadas e documentadas.

## 7. Tecnologias

As tecnologias previstas para o projeto são:

- **Python:** implementação do grafo e dos algoritmos.
- **pytest:** testes automatizados.
- **matplotlib:** visualização de resultados experimentais, quando aplicável.
- **cProfile:** análise do desempenho do código.
- **Git e GitHub:** controle de versão e colaboração.

## 8. Limites do projeto

O escopo atual prioriza a implementação dos algoritmos e a documentação acadêmica em Python.

Uma aplicação web, um aplicativo móvel, serviços distribuídos e integrações externas não fazem parte do escopo atual.

A implementação deve evitar funcionalidades que não sejam necessárias para os requisitos definidos no projeto.

## 9. Critérios gerais de sucesso

O projeto será considerado satisfatório quando:

- A representação do grafo permitir cadastrar e consultar pontos e conexões válidas.
- Os algoritmos previstos estiverem implementados de acordo com seus objetivos.
- Os casos importantes e as entradas inválidas forem cobertos por testes automatizados.
- Os caminhos retornados forem coerentes com as conexões existentes.
- O custo total for calculado corretamente pelo algoritmo de roteamento correspondente.
- A documentação explicar a modelagem, a arquitetura, os algoritmos, os testes e a complexidade.
- A análise de desempenho utilizar resultados obtidos experimentalmente, sem inventar medições.
