import random
from src.models.grafo import Grafo


def gerar_grafo(n_pontos, n_extra, semente=42):

    rng = random.Random(semente)
    grafo = Grafo()
    nomes = [f'P{i}' for i in range(n_pontos)]

    for nome in nomes:
        grafo.adicionar_ponto(nome)

    for i in range(n_pontos - 1):
        grafo.adicionar_conexao(nomes[i], nomes[i + 1], rng.randint(1, 10))

    adicionadas = 0
    while adicionadas < n_extra:
        a, b = rng.sample(nomes, 2)
        try:
            grafo.adicionar_conexao(a, b, rng.randint(1, 10))
            adicionadas += 1
        except ValueError:
            pass    

    return grafo, nomes