import matplotlib.pyplot as plt

tamanhos = [10, 50, 100, 500]
tempos_bfs = [0.001, 0.003, 0.008, 0.04]

plt.plot(tamanhos, tempos_bfs, label="BFS")
plt.xlabel("Número de pontos")
plt.ylabel("Tempo (s)")
plt.legend()
plt.show()