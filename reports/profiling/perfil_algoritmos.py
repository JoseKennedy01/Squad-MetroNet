import cProfile
import pstats
import time
from pathlib import Path
from src.algorithms.busca_largura import busca_largura
from src.algorithms.busca_profundidade import busca_profundidade
from src.algorithms.dijkstra import dijkstra
from src.data.gerar_rede_sintetica import gerar_rede_sintetica

# Define o diretório em que os relatórios serão armazenados.
DIRETORIO_RELATORIOS = Path(__file__).resolve().parent

# Utiliza os mesmos tamanhos de rede do benchmark.
TAMANHOS_REDE = [100, 500, 1000]

ALGORITMOS = [
    ("BFS", busca_largura),
    ("DFS", busca_profundidade),
    ("Dijkstra", dijkstra),
]

def validar_resultado(resultado, nome, origem, destino):
    # Dijkstra retorna (caminho, custo); BFS e DFS retornam o caminho.
    if (
        isinstance(resultado, tuple)
        and len(resultado) == 2
        and isinstance(resultado[0], (list, tuple))
    ):
        caminho = resultado[0]
    else:
        caminho = resultado

    # Rejeita resultados vazios ou que não representem um caminho.
    if not isinstance(caminho, (list, tuple)) or not caminho:
        raise RuntimeError(
            f"{nome} não retornou um caminho válido."
        )

    # Confirma que o caminho começa e termina nos pontos solicitados.
    if caminho[0] != origem or caminho[-1] != destino:
        raise RuntimeError(f"{nome} retornou uma origem ou um destino incorreto.")
    return caminho

def executar_perfil(nome, algoritmo, grafo, origem, destino):
    # Cria um profiler independente para cada execução.
    profiler = cProfile.Profile()

    inicio = time.perf_counter()

    # Executa o algoritmo enquanto o cProfile registra as chamadas.
    resultado = profiler.runcall(
        algoritmo,
        grafo,
        origem,
        destino,
    )

    # Este tempo inclui o overhead do profiler.
    tempo_total = time.perf_counter() - inicio

    # Valida o resultado antes de gerar o relatório.
    caminho = validar_resultado(
        resultado,
        nome,
        origem,
        destino,
    )

    print(f"\n{'=' * 60}")
    print(f"Algoritmo: {nome}")
    print(f"Origem: {origem}")
    print(f"Destino: {destino}")
    print(f"Quantidade de pontos: {grafo.quantidade_pontos()}")
    print(f"Quantidade de conexões: {grafo.quantidade_conexoes()}")
    print(f"Tempo com profiling: {tempo_total:.8f} segundos")
    print(f"Quantidade de pontos no caminho: {len(caminho)}")
    print(f"Caminho encontrado: {' -> '.join(caminho)}")

    # O Dijkstra também informa o custo total da rota.
    if nome == "Dijkstra":
        _, custo = resultado
        print(f"Custo total: {custo}")

    print("\nFunções com maior tempo acumulado:")

    # Organiza as estatísticas pelo tempo acumulado em cada função.
    estatisticas = pstats.Stats(profiler)
    estatisticas.strip_dirs()
    estatisticas.sort_stats("cumulative")
    estatisticas.print_stats(10)

    # Salva os dados brutos para análise posterior.
    arquivo_saida = DIRETORIO_RELATORIOS / (
        f"perfil_{nome.lower()}_{grafo.quantidade_pontos()}.prof"
    )
    profiler.dump_stats(str(arquivo_saida))

    print(f"Perfil salvo em: {arquivo_saida}")

def main():
    # Cria o diretório caso ele ainda não exista.
    DIRETORIO_RELATORIOS.mkdir(parents=True, exist_ok=True)

    for quantidade in TAMANHOS_REDE:
        print(f"\n\n### Rede com {quantidade} pontos ###")

        # Todos os algoritmos recebem o mesmo grafo e os mesmos extremos.
        grafo = gerar_rede_sintetica(quantidade)
        origem = "EST001"
        destino = f"EST{quantidade:03d}"

        # Executa cada algoritmo e salva um perfil separado.
        for nome, algoritmo in ALGORITMOS:
            executar_perfil(
                nome,
                algoritmo,
                grafo,
                origem,
                destino,
            )

if __name__ == "__main__":
    main()
