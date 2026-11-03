import matplotlib.pyplot as plt
from experimentos.medir import coletar

def gerar_graficos():
    dados = coletar()
    algoritmos = {"bfs": "BFS", "dfs": "DFS", "dijkstra": "Dijkstra"}
    cores = {"bfs": "#2196F3", "dfs": "#4CAF50", "dijkstra": "#FF5722"}

    fig, (ax_tempo, ax_mem) = plt.subplots(1, 2, figsize=(12, 5))

    for chave, rotulo in algoritmos.items():
        series = dados[chave]
        ns = [r["n"] for r in series]
        tempos = [r["tempo"] * 1000 for r in series]
        memorias = [r["memoria"] / 1024 for r in series]

        ax_tempo.plot(ns, tempos, marker="o", label=rotulo, color=cores[chave])
        ax_mem.plot(ns, memorias, marker="o", label=rotulo, color=cores[chave])

    ax_tempo.set_title("Tempo médio de execução")
    ax_tempo.set_xlabel("Número de pontos (V)")
    ax_tempo.set_ylabel("Tempo (ms)")
    ax_tempo.legend()
    ax_tempo.grid(True, linestyle="--", alpha=0.5)

    ax_mem.set_title("Pico de memória")
    ax_mem.set_xlabel("Número de pontos (V)")
    ax_mem.set_ylabel("Memória (KB)")
    ax_mem.legend()
    ax_mem.grid(True, linestyle="--", alpha=0.5)

    fig.suptitle("MetroNet — Comparativo de Desempenho dos Algoritmos", fontsize=13)
    plt.tight_layout()
    plt.savefig("experimentos/resultado_desempenho.png", dpi=150)
    plt.show()

if __name__ == "__main__":
    gerar_graficos()
