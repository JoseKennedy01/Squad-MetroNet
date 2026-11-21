from src.models.grafo import Grafo

def gerar_rede_sintetica(quantidade_pontos: int) -> Grafo:
    # Gera uma rede conectada e determinística para testes.
    if (
        isinstance(quantidade_pontos, bool)
        or not isinstance(quantidade_pontos, int)
        or quantidade_pontos < 1
    ):
        raise ValueError("A quantidade de pontos deve ser um inteiro positivo.")

    grafo = Grafo(direcionado=False)

    pontos = [
        f"EST{numero:03d}"
        for numero in range(1, quantidade_pontos + 1)
    ]

    for ponto in pontos:
        grafo.adicionar_ponto(ponto)

    # Conecta cada ponto ao seguinte para garantir conectividade.
    for indice in range(quantidade_pontos - 1):
        peso = float((indice % 9) + 1)
        grafo.adicionar_conexao(
            pontos[indice],
            pontos[indice + 1],
            peso,
        )

    # Adiciona conexões extras quando existem pontos suficientes.
    for indice in range(quantidade_pontos - 2):
        origem = pontos[indice]
        destino = pontos[indice + 2]
        peso = float(((indice + 3) % 9) + 1)

        grafo.adicionar_conexao(origem, destino, peso)

    return grafo
