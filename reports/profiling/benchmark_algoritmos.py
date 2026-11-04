import csv
import math
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

def validar_resultado(resultado, grafo, origem, destino, nome_algoritmo):
    # Separa o caminho e o custo retornados pelo Dijkstra.
    if nome_algoritmo == "Dijkstra":
        if not isinstance(resultado, tuple) or len(resultado) != 2:
            raise RuntimeError(
                "Dijkstra deveria retornar uma tupla (caminho, custo)."
            )

        caminho, custo = resultado

        # Verifica se o custo é numérico, finito e não negativo.
        if (
            isinstance(custo, bool)
            or not isinstance(custo, (int, float))
            or not math.isfinite(custo)
            or custo < 0
        ):
            raise RuntimeError("Dijkstra retornou um custo inválido.")

    else:
        caminho = resultado

    # Rejeita resultados ausentes ou que não representem um caminho.
    if not isinstance(caminho, (list, tuple)) or not caminho:
        raise RuntimeError(
            f"{nome_algoritmo} não retornou um caminho válido."
        )

    # Confirma que o caminho liga os pontos solicitados.
    if caminho[0] != origem or caminho[-1] != destino:
        raise RuntimeError(
            f"{nome_algoritmo} retornou um caminho com origem "
            "ou destino incorreto."
        )

    # Verifica se todos os pontos do caminho estão cadastrados.
    for ponto in caminho:
        if not grafo.possui_ponto(ponto):
            raise RuntimeError(
                f"{nome_algoritmo} retornou um ponto inexistente: {ponto}."
            )

    # Verifica se cada par consecutivo possui uma conexão real.
    for indice in range(len(caminho) - 1):
        ponto_atual = caminho[indice]
        proximo_ponto = caminho[indice + 1]

        vizinhos = grafo.obter_vizinhos(ponto_atual)

        if not any(
            vizinho == proximo_ponto
            for vizinho, peso in vizinhos
        ):
            raise RuntimeError(
                f"{nome_algoritmo} retornou uma conexão inexistente: "
                f"{ponto_atual} -> {proximo_ponto}."
            )

def medir_tempo(algoritmo, nome_algoritmo, grafo, origem, destino):
    # Inicia a medição do tempo de execução.
    inicio = time.perf_counter()
    resultado = algoritmo(grafo, origem, destino)
    fim = time.perf_counter()

    # Valida o resultado fora do intervalo cronometrado.
    validar_resultado(resultado, grafo, origem, destino, nome_algoritmo)

    # Retorna o tempo individual da execução.
    return fim - inicio

def medir_memoria(algoritmo, nome_algoritmo, grafo, origem, destino):
    # Mede o pico de memória de uma única execução.
    tracemalloc.start()

    try:
        resultado = algoritmo(grafo, origem, destino)
        _, pico_bytes = tracemalloc.get_traced_memory()
    finally:
        # Encerra o rastreamento mesmo quando ocorre uma exceção.
        tracemalloc.stop()

    # Valida o resultado depois de encerrar o rastreamento.
    validar_resultado(resultado, grafo, origem, destino, nome_algoritmo)

    # Converte bytes para KiB.
    return pico_bytes / 1024

def salvar_csv(resultados):
    # Mantém o nome do arquivo utilizado pelos relatórios.
    arquivo_csv = DIRETORIO_RELATORIOS / "resultados_benchmark.csv"

    # Identifica separadamente as repetições de tempo e memória.
    colunas = [
        "algoritmo",
        "pontos",
        "conexoes",
        "repeticoes_tempo",
        "repeticoes_memoria",
        "mediana_tempo_segundos",
        "pico_memoria_kib",
    ]

    # Abre o CSV para escrita utilizando UTF-8.
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

        # Prepara uma lista para armazenar as medições de cada algoritmo.
        tempos = {nome: [] for nome, _ in ALGORITMOS}
        memorias = {nome: [] for nome, _ in ALGORITMOS}

        # Mantém o aquecimento separado das medições oficiais.
        for nome, algoritmo in ALGORITMOS:
            resultado = algoritmo(grafo, origem, destino)
            validar_resultado(
                resultado, grafo, origem, destino, nome
            )
        # Executa as 15 rodadas de tempo com ordem alternada.
        for rodada in range(REPETICOES):
            deslocamento = (
                indice_rede + rodada
            ) % len(ALGORITMOS)

            algoritmos_ordenados = (
                ALGORITMOS[deslocamento:]
                + ALGORITMOS[:deslocamento]
            )
            for nome, algoritmo in algoritmos_ordenados:
                tempo = medir_tempo(
                    algoritmo,
                    nome,
                    grafo,
                    origem,
                    destino,
                )
                tempos[nome].append(tempo)

        # Executa as 5 rodadas de memória com ordem alternada.
        for rodada in range(REPETICOES_MEMORIA):
            deslocamento = (
                indice_rede + rodada
            ) % len(ALGORITMOS)

            algoritmos_ordenados = (
                ALGORITMOS[deslocamento:]
                + ALGORITMOS[:deslocamento]
            )

            for nome, algoritmo in algoritmos_ordenados:
                memoria = medir_memoria(
                    algoritmo,
                    nome,
                    grafo,
                    origem,
                    destino,
                )

                memorias[nome].append(memoria)

        # Calcula as medianas depois de concluir todas as rodadas.
        for nome, _ in ALGORITMOS:
            mediana = statistics.median(tempos[nome])
            memoria = statistics.median(memorias[nome])

            resultados.append(
                {
                    "algoritmo": nome,
                    "pontos": quantidade,
                    "conexoes": quantidade_conexoes,
                    "repeticoes_tempo": REPETICOES,
                    "repeticoes_memoria": REPETICOES_MEMORIA,
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