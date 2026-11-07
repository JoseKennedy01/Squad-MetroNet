# Busca um caminho de menor custo em um grafo com pesos não negativos.

from heapq import heappop, heappush

def dijkstra(grafo, origem, destino):
    """ Retorna (caminho, custo) ou None se não houver rota.

    Levanta ValueError se a origem ou o destino não estiver cadastrado.
    O grafo valida os pesos e não permite valores negativos.
    """
    if not grafo.possui_ponto(origem):
        raise ValueError(f"A origem {origem!r} não está cadastrada.")

    if not grafo.possui_ponto(destino):
        raise ValueError(f"O destino {destino!r} não está cadastrado.")

    # Mantém a mesma normalização de espaços usada pela classe Grafo.
    origem = origem.strip()
    destino = destino.strip()

    # A distância inicial é zero; as demais serão descobertas pela busca.
    distancias = {origem: 0}
    predecessores = {origem: None}
    fila_prioridade = [(0, origem)]

    while fila_prioridade:
        custo_atual, atual = heappop(fila_prioridade)

        # Ignora entradas antigas quando uma rota melhor já foi encontrada.
        if custo_atual > distancias[atual]:
            continue

        if atual == destino:
            break

        for vizinho, peso in grafo.obter_vizinhos(atual):
            novo_custo = custo_atual + peso

            if vizinho not in distancias or novo_custo < distancias[vizinho]:
                distancias[vizinho] = novo_custo
                predecessores[vizinho] = atual
                heappush(fila_prioridade, (novo_custo, vizinho))

    if destino not in distancias:
        return None

    # Reconstrói o caminho seguindo os predecessores do destino à origem.
    caminho = []
    atual = destino
    while atual is not None:
        caminho.append(atual)
        atual = predecessores[atual]
    caminho.reverse()

    return caminho, distancias[destino]
