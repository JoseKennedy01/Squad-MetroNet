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
DIRETORIO_GRAFICOS = DIRETORIO_RELATORIOS.parent / "figures" # Define a pasta específica para armazenar os gráficos.
TAMANHOS_REDE = [100, 500, 1000]
REPETICOES = 15
REPETICOES_MEMORIA = 5

ALGORITMOS = [
    ("BFS", busca_largura),
    ("DFS", busca_profundidade),
    ("Dijkstra", dijkstra),
]

def validar_resultado(resultado, origem, destino, nome_algoritmo):
    # O Dijkstra pode retornar (caminho, custo); BFS e DFS podem retornar o caminho.
    if (
        isinstance(resultado, tuple)
        and len(resultado) == 2
        and isinstance(resultado[0], (list, tuple))
    ):
        caminho = resultado[0]
    else:
        caminho = resultado

    # Rejeita resultados ausentes, vazios ou que não representem um caminho.
    if not isinstance(caminho, (list, tuple)) or not caminho:
        raise RuntimeError(
            f"{nome_algoritmo} não retornou um caminho válido."
        )

    # Confirma que o caminho liga os pontos solicitados.
    if caminho[0] != origem or caminho[-1] != destino:
        raise RuntimeError(
            f"{nome_algoritmo} retornou um caminho com origem ou destino incorreto."
        )

def medir_tempo(algoritmo, nome_algoritmo, grafo, origem, destino):
    # Executa um aquecimento e também valida o resultado dessa execução.
    resultado = algoritmo(grafo, origem, destino)
    validar_resultado(resultado, origem, destino, nome_algoritmo)

    tempos = []

    for _ in range(REPETICOES):
        inicio = time.perf_counter()
        resultado = algoritmo(grafo, origem, destino)
        fim = time.perf_counter()

        # Valida o resultado fora do intervalo cronometrado.
        tempos.append(fim - inicio)
        validar_resultado(resultado, origem, destino, nome_algoritmo)

    # A mediana reduz a influência de medições excepcionalmente altas ou baixas.
    return statistics.median(tempos)

def medir_memoria(algoritmo, nome_algoritmo, grafo, origem, destino):
    # Repete a medição para reduzir a dependência de uma única execução.
    picos_kib = []

    for _ in range(REPETICOES_MEMORIA):
        tracemalloc.start()

        try:
            resultado = algoritmo(grafo, origem, destino)
            _, pico_bytes = tracemalloc.get_traced_memory()
        finally:
            # Encerra o rastreamento mesmo quando o algoritmo gera uma exceção.
            tracemalloc.stop()

        validar_resultado(resultado, origem, destino, nome_algoritmo)
        picos_kib.append(pico_bytes / 1024)

    return statistics.median(picos_kib)

def salvar_csv(resultados):
    # Mantém o nome do arquivo e as colunas esperadas pelos relatórios.
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
    # Preserva os gráficos de tempo e memória utilizados no projeto.
    configuracoes = [
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
    ]

    for campo, titulo, eixo_y, nome_arquivo in configuracoes:
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

        caminho = DIRETORIO_GRAFICOS / nome_arquivo # Salva o gráfico na pasta destinada às figuras do projeto.
        plt.savefig(caminho, dpi=150)
        plt.close()

        print(f"Gráfico salvo em: {caminho}")

def main():
    resultados = []

    for indice_rede, quantidade in enumerate(TAMANHOS_REDE):
        grafo = gerar_rede_sintetica(quantidade)
        origem = "EST001"
        destino = f"EST{quantidade:03d}"
        quantidade_conexoes = grafo.quantidade_conexoes()

        print(f"\nRede com {quantidade} pontos")
        print(f"Conexões: {quantidade_conexoes}")

        # Alterna a ordem inicial entre as redes para reduzir efeitos de ordem.
        deslocamento = indice_rede % len(ALGORITMOS)
        algoritmos_ordenados = (
            ALGORITMOS[deslocamento:]
            + ALGORITMOS[:deslocamento]
        )

        for nome, algoritmo in algoritmos_ordenados:
            mediana = medir_tempo(
                algoritmo,
                nome,
                grafo,
                origem,
                destino,
            )

            memoria = medir_memoria(
                algoritmo,
                nome,
                grafo,
                origem,
                destino,
            )

            resultados.append(
                {
                    "algoritmo": nome,
                    "pontos": quantidade,
                    "conexoes": quantidade_conexoes,
                    "repeticoes": REPETICOES,
                    "mediana_tempo_segundos": mediana,
                    "pico_memoria_kib": memoria,
                }
            )

            print(
                f"{nome}: mediana = {mediana:.8f} s; "
                f"pico de memória = {memoria:.2f} KiB"
            )
    salvar_csv(resultados)
    gerar_graficos(resultados)

if __name__ == "__main__":
    main()
