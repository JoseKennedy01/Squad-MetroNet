import time
import tracemalloc
import cProfile
import pstats
import io
from experimentos.gerador import gerar_grafo
from src.algorithms.busca_largura import busca_largura
from src.algorithms.busca_profundidade import busca_profundidade
from src.algorithms.dijkstra import dijkstra

TAMANHOS = [10, 50, 100, 250, 500]
EXTRAS = 5
SEMENTE = 42

def medir_tempo(fn, grafo, origem, destino, repeticoes=30):
    inicio = time.perf_counter()
    for _ in range(repeticoes):
        fn(grafo, origem, destino)
    fim = time.perf_counter()
    return (fim - inicio) / repeticoes

def medir_memoria(fn, grafo, origem, destino):
    tracemalloc.start()
    fn(grafo, origem, destino)
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return pico

def executar_profiling(fn, grafo, origem, destino):
    pr = cProfile.Profile()
    pr.enable()
    fn(grafo, origem, destino)
    pr.disable()
    stream = io.StringIO()
    ps = pstats.Stats(pr, stream=stream).sort_stats("cumulative")
    ps.print_stats(5)
    return stream.getvalue()

def coletar():
    resultados = {"bfs": [], "dfs": [], "dijkstra": []}

    for n in TAMANHOS:
        grafo, nomes = gerar_grafo(n, EXTRAS, SEMENTE)
        origem, destino = nomes[0], nomes[-1]

        resultados["bfs"].append({
            "n": n,
            "tempo": medir_tempo(busca_largura, grafo, origem, destino),
            "memoria": medir_memoria(busca_largura, grafo, origem, destino),
        })
        resultados["dfs"].append({
            "n": n,
            "tempo": medir_tempo(busca_profundidade, grafo, origem, destino),
            "memoria": medir_memoria(busca_profundidade, grafo, origem, destino),
        })
        resultados["dijkstra"].append({
            "n": n,
            "tempo": medir_tempo(dijkstra, grafo, origem, destino),
            "memoria": medir_memoria(dijkstra, grafo, origem, destino),
        })

    return resultados

if __name__ == "__main__":
    dados = coletar()
    for algo, series in dados.items():
        print(f"\n{algo.upper()}")
        for r in series:
            print(f"  n={r['n']:>4}  tempo={r['tempo']*1000:.4f} ms  mem={r['memoria']/1024:.2f} KB")

    print("\n--- cProfile (Dijkstra, n=500) ---")
    grafo500, nomes500 = gerar_grafo(500, EXTRAS, SEMENTE)
    print(executar_profiling(dijkstra, grafo500, nomes500[0], nomes500[-1]))

