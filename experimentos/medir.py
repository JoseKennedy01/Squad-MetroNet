import time
from experimentos.gerador import gerar_grafo
from src.algorithms.busca_largura import busca_largura

def medir_bfs(grafo, origem, destino, repeticoes=5):
    inicio = time.perf_counter()
    for _ in range(repeticoes):
        busca_largura(grafo, origem, destino)
    return (time.perf_counter() - inicio) / repeticoes