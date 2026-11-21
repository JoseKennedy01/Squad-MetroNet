from src.algorithms.busca_largura import busca_largura
from src.algorithms.busca_profundidade import busca_profundidade
from src.algorithms.dijkstra import dijkstra


def obter_algoritmos_disponiveis():
    """Retorna os algoritmos que o menu pode oferecer."""
    return ("BFS", "DFS", "DIJKSTRA")


def calcular_custo_do_caminho(grafo, caminho):
    """Soma os pesos das conexões usadas pelo caminho."""
    custo_total = 0

    for origem, destino in zip(caminho, caminho[1:]):
        for vizinho, peso in grafo.obter_vizinhos(origem):
            if vizinho == destino:
                custo_total += peso
                break
        else:
            raise ValueError("O caminho contém uma conexão inexistente.")

    return custo_total


def executar_rota(grafo, origem, destino, algoritmo):
    """Retorna (caminho, custo) ou None quando não há rota."""
    if not isinstance(algoritmo, str):
        raise ValueError("O algoritmo deve ser informado como texto.")

    nome = algoritmo.strip().upper()

    if nome == "BFS":
        caminho = busca_largura(grafo, origem, destino)
    elif nome == "DFS":
        caminho = busca_profundidade(grafo, origem, destino)
    elif nome == "DIJKSTRA":
        return dijkstra(grafo, origem, destino)
    else:
        raise ValueError(
            "Algoritmo inválido. Escolha BFS, DFS ou DIJKSTRA."
        )

    if caminho is None:
        return None

    return caminho, calcular_custo_do_caminho(grafo, caminho)