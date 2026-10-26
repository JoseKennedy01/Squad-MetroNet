import csv
import statistics
import time
import tracemalloc
from pathlib import Path
import matplotlib.pyplot as plt
from src.algorithms.busca_largura import busca_largura
from src.algorithms.busca_profundidade import busca_profundidade
from src.algorithms.dijkstra import dijkstra
from src.data.gerar_rede_sintetica import gerar_rede_sintetica

DIRETORIO_RELATORIOS = Path(__file__).resolve().parent
TAMANHOS_REDE = [100, 500, 1000]
REPETICOES = 15
ALGORITMOS = [
    ("BFS", busca_largura),
    ("DFS", busca_profundidade),
    ("Dijkstra", dijkstra),
]


def medir_tempo(algoritmo, grafo, origem, destino):
    # Calcula a mediana dos tempos de execução.
    tempos = []

    algoritmo(grafo, origem, destino)  # Aquecimento inicial.

    for _ in range(REPETICOES):
        inicio = time.perf_counter()
        resultado = algoritmo(grafo, origem, destino)
        fim = time.perf_counter()

        tempos.append(fim - inicio)

        if resultado is None:
            raise RuntimeError("O algoritmo não encontrou um caminho.")

    return statistics.median(tempos)


def medir_memoria(algoritmo, grafo, origem, destino):
    # Mede o pico de memória rastreada durante uma execução.
    tracemalloc.start()

    try:
        resultado = algoritmo(grafo, origem, destino)
        _, pico_bytes = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    if resultado is None:
        raise RuntimeError("O algoritmo não encontrou um caminho.")

    return pico_bytes / 1024


def salvar_csv(resultados):
    # Salva os resultados em formato CSV.
    arquivo_csv = DIRETORIO_RELATORIOS / "resultados_benchmark.csv"

    colunas = [
        "algoritmo",
        "pontos",
        "conexoes",
        "repeticoes",
        "mediana_tempo_segundos",
        "pico_memoria_kib",
    ]

    with arquivo_csv.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(resultados)

    print(f"\nCSV salvo em: {arquivo_csv}")

def gerar_graficos(resultados):
    # Gera gráficos de tempo e memória.
    for campo, titulo, eixo_y, nome_arquivo in [
        (
            "mediana_tempo_segundos",
            "Tempo de execução dos algoritmos",
            "Mediana do tempo (segundos)",
            "tempo_algoritmos.png",
        ),
        (
            "pico_memoria_kib",
            "Pico de memória rastreada",
            "Pico de memória (KiB)",
            "memoria_algoritmos.png",
        ),
    ]:
        plt.figure(figsize=(9, 5))

        for nome_algoritmo, _ in ALGORITMOS:
            dados = [
                item for item in resultados
                if item["algoritmo"] == nome_algoritmo
            ]

            pontos = [item["pontos"] for item in dados]
            valores = [item[campo] for item in dados]

            plt.plot(
                pontos,
                valores,
                marker="o",
                label=nome_algoritmo,
            )

        plt.title(titulo)
        plt.xlabel("Quantidade de pontos")
        plt.ylabel(eixo_y)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        caminho = DIRETORIO_RELATORIOS / nome_arquivo
        plt.savefig(caminho, dpi=150)
        plt.close()

        print(f"Gráfico salvo em: {caminho}")

def main():
    resultados = []

    for quantidade in TAMANHOS_REDE:
        grafo = gerar_rede_sintetica(quantidade)
        origem = "EST001"
        destino = f"EST{quantidade:03d}"

        print(f"\nRede com {quantidade} pontos")
        print(f"Conexões: {grafo.quantidade_conexoes()}")

        for nome, algoritmo in ALGORITMOS:
            mediana = medir_tempo(
                algoritmo,
                grafo,
                origem,
                destino,
            )

            memoria = medir_memoria(
                algoritmo,
                grafo,
                origem,
                destino,
            )

            resultado = {
                "algoritmo": nome,
                "pontos": quantidade,
                "conexoes": grafo.quantidade_conexoes(),
                "repeticoes": REPETICOES,
                "mediana_tempo_segundos": mediana,
                "pico_memoria_kib": memoria,
            }

            resultados.append(resultado)

            print(
                f"{nome}: mediana = {mediana:.8f} s; "
                f"pico de memória = {memoria:.2f} KiB"
            )

    salvar_csv(resultados)
    gerar_graficos(resultados)

if __name__ == "__main__":
    main()
