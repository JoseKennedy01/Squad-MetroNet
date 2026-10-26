import cProfile
import pstats
import time
from pathlib import Path
from src.algorithms.busca_largura import busca_largura
from src.algorithms.busca_profundidade import busca_profundidade
from src.algorithms.dijkstra import dijkstra
from src.data.gerar_rede_sintetica import gerar_rede_sintetica

DIRETORIO_RELATORIOS = Path(__file__).resolve().parent
TAMANHOS_REDE = [100, 500, 1000]

def executar_perfil(nome, algoritmo, grafo, origem, destino):
    # Executa um algoritmo e registra seu perfil de desempenho.
    profiler = cProfile.Profile()

    inicio = time.perf_counter()
    resultado = profiler.runcall(
        algoritmo,
        grafo,
        origem,
        destino,
    )
    tempo_total = time.perf_counter() - inicio

    print(f"\n{'=' * 60}")
    print(f"Algoritmo: {nome}")
    print(f"Tempo total medido: {tempo_total:.6f} segundos")
    print(f"Quantidade de pontos: {grafo.quantidade_pontos()}")
    print(f"Quantidade de conexões: {grafo.quantidade_conexoes()}")

    if resultado is None:
        print("Resultado: nenhum caminho encontrado.")
    elif nome == "Dijkstra":
        caminho, custo = resultado
        print(f"Quantidade de pontos no caminho: {len(caminho)}")
        print(f"Custo total: {custo}")
    else:
        print(f"Quantidade de pontos no caminho: {len(resultado)}")

    print("\nFunções com maior tempo acumulado:")

    estatisticas = pstats.Stats(profiler)
    estatisticas.strip_dirs()
    estatisticas.sort_stats("cumulative")
    estatisticas.print_stats(10)

    arquivo_saida = DIRETORIO_RELATORIOS / (
        f"perfil_{nome.lower()}_{grafo.quantidade_pontos()}.prof"
    )
    profiler.dump_stats(str(arquivo_saida))

    print(f"Perfil salvo em: {arquivo_saida}")

def main():
    algoritmos = [
        ("BFS", busca_largura),
        ("DFS", busca_profundidade),
        ("Dijkstra", dijkstra),
    ]

    for quantidade in TAMANHOS_REDE:
        print(f"\n\n### Rede com {quantidade} pontos ###")

        grafo = gerar_rede_sintetica(quantidade)
        origem = "EST001"
        destino = f"EST{quantidade:03d}"

        for nome, algoritmo in algoritmos:
            executar_perfil(
                nome,
                algoritmo,
                grafo,
                origem,
                destino,
            )

if __name__ == "__main__":
    main()
